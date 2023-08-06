from typing import List

from helm.benchmark.scenarios.scenario import Instance, Reference

from .data_augmenter import DataAugmenter
from .extra_space_perturbation import ExtraSpacePerturbation
from .misspelling_perturbation import MisspellingPerturbation
from .contraction_expansion_perturbation import ContractionPerturbation, ExpansionPerturbation
from .typos_perturbation import TyposPerturbation
from .filler_words_perturbation import FillerWordsPerturbation
from .synonym_perturbation import SynonymPerturbation
from .lowercase_perturbation import LowerCasePerturbation
from .space_perturbation import SpacePerturbation
from .dialect_perturbation import DialectPerturbation
from .person_name_perturbation import PersonNamePerturbation
from .gender_perturbation import GenderPerturbation


def test_extra_space_perturbation():
    data_augmenter = DataAugmenter(perturbations=[ExtraSpacePerturbation(num_spaces=2)])
    instance: Instance = Instance(
        id="id0", input="Hello my name is", references=[Reference(output="some name", tags=[])]
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    assert len(instances) == 2
    assert instances[1].id == "id0"
    assert instances[1].perturbation.name == "extra_space"
    assert instances[1].perturbation.num_spaces == 2
    assert instances[1].input == "Hello  my  name  is"
    assert instances[1].references[0].output == "some name"


def test_misspelling_perturbation():
    data_augmenter = DataAugmenter(perturbations=[MisspellingPerturbation(prob=1.0)])
    instance: Instance = Instance(
        id="id0",
        input="Already, the new product is not available.",
        references=[],
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    assert len(instances) == 2
    assert instances[1].id == "id0"
    assert instances[1].perturbation.name == "misspellings"
    assert instances[1].perturbation.prob == 1.0
    assert instances[1].input == "Alreayd, hten new product is nto avaliable."


def test_filler_words_perturbation():
    data_augmenter = DataAugmenter(perturbations=[FillerWordsPerturbation(insert_prob=0.3, speaker_ph=False)])
    instance: Instance = Instance(
        id="id0",
        input="The quick brown fox jumps over the lazy dog.",
        references=[Reference(output="The quick brown fox jumps over the lazy dog.", tags=[])],
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    assert len(instances) == 2
    assert instances[1].id == "id0"
    assert instances[1].perturbation.name == "filler_words"
    assert instances[1].input == "The quick brown fox jumps over like the lazy probably dog."


def test_contraction_perturbation():
    data_augmenter = DataAugmenter(perturbations=[ContractionPerturbation()])
    instance: Instance = Instance(
        id="id0", input="She is a doctor, and I am a student", references=[Reference(output="he is a teacher", tags=[])]
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    assert len(instances) == 2
    assert instances[1].id == "id0"
    assert instances[1].perturbation.name == "contraction"
    assert instances[1].input == "She's a doctor, and I'm a student"
    assert instances[1].references[0].output == "he is a teacher"


def test_expansion_perturbation():
    data_augmenter = DataAugmenter(perturbations=[ExpansionPerturbation()])
    instance: Instance = Instance(
        id="id0", input="She's a doctor, and I'm a student", references=[Reference(output="he's a teacher", tags=[])]
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    assert len(instances) == 2
    assert instances[1].id == "id0"
    assert instances[1].perturbation.name == "expansion"
    assert instances[1].input == "She is a doctor, and I am a student"
    assert instances[1].references[0].output == "he's a teacher"


def test_typos_perturbation():
    data_augmenter = DataAugmenter(perturbations=[TyposPerturbation(prob=0.1)])
    instance: Instance = Instance(
        id="id0",
        input="After their marriage, she started a close collaboration with Karvelas.",
        references=[],
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    assert len(instances) == 2
    assert instances[1].perturbation.name == "typos"
    assert instances[1].perturbation.prob == 0.1
    assert instances[1].input == "After tjeir marriage, she xrwrted a cloae dollabpration with Iarvwlas."


def test_synonym_perturbation():
    data_augmenter = DataAugmenter(perturbations=[SynonymPerturbation(prob=1.0)])
    instance: Instance = Instance(
        id="id0",
        input="This was a good movie, would watch again.",
        references=[],
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    assert len(instances) == 2
    assert instances[1].perturbation.name == "synonym"
    assert instances[1].perturbation.prob == 1.0
    assert instances[1].input == "This was a near motion-picture show, would check once more."


def test_lowercase_perturbation():
    data_augmenter = DataAugmenter(perturbations=[LowerCasePerturbation()])
    instance: Instance = Instance(
        id="id0",
        input="Hello World!\nQuite a day, huh?",
        references=[Reference(output="Yes!", tags=[])],
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    assert len(instances) == 2
    assert instances[1].perturbation.name == "lowercase"
    assert instances[1].input == "hello world!\nquite a day, huh?"
    assert instances[1].references[0].output == "Yes!"


def test_space_perturbation():
    data_augmenter = DataAugmenter(perturbations=[SpacePerturbation(max_spaces=3)])
    instance: Instance = Instance(id="id0", input="Hello World!\nQuite a day, huh?", references=[])
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    print(instances)
    assert len(instances) == 2
    assert instances[1].perturbation.name == "space"
    assert instances[1].input == "Hello   World!\nQuite a  day,   huh?"


def test_dialect_perturbation():
    data_augmenter = DataAugmenter(
        perturbations=[DialectPerturbation(prob=1.0, source_class="SAE", target_class="AAVE")],
    )
    instance: Instance = Instance(
        id="id0",
        input="I will remember this day to be the best day of my life.",
        references=[Reference(output="Is this love?", tags=[])],
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    print(instances)
    assert len(instances) == 2
    assert instances[1].perturbation.name == "dialect"
    assert instances[1].input == "I gon remember dis day to b the best day of mah life."
    assert instances[1].references[0].output == "Is dis love?"


def test_person_name_perturbation():
    data_augmenter = DataAugmenter(
        perturbations=[
            PersonNamePerturbation(
                prob=1.0,
                source_class={"race": "white_american"},
                target_class={"race": "black_american"},
                person_name_type="first_name",
                preserve_gender=True,
            )
        ],
    )
    instance: Instance = Instance(
        id="id0",
        input="I learned that Jack, Peter, and Lauren are siblings! Do you know who is the oldest?",
        references=[Reference(output="Peter and peter were friends.", tags=[])],
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    print(instances)
    assert len(instances) == 2
    assert instances[1].perturbation.name == "person_name"
    assert instances[1].input == "I learned that Lamar, Tyree, and Sharise are siblings! Do you know who is the oldest?"
    assert instances[1].references[0].output == "Tyree and tyree were friends."


def test_gender_pronoun_perturbation():
    data_augmenter = DataAugmenter(
        perturbations=[GenderPerturbation(prob=1.0, mode="pronouns", source_class="male", target_class="female")],
    )
    instance: Instance = Instance(
        id="id0",
        input="Did she mention that he was coming with his parents and their friends?",
        references=[Reference(output="She didn't, perhaps he didn't tell her!", tags=[])],
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    print(instances)
    assert len(instances) == 2
    assert instances[1].perturbation.mode == "pronouns"
    assert instances[1].input == "Did she mention that she was coming with her parents and their friends?"
    assert instances[1].references[0].output == "She didn't, perhaps she didn't tell her!"


def test_gender_term_perturbation():
    data_augmenter = DataAugmenter(
        perturbations=[GenderPerturbation(prob=1.0, mode="terms", source_class="male", target_class="female")],
    )
    instance: Instance = Instance(
        id="id0",
        input="His grandsons looked a lot like their dad.",
        references=[Reference(output="How did their father look like?", tags=[])],
    )
    instances: List[Instance] = data_augmenter.generate([instance], include_original=True)

    print(instances)
    assert len(instances) == 2
    assert instances[1].perturbation.mode == "terms"
    assert instances[1].input == "His granddaughters looked a lot like their mom."
    assert instances[1].references[0].output == "How did their mother look like?"
