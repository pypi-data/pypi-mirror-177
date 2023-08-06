import argparse
import os
import datetime
import urllib.parse
import dacite
import json
from collections import defaultdict
from dataclasses import dataclass, replace
from typing import List, Optional, Dict, Any, Tuple, Set

from helm.common.general import (
    write,
    ensure_directory_exists,
    asdict_without_nones,
    singleton,
    unique_simplification,
    parallel_map,
)
from helm.common.hierarchical_logger import hlog, htrack, htrack_block
from helm.benchmark.scenarios.scenario import ScenarioSpec
from helm.benchmark.adapter import AdapterSpec
from helm.benchmark.metrics.metric_name import MetricName
from helm.benchmark.metrics.metric import get_all_stats_by_name
from helm.benchmark.metrics.statistic import Stat, merge_stat
from helm.benchmark.runner import RunSpec
from .table import Cell, Table, Hyperlink, table_to_latex
from .schema import (
    MetricNameMatcher,
    RunGroup,
    read_schema,
    SCHEMA_YAML_FILENAME,
    BY_GROUP,
    THIS_GROUP_ONLY,
    NO_GROUPS,
    DOWN_ARROW,
)
from .contamination import read_contamination, validate_contamination, CONTAMINATION_SYMBOLS, CONTAMINATION_STYLES

"""
Reads the output of the benchmark runs and produces:
- JSON files for the frontend
- Tables for the paper

Usage:

    venv/bin/helm-summarize --suite <Name of the suite>

"""


@dataclass(frozen=True)
class ExecutiveSummary:
    """
    Summary of the output of benchmarking.
    This is always loaded by the frontend, so keep this small
    """

    suite: str
    date: str

    # TODO: later, put model rankings, etc. here


@dataclass(frozen=True)
class Run:
    """Represents a run with spec and stats."""

    # Directory name of the run (used by frontend to find the actual instances to load)
    run_path: str

    # Run spec for the run
    run_spec: RunSpec

    # Statistics for the run
    stats: List[Stat]


def get_unique_stat_by_matcher(stats: List[Stat], matcher: MetricNameMatcher) -> Optional[Stat]:
    """Return the single stat that matches."""
    matching_stats = [stat for stat in stats if matcher.matches(stat.name)]
    if len(matching_stats) == 0:
        # HACK: if we are looking for `quasi_exact_match` and it's not there, try `exact_match` instead
        # This is necessary for prompting ablations at the moment, since some scenarios normally have quasi_exact_match
        # as the main metric but multiple_choice_separate_original only generates exact_match
        if matcher.name == "quasi_exact_match":
            hlog("WARNING: No quasi_exact_match metric found, looking for exact_match instead")
            matcher = replace(matcher, name="exact_match")
            matching_stats = [stat for stat in stats if matcher.matches(stat.name)]
            if len(matching_stats) == 0:
                return None
        else:
            return None

    # Matcher matches all sub splits so we should aggregate these
    if matcher.sub_split is None:
        stats_dict: Dict[MetricName, Stat] = {}
        for stat in matching_stats:
            stat = Stat(replace(stat.name, sub_split=None)).merge(stat)
            merge_stat(stats_dict, stat)
        matching_stats = list(stats_dict.values())

    return singleton(matching_stats)


def get_benchmarking_url(params: Dict[str, str]) -> str:
    # Don't encode ' ' as '+'
    return "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def dict_to_str(d: Dict[str, Any]) -> str:
    return ", ".join(f"{k}: {v}" for k, v in d.items())


def get_scenario_name(group: RunGroup, scenario_spec: ScenarioSpec):
    return group.name + "_" + dict_to_str(scenario_spec.args).replace(" ", "").replace("/", "_")


def get_coarse_adapter_spec(
    adapter_spec: AdapterSpec, scenario_spec: Optional[ScenarioSpec] = None, adapter_keys_shown: List[str] = []
) -> AdapterSpec:
    """
    Return an abstraction of an AdapterSpec that corresponds to the method
    (e.g., model, decoding parameters), and not the part that contains
    scenario-specific things like instructions.
    This is not an easy thing to disentangle, so just try our best
    in a necessarily scenario-specific way.
    """
    # TODO: clean up this logic a bit
    # Sometimes the instructions contain information about the scenario.
    if scenario_spec and scenario_spec.class_name.endswith(".MMLUScenario"):
        # MMLU: Sync up with logic in `get_mmlu_spec` for constructing the instructions.
        subject = scenario_spec.args["subject"].replace("_", " ")
        instructions = adapter_spec.instructions.replace(subject, "___")
    elif scenario_spec and scenario_spec.class_name.endswith(".RAFTScenario"):
        # RAFT scenario has arbitrary instructions, so impossible to remove
        # the scenario information, so remove all of it.
        instructions = "<scenario specific>"
    else:
        instructions = adapter_spec.instructions
    adapter_spec = replace(adapter_spec, instructions=instructions)

    # Create a new adapter_spec, keeping only the model and the keys in adapter_keys_shown
    adapter_spec_kwargs = {key: adapter_spec.__dict__[key] for key in adapter_keys_shown}
    return AdapterSpec(**adapter_spec_kwargs)  # type: ignore


def get_method_display_name(model_display_name: Optional[str], info: Dict[str, Any]) -> str:
    """
    Return a nice name to display for `adapter_spec` which denotes a method.
    `info` contains the decoding parameters.

    Format: Model (info...)
    """
    info = dict(info)
    if "model" in info:
        del info["model"]

    return (model_display_name or "???") + (f" [{dict_to_str(info)}]" if len(info) > 0 else "")


class Summarizer:
    """Summarize the benchmark results in JSON files to be displayed in the UI."""

    COST_REPORT_FIELDS: List[str] = ["num_prompt_tokens", "num_completion_tokens", "num_completions", "num_requests"]

    # We need to hide stats for these model-metric combinations
    LOGPROBS_ISSUE_MODELS: Set[str] = {
        "anthropic/stanford-online-all-v4-s3",
        "ai21/j1-jumbo",
        "ai21/j1-grande",
        "ai21/j1-large",
    }
    LOGPROBS_ISSUE_METRICS: Set[str] = {
        # MSMARCO metrics
        "NDCG@10",
        "RR@10",
        "NDCG@20",
        "RR@20",
        # Calibration metrics
        "ece_1_bin",
        "ece_10_bin",
        "platt_ece_1_bin",
        "platt_ece_10_bin",
        "platt_coef",
        "platt_intercept",
        "selective_cov_acc_area",
        "selective_acc@10",
    }

    def __init__(self, suite: str, output_path: str, verbose: bool, num_threads: int):
        self.suite: str = suite
        self.run_suite_path: str = os.path.join(output_path, "runs", suite)
        self.verbose: bool = verbose
        self.num_threads: int = num_threads

        self.schema = read_schema()
        self.contamination = read_contamination()
        validate_contamination(self.contamination, self.schema)

    def read_run(self, run_path: str) -> Run:
        """Load the `Run` object from `run_path`."""

        with open(os.path.join(run_path, "run_spec.json")) as f:
            run_spec = dacite.from_dict(RunSpec, json.load(f))

        with open(os.path.join(run_path, "stats.json")) as f:
            stats = [dacite.from_dict(Stat, raw) for raw in json.load(f)]

        return Run(
            run_path=run_path,
            run_spec=run_spec,
            stats=stats,
        )

    def compute_slim_per_instance_stats(self, per_instance_stats: List[Dict]) -> List[Dict]:
        """Given per instance stats, output a slim version for the frontend."""
        result = []
        for instance in per_instance_stats:
            slim_instance = {}
            # Unfortunately we can't pre-compute the instance key because
            # Python's JSON serialization is slightly different from JavaScript's.
            slim_instance["instance_id"] = instance["instance_id"]
            if "perturbation" in instance:
                slim_instance["perturbation"] = instance["perturbation"]
            slim_instance["train_trial_index"] = instance["train_trial_index"]
            slim_instance["stats"] = []
            for stat in instance["stats"]:
                slim_stat = {}
                slim_stat["name"] = {"name": stat["name"]["name"]}
                if "mean" in stat:
                    slim_stat["mean"] = stat["mean"]
                slim_instance["stats"].append(slim_stat)
            result.append(slim_instance)
        return result

    @htrack(None)
    def write_slim_per_instance_stats(self) -> None:
        """
        For each run, load per_instance_stats.json and write per_instance_stats_slim.json.
        TODO: Move this logic to Runner, so it gets generated during the run
              https://github.com/stanford-crfm/helm/issues/1119
        """
        run_specs_path: str = os.path.join(self.run_suite_path, "run_specs.json")
        assert os.path.exists(run_specs_path), f"{run_specs_path} does not exist."

        with open(run_specs_path) as f:
            raw_run_specs = json.load(f)

        def process(raw_run_spec: Dict):
            run_spec = dacite.from_dict(RunSpec, raw_run_spec)
            run_path: str = os.path.join(self.run_suite_path, run_spec.name)

            per_instance_stats_path: str = os.path.join(run_path, "per_instance_stats.json")
            if os.path.exists(per_instance_stats_path):
                per_instance_stats: List[Dict]
                with open(per_instance_stats_path) as input_file:
                    per_instance_stats = json.load(input_file)
                per_instance_stats_slim_path = f"{per_instance_stats_path[:-len('.json')]}_slim.json"
                with open(per_instance_stats_slim_path, "w") as output_file:
                    json.dump(self.compute_slim_per_instance_stats(per_instance_stats), output_file)

        parallel_map(process, raw_run_specs, parallelism=self.num_threads)

    def filter_runs_by_visibility(self, runs: List[Run], group: RunGroup) -> List[Run]:
        """Filter the list of runs and only keep runs relevant to this group."""
        filtered_runs: List[Run] = []
        for run in runs:
            included = True
            if group.visibility == THIS_GROUP_ONLY:  # don't include the canonical runs when looking at, say, ablations
                included = False
            for run_group_name in run.run_spec.groups:  # go through the groups of the run to determine visibility
                if run_group_name not in self.schema.name_to_run_group:
                    hlog(
                        f"WARNING: group {run_group_name} mentioned in run spec {run.run_spec.name} "
                        f"but undefined in {SCHEMA_YAML_FILENAME}, skipping"
                    )
                    continue
                run_group = self.schema.name_to_run_group[run_group_name]
                if run_group.visibility == NO_GROUPS:  # this run should never be visible
                    included = False
                    break
                if run_group.visibility == THIS_GROUP_ONLY:  # this run is part of a group with partial visibility
                    if run_group.name == group.name:  # if this is the exact group we are visualizing, include for sure
                        included = True
                        break
                    else:  # we won't visualize unless we hit exactly the group with partial visibility
                        included = False
            if included:
                filtered_runs.append(run)
        return filtered_runs

    def read_runs(self):
        """Load the corresponding runs for the run specs in run_specs.json."""

        run_specs_path: str = os.path.join(self.run_suite_path, "run_specs.json")
        if not os.path.exists(run_specs_path):
            hlog(f"Summarizer won't run because {run_specs_path} doesn't exist yet. This is expected in a dry run.")
            return []

        self.runs: List[Run] = []
        with open(run_specs_path) as f:
            raw_run_specs = json.load(f)
        for raw_run_spec in raw_run_specs:
            run_spec = dacite.from_dict(RunSpec, raw_run_spec)
            run_path: str = os.path.join(self.run_suite_path, run_spec.name)

            run_spec_path: str = os.path.join(run_path, "run_spec.json")
            stats_path: str = os.path.join(run_path, "stats.json")

            if os.path.exists(run_spec_path) and os.path.exists(stats_path):
                run = self.read_run(run_path)
                self.runs.append(run)
            else:
                hlog(f"WARNING: {run_path} doesn't have run_spec.json or stats.json, skipping")

        # For each group (e.g., natural_qa), map
        # (i) scenario spec (e.g., subject=philosophy) [optional] and
        # (ii) adapter spec (e.g., model = openai/davinci)
        # to list of runs
        self.group_adapter_to_runs: Dict[str, Dict[AdapterSpec, List[Run]]] = defaultdict(lambda: defaultdict(list))
        self.group_scenario_adapter_to_runs: Dict[str, Dict[ScenarioSpec, Dict[AdapterSpec, List[Run]]]] = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list))
        )
        for run in self.runs:
            scenario_spec = run.run_spec.scenario_spec
            adapter_spec = run.run_spec.adapter_spec
            for group_name in run.run_spec.groups:
                self.group_adapter_to_runs[group_name][adapter_spec].append(run)
                self.group_scenario_adapter_to_runs[group_name][scenario_spec][adapter_spec].append(run)

    @htrack(None)
    def check_metrics_defined(self):
        """Check that all the metrics that appear in stats are defined."""
        # Compute all metric names that were encountered
        metric_name_to_run_spec_names: Dict[str, List[str]] = defaultdict(list)
        for run in self.runs:
            for stat in run.stats:
                metric_name_to_run_spec_names[stat.name.name].append(run.run_spec.name)

        defined_metric_names = set(entry.name for entry in self.schema.metrics)

        for metric_name, run_spec_names in metric_name_to_run_spec_names.items():
            if metric_name not in defined_metric_names:
                hlog(
                    f"WARNING: metric name {metric_name} undefined in {SCHEMA_YAML_FILENAME} "
                    f"but appears in {len(run_spec_names)} run specs, including {run_spec_names[0]}"
                )

    @htrack(None)
    def write_executive_summary(self):
        """Write the executive summary."""
        date = datetime.date.today().strftime("%Y-%m-%d")

        summary = ExecutiveSummary(
            suite=self.suite,
            date=date,
        )
        write(
            os.path.join(self.run_suite_path, "summary.json"),
            json.dumps(asdict_without_nones(summary), indent=2),
        )

    @htrack(None)
    def write_cost_report(self):
        """Write out the information we need to calculate costs per model."""
        # TODO: move to write_executive_summary()
        models_to_costs: Dict[str, Dict[str]] = defaultdict(lambda: defaultdict(int))
        for run in self.runs:
            model: str = run.run_spec.adapter_spec.model

            for stat in run.stats:
                stat_name = stat.name.name
                if stat_name in Summarizer.COST_REPORT_FIELDS and not stat.name.split:
                    models_to_costs[model][stat_name] += stat.sum

        # Do a second pass to add up the total number of tokens
        for costs in models_to_costs.values():
            costs["total_tokens"] = costs["num_prompt_tokens"] + costs["num_completion_tokens"]

        write(
            os.path.join(self.run_suite_path, "costs.json"),
            json.dumps(models_to_costs, indent=2),
        )

    def write_runs(self):
        write(
            os.path.join(self.run_suite_path, "runs.json"),
            json.dumps(list(map(asdict_without_nones, self.runs)), indent=2),
        )

    def expand_subgroups(self, group: RunGroup) -> List[RunGroup]:
        """Given a RunGroup, collect a list of its subgroups by traversing the subgroup tree."""

        def expand_subgroups_(group: RunGroup, visited: Set[str]) -> List[RunGroup]:
            if group.name in visited:
                return []
            visited.add(group.name)
            return [group] + [
                subsubgroup
                for subgroup in group.subgroups
                for subsubgroup in expand_subgroups_(self.schema.name_to_run_group[subgroup], visited)
            ]

        return expand_subgroups_(group, visited=set())

    def create_index_tables(self) -> List[Table]:
        """
        Create a table for each RunGroup category, linking to the pages where each one is displayed.
        """
        category_to_groups = defaultdict(list)
        for group in self.schema.run_groups:
            category_to_groups[group.category].append(group)

        def get_cell(stats: List[Stat], compute_mean: bool = False, compute_sum: bool = False) -> Cell:
            """Render a value."""
            if len(stats) == 0:
                return Cell(None)
            aggregate_stat = replace(stats[0])
            for stat in stats[1:]:
                aggregate_stat.merge(stat)
            if compute_mean:
                return Cell(aggregate_stat.mean, description=aggregate_stat.bare_str())
            if compute_sum:
                return Cell(aggregate_stat.sum, description=aggregate_stat.bare_str())
            raise Exception("Either specify compute_mean or compute_sum")

        tables: List[Table] = []
        for category, groups in category_to_groups.items():
            header = [
                Cell("Group"),
                Cell("Description"),
                # Synchronize these names with `schema.yaml`
                Cell("Adaptation method", description="Adaptation strategy (e.g., generation)"),
                Cell("# instances", description="Number of instances evaluated on"),
                Cell("# references", description="Number of references provided per instance"),
                Cell("# prompt tokens", description="Total number of prompt tokens"),
                Cell("# completion tokens", description="Total number of completion tokens"),
                Cell("# models", description="Number of models we're evaluating"),
            ]
            rows: List[List[Cell]] = []
            for group in groups:
                models: Set[str] = set()
                methods: Set[str] = set()
                num_instances: List[Stat] = []
                num_references: List[Stat] = []
                num_prompt_tokens: List[Stat] = []
                num_completion_tokens: List[Stat] = []

                # Go over all the matching runs
                for subgroup in self.expand_subgroups(group):
                    for adapter_spec, runs in self.group_adapter_to_runs[subgroup.name].items():
                        filtered_runs = self.filter_runs_by_visibility(runs, subgroup)
                        models.add(adapter_spec.model)
                        methods.add(adapter_spec.method)
                        for run in filtered_runs:
                            num_instances.extend(get_all_stats_by_name(run.stats, "num_instances"))
                            num_references.extend(get_all_stats_by_name(run.stats, "num_references"))
                            num_prompt_tokens.extend(get_all_stats_by_name(run.stats, "num_prompt_tokens"))
                            num_completion_tokens.extend(get_all_stats_by_name(run.stats, "num_completion_tokens"))

                if len(num_instances) == 0:
                    continue

                rows.append(
                    [
                        Cell(group.display_name, href=get_benchmarking_url({"group": group.name})),
                        Cell(group.description, markdown=True),
                        Cell(", ".join(methods)),
                        get_cell(num_instances, compute_mean=True),
                        get_cell(num_references, compute_mean=True),
                        get_cell(num_prompt_tokens, compute_sum=True),
                        get_cell(num_completion_tokens, compute_sum=True),
                        Cell(len(models)),
                    ]
                )
            tables.append(Table(title=category, header=header, rows=rows))

        return tables

    def create_groups_metadata(self) -> Dict[str, Dict[str, Any]]:
        """
        Create a table for each RunGroup category, linking to the pages where each one is displayed.
        """
        metadata = {}
        for group in self.schema.run_groups:
            metadata[group.name] = {
                "display_name": group.display_name,
                "description": group.description,
                "taxonomy": group.taxonomy and asdict_without_nones(group.taxonomy),
            }
        return metadata

    def create_cell(
        self,
        runs: List[Run],
        matcher: MetricNameMatcher,
        contamination_level: Optional[str],
        additional_info: Optional[str],
        hide_value: bool = False,
    ) -> Cell:
        """
        Use the metric name identified by `matcher` to pull out the stats from
        `runs` and return a representation of the average.
        There are four cases:
        1. No matching runs
        2. Matching runs but no matching stats (maybe stat was named incorrectly)
        3. Matching runs, matching stats, but stats have count = 0, so mean is undefined
           (e.g., bias metric ran and computed 0/0)
        4. Matching runs, matching stats, stats with count > 0

        In the first three cases, the cell value is None, but the description distinguishes between these cases.
        """
        # No runs at all
        if len(runs) == 0:
            return Cell(value=None, description="No matching runs")

        aggregate_stat: Optional[Stat] = None
        aggregated_run_specs: List[str] = []  # keep track of which run_specs we aggregate into the cell for debugging

        for run in runs:
            stat = get_unique_stat_by_matcher(run.stats, matcher)
            if stat is None:
                # Print out near misses to provide a more informative warning
                near_misses = [stat for stat in run.stats if stat.name.name == matcher.name]
                hlog(
                    f"WARNING: run spec {run.run_spec.name} does not have any stat matched by {matcher}, "
                    f"{len(near_misses)} near misses matching just the name"
                )
                if len(near_misses) > 0:
                    with htrack_block("Near misses"):
                        for stat in near_misses:
                            hlog(stat.name)
                continue

            if aggregate_stat is None:
                aggregate_stat = replace(stat)  # Important: copy!
            else:
                assert stat is not None  # Make type-checking happy
                aggregate_stat.merge(stat)
            aggregated_run_specs.append(run.run_spec.name)

        if aggregate_stat is None:
            return Cell(value=None, description=f"{len(runs)} matching runs, but no matching metrics")

        # TODO: need to exclude contaminated numbers somehow
        value: Optional[float] = None if hide_value else aggregate_stat.mean
        description = aggregate_stat.bare_str()
        if additional_info:
            description += "\n" + additional_info
        if self.verbose:
            description += "\n-- ".join(["\nRun specs:", *aggregated_run_specs])

        style: Dict[str, Any] = {}
        if contamination_level is not None:
            style = CONTAMINATION_STYLES.get(contamination_level, style)

        return Cell(value=value, description=description, style=style)

    def create_group_table(
        self,
        name: str,
        title: str,
        adapter_to_runs: Dict[AdapterSpec, List[Run]],
        link_to_runs: bool,
        columns: List[Tuple[RunGroup, str]],  # run_group, metric_group
        sort_by_model_order: bool = True,
        sub_split: Optional[str] = None,
        bold_columns: bool = True,
    ) -> Table:
        """
        Create a table for where each row is an adapter (for which we have a set of runs) and columns are pairs of
        run_group (natural_qa) and metrics (accuracy). This method can be used to either create a table with multiple
        metrics for a single scenario or a table with multiple scenarios together.
        adapter (e.g,  model) and columns are constructed based on metrics.
        """

        # Figure out what the columns of the table are.
        # Create header (cells to display) and the list of metric name filters
        # (to pull out information later).
        if not columns or not adapter_to_runs:
            hlog(f"WARNING: table {title}, has no rows or columns, leaving empty")
            return Table("empty", [], [])

        header: List[Cell] = []
        matchers: List[MetricNameMatcher] = []
        group_names: List[str] = []  # for each column
        num_groups = len(set(run_group.name for run_group, _ in columns))  # number of unique groups, determines headers

        # Column headers
        header.append(Cell("Model/adapter"))
        for run_group, metric_group_name in columns:
            if metric_group_name not in run_group.metric_groups:
                continue
            metric_group = self.schema.name_to_metric_group[metric_group_name]
            for metric in metric_group.metrics:
                matcher = metric.substitute(run_group.environment)
                if sub_split is not None:
                    matcher = replace(matcher, sub_split=sub_split)
                header_field = self.schema.name_to_metric.get(matcher.name)
                if header_field is None:
                    hlog(f"WARNING: metric name {matcher.name} undefined in {SCHEMA_YAML_FILENAME}, skipping")
                    continue

                header_name = header_field.get_short_display_name(arrow=True)
                description = (run_group.description + "\n\n" if run_group.description is not None else "") + (
                    header_field.display_name + ": " + header_field.description
                )

                if matcher.perturbation_name is not None:
                    perturbation_field = self.schema.name_to_perturbation[matcher.perturbation_name]
                    header_name += " (" + perturbation_field.get_short_display_name() + ")"
                    description += (
                        "\n- Perturbation "
                        + perturbation_field.display_name
                        + ": "
                        + (perturbation_field.description or "???")
                    )

                if num_groups > 1:  # we have multiple groups in the same table, so display the name in the column
                    header_name = f"{run_group.get_short_display_name()} - {header_name}"

                header.append(Cell(header_name, description=description))
                matchers.append(matcher)
                group_names.append(run_group.name)

        # TODO: Fix run_group logic
        run_group = columns[0][0]

        def run_spec_names_to_url(run_spec_names: List[str]) -> str:
            return get_benchmarking_url(
                {
                    "group": run_group.name,
                    "subgroup": title,
                    "runSpecs": json.dumps(run_spec_names),
                }
            )

        adapter_specs: List[AdapterSpec] = list(adapter_to_runs.keys())
        if sort_by_model_order:
            # Sort models by the order defined in the schema.
            # Models not defined in the schema will be sorted alphabetically and
            # placed before models in defined the schema.
            model_order = [model.name for model in self.schema.models]

            def _adapter_spec_sort_key(spec):
                index = model_order.index(spec.model) if spec.model in model_order else -1
                return (index, spec.model)

            adapter_specs = list(sorted(adapter_specs, key=_adapter_spec_sort_key))

        # Pull out only the keys of the method adapter_spec that is needed to
        # uniquely identify the method.
        infos = unique_simplification(list(map(asdict_without_nones, adapter_specs)), ["model"])

        assert len(adapter_specs) == len(infos), [adapter_specs, infos]

        # Populate the contents of the table
        rows = []
        for adapter_spec, info in zip(adapter_specs, infos):
            model_name: str = adapter_spec.model

            # Get the model display name from the schema.
            # Fall back to using the model name as the model display name if the model is not
            # defined in the schema.
            model_display_name = (
                self.schema.name_to_model[model_name].display_name
                if model_name in self.schema.name_to_model
                else model_name
            )

            runs = adapter_to_runs[adapter_spec]
            display_name = get_method_display_name(model_display_name, info)

            # Link to all the runs under this model
            if link_to_runs:
                run_spec_names = [run.run_spec.name for run in runs]
                href = run_spec_names_to_url(run_spec_names)
            else:
                href = None

            # Render contamination information
            point = self.contamination.get_point(model_name, columns[0][0].name)
            if num_groups == 1 and point is not None:  # display contamination information at the adapter level
                cells = [
                    Cell(display_name + CONTAMINATION_SYMBOLS[point.level], description=point.description, href=href)
                ]
            else:
                cells = [Cell(display_name, description="", href=href)]
            assert len(group_names) == len(matchers)
            for group_name, matcher in zip(group_names, matchers):
                group_runs = [run for run in runs if group_name in run.run_spec.groups]
                # HACK: when looking at aggregate bAbi results (e.g., reasoning), we want to see only the `task: all`
                # version and not the default aggregation across a sparse set of tasks, e.g., `task: {all, 3, 15, 19}`
                if "babi" in group_name and "task:" not in name:
                    group_runs = [run for run in group_runs if "task=all" in run.run_spec.name]

                point = self.contamination.get_point(model_name, group_name)
                if point is not None:
                    description = CONTAMINATION_SYMBOLS[point.level] + " " + point.description
                    contamination_level = point.level
                else:
                    description = ""
                    contamination_level = None

                # HACK: we want to hide stats for the following model-metric combinations:
                # 1. Calibration metrics + AI21/Anthropic
                # 2. MSMARCO metrics + AI21/Anthropic
                hide_value: bool = (
                    model_name in Summarizer.LOGPROBS_ISSUE_MODELS and matcher.name in Summarizer.LOGPROBS_ISSUE_METRICS
                )
                cells.append(
                    self.create_cell(
                        group_runs,
                        matcher,
                        contamination_level,
                        additional_info=description,
                        hide_value=hide_value,
                    )
                )

            rows.append(cells)

        # Link to a page to visualize all runs for comparison.
        # There could be a ton of runs, so only do this if there are 2-5
        # TODO: replace in frontend with a selector to choose which rows to visualize.
        links = []
        if link_to_runs:
            all_run_spec_names = []
            for adapter_spec, runs in adapter_to_runs.items():
                if len(runs) > 1:
                    hlog(
                        f"WARNING: table row corresponding to adapter spec {adapter_spec} has {len(runs)} > 1 runs:"
                        f" {[run.run_spec.name for run in runs]}"
                    )
                for run in runs:
                    all_run_spec_names.append(run.run_spec.name)
            if len(all_run_spec_names) >= 2 and len(all_run_spec_names) <= 5:
                links.append(Hyperlink(text="compare all", href=run_spec_names_to_url(all_run_spec_names)))

        table = Table(title=title, header=header, rows=rows, links=links, name=name)
        if bold_columns:
            for i in range(1, len(header)):
                # TODO: handle lower_is_better in a cleaner way
                lower_is_better = DOWN_ARROW in header[i].value
                values = [float(row[i].value) for row in rows if row[i].value is not None]
                if not values:
                    continue
                best = min(values) if lower_is_better else max(values)
                for row in rows:
                    cell = row[i]
                    if cell.value is not None and cell.value == best:
                        bold_style = cell.style.copy() if cell.style is not None else {}
                        bold_style["font-weight"] = "bold"
                        row[i] = replace(cell, style=bold_style)
        return table

    def create_group_tables_by_metric_group(self, group: RunGroup) -> List[Table]:
        """Creates a list of tables, one for each metric group (e.g., accuracy, robustness).
        Each table has `adapter_spec`s as rows and scenarios or groups as columns."""
        tables: List[Table] = []
        adapter_to_runs: Dict[AdapterSpec, List[Run]] = defaultdict(list)
        all_metric_groups: List[str] = []
        subgroups = self.expand_subgroups(group)
        for subgroup in subgroups:
            all_metric_groups.extend(subgroup.metric_groups)
            for adapter_spec, runs in self.group_adapter_to_runs[subgroup.name].items():
                coarse_adapter_spec = get_coarse_adapter_spec(adapter_spec, adapter_keys_shown=group.adapter_keys_shown)
                filtered_runs = self.filter_runs_by_visibility(runs, group)
                if filtered_runs:
                    adapter_to_runs[coarse_adapter_spec].extend(filtered_runs)
        all_metric_groups = list(dict.fromkeys(all_metric_groups))  # deduplicate while preserving order

        if len(adapter_to_runs) > 0:
            for metric_group in all_metric_groups:
                display_name = self.schema.name_to_metric_group[metric_group].get_short_display_name()
                table = self.create_group_table(
                    name=metric_group,
                    title=display_name,
                    adapter_to_runs=adapter_to_runs,
                    columns=[(subgroup, metric_group) for subgroup in subgroups],
                    link_to_runs=False,
                )
                tables.append(table)
        return tables

    def create_group_tables_by_subgroup(self, group: RunGroup) -> List[Table]:
        """Creates a list of tables, one for each subgroup (e.g., mmlu).
        Each table has coarsened `adapter_spec`s` as rows and metrics as columns."""
        all_tables: List[Table] = []
        subgroups = self.expand_subgroups(group)
        for subgroup in subgroups:
            tables: List[Table] = []
            scenarios_shown = 0
            columns = [(subgroup, metric_group) for metric_group in subgroup.metric_groups]
            # Show the table per scenario
            for scenario_spec in self.group_scenario_adapter_to_runs[subgroup.name]:
                scenario_name = get_scenario_name(subgroup, scenario_spec)
                scenario_display_name = dict_to_str(scenario_spec.args)
                if group.name not in scenario_name:
                    scenario_display_name = f"{subgroup.display_name} {scenario_display_name}"
                adapter_to_runs: Dict[AdapterSpec, List[Run]] = {}
                for adapter_spec, runs in self.group_scenario_adapter_to_runs[group.name][scenario_spec].items():
                    filtered_runs = self.filter_runs_by_visibility(runs, group)
                    coarse_adapter_spec = get_coarse_adapter_spec(adapter_spec, scenario_spec, group.adapter_keys_shown)
                    if filtered_runs:
                        adapter_to_runs[coarse_adapter_spec] = filtered_runs
                if adapter_to_runs and subgroup.metric_groups:
                    table = self.create_group_table(
                        title=scenario_display_name,
                        name=scenario_name,
                        adapter_to_runs=adapter_to_runs,
                        columns=columns,
                        link_to_runs=True,
                    )
                    tables.append(table)
                    scenarios_shown += 1

                    if subgroup.sub_splits is not None:
                        for sub_split in subgroup.sub_splits:
                            table = self.create_group_table(
                                title=f"{subgroup.display_name} (sub-split: {sub_split})",
                                name=f"{subgroup.name}:sub_split={sub_split}",
                                adapter_to_runs=adapter_to_runs,
                                columns=columns,
                                link_to_runs=False,
                                sub_split=sub_split,
                            )
                            tables.append(table)

            if scenarios_shown > 1:  # add aggregate table
                adapter_to_runs = {}
                for adapter_spec, runs in self.group_adapter_to_runs[subgroup.name].items():
                    filtered_runs = self.filter_runs_by_visibility(runs, group)
                    coarse_adapter_spec = get_coarse_adapter_spec(
                        adapter_spec,
                        adapter_keys_shown=group.adapter_keys_shown,
                    )
                    if filtered_runs:
                        adapter_to_runs[coarse_adapter_spec] = filtered_runs
                if adapter_to_runs and subgroup.metric_groups:
                    table = self.create_group_table(
                        title=str(subgroup.display_name),
                        name=subgroup.name,
                        adapter_to_runs=adapter_to_runs,
                        columns=columns,
                        link_to_runs=False,
                    )
                    tables = [table] + tables
            all_tables.extend(tables)

        return all_tables

    def write_groups(self):
        """
        Each group selects out a set of runs.

        For each group, output:
        - Main table (model x columns): each row aggregate over all runs that match the (group, model).
        - Table for each scenario spec.
        """

        # Write out index file with all the groups and basic stats
        write(
            os.path.join(self.run_suite_path, "groups.json"),
            json.dumps(list(map(asdict_without_nones, self.create_index_tables())), indent=2),
        )

        # Write out metadata file for all groups
        write(
            os.path.join(self.run_suite_path, "groups_metadata.json"),
            json.dumps(self.create_groups_metadata(), indent=2),
        )

        # Write out a separate JSON for each group
        groups_path = os.path.join(self.run_suite_path, "groups")
        ensure_directory_exists(groups_path)
        for group in self.schema.run_groups:
            if group.subgroup_display_mode == BY_GROUP or len(self.expand_subgroups(group)) == 1:
                # Create table aggregating over all scenarios in each group and then expand each scenario (we always do
                # this when there are no additional subgroups)
                tables: List[Table] = self.create_group_tables_by_subgroup(group)
            else:
                # Create a table for each metric, showing one subgroup per column for each adapter
                tables: List[Table] = self.create_group_tables_by_metric_group(group)
            if len(tables) == 0:
                continue

            # Output latex and JSON file for each table
            # Add the latex and JSON path as links to each table (mutates the tables!)
            ensure_directory_exists(os.path.join(groups_path, "latex"))
            ensure_directory_exists(os.path.join(groups_path, "json"))
            for table in tables:
                latex_path = os.path.join(groups_path, "latex", f"{group.name}_{table.name}.tex")
                table.links.append(Hyperlink(text="LaTeX", href=latex_path))
                write(latex_path, table_to_latex(table, f"{table.name} ({group.name})"))

                json_path = os.path.join(groups_path, "json", f"{group.name}_{table.name}.json")
                table.links.append(Hyperlink(text="JSON", href=json_path))
                write(json_path, json.dumps(asdict_without_nones(table), indent=2))

            # Write master JSON file
            write(
                os.path.join(groups_path, group.name + ".json"),
                json.dumps(list(map(asdict_without_nones, tables)), indent=2),
            )


@htrack(None)
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output-path", type=str, help="Where the benchmarking output lives", default="benchmark_output"
    )
    parser.add_argument(
        "--suite",
        type=str,
        help="Name of the suite this run belongs to (default is today's date).",
        required=True,
    )
    parser.add_argument("-n", "--num-threads", type=int, help="Max number of threads used to summarize", default=8)
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Display debugging information.",
    )
    parser.add_argument(
        "--skip-slim-per-instance-stats",
        action="store_true",
        help="Don't generate any per-instance stats.",
    )
    args = parser.parse_args()

    # Output JSON files summarizing the benchmark results which will be loaded in the web interface
    summarizer = Summarizer(
        suite=args.suite, output_path=args.output_path, verbose=args.debug, num_threads=args.num_threads
    )
    summarizer.read_runs()
    summarizer.check_metrics_defined()

    summarizer.write_executive_summary()
    summarizer.write_runs()
    summarizer.write_groups()
    summarizer.write_cost_report()
    if not args.skip_slim_per_instance_stats:
        summarizer.write_slim_per_instance_stats()

    hlog("Done.")


if __name__ == "__main__":
    main()
