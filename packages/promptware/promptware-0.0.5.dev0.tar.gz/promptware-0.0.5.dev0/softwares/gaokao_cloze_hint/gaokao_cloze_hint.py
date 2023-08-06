from __future__ import annotations

import re

from nltk import sent_tokenize

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.licenses import LicenseType
from promptware.promptware import PromptConfig, Promptware
from promptware.tasks import TaskType


def truncate(text, num=512):
    """Keep text length around 512 by default"""
    text_tokens = text.split(" ")
    if len(text_tokens) <= num:
        return text
    total = 0
    sents = sent_tokenize(text)
    final_sents = []
    for i in range(len(sents)):
        if total < num:
            final_sents.append(sents[i])
            total += len(sents[i].split(" "))
        else:
            break
    return " ".join(final_sents)


def normalize_text(text):
    text = re.sub("\n+", " ", text)
    text = re.sub("\t", " ", text)
    text = re.sub(" +", " ", text)
    text = text.encode("ascii", "ignore").decode()
    text = text.strip()
    if len(text) == 0:
        return None
    return text


def preprocess_context(context):
    cont = context.replace("W:", "The woman said:").replace("M:", "The man said:")
    return truncate(normalize_text(cont), 600)


def preprocess_options(options: list[str]):
    options = [f'"{o}"' for o in options]
    return ", ".join(options[:-1]) + " or " + options[-1]


gaokao_cloze_hint = PromptConfig(
    name="gaokao_cloze_hint",
    description="Gaokao English Cloze Hint",
    instruction="",
    demonstration=[
        "There has been a recent trend in the food service industry toward"
        " lower fat content and less salt. This trend, which was started by"
        " the medical community <Q61> a method of fighting heart disease, has"
        " had some unintended side <Q62> such as overweight and heart disease"
        " the very thing the medical community was trying to fight. Fat and"
        " salt are very important parts of a diet. They are required <Q63> the"
        " food that we eat, to recover from injury and for several other bodily"
        " functions. When fat and salt <Q64> from food, the food tastes as if"
        " is missing something. As <Q65> result, people will eat more food to try"
        " to make up for that something missing. Even <Q66>, the amount of fast"
        " food that people eat goes up. Fast food <Q67> full of fat and salt;"
        " by <Q68> more fast food people will get more salt and fat than they"
        " need in their diet. Having enough fat and salt in your meals will reduce"
        " the urge to snack between meals and will improve the taste of your food."
        " However, be <Q69> not to go to extremes. Like anything, it is possible"
        " to have too much of both, <Q70> is not good for the health.\nWhat should"
        " be filled in at the <Q61> position?\nas\n",
        "There has been a recent trend in the food service industry toward"
        " lower fat content and less salt. This trend, which was started by"
        " the medical community as a method of fighting heart disease, has had"
        " some unintended side effects such as overweight and heart disease the"
        " very thing the medical community was trying to fight. Fat and salt"
        " are very important parts of a diet. They are required to process the"
        " food that we eat, to recover from injury and for several other bodily"
        " functions. When fat and salt <Q64> from food, the food tastes as if"
        " is missing something. As <Q65> result, people will eat more food to"
        " try to make up for that something missing. Even <Q66>, the amount of"
        " fast food that people eat goes up. Fast food <Q67> full of fat and"
        " salt; by <Q68> more fast food people will get more salt and fat than they"
        " need in their diet. Having enough fat and salt in your meals will reduce"
        " the urge to snack between meals and will improve the taste of your food."
        " However, be <Q69> not to go to extremes. Like anything, it is possible "
        "to have too much of both, <Q70> is not good for the health.\nWhat should"
        ' be filled in at the <Q64> position given the hint "remove"?\nare removed',
    ],
    prompt_template=lambda input: f"{normalize_text(input['context'])}\n"
    f"What should be filled in at the "
    f"{input['question_mark']} position? given the hint \"{input['hint']}\"?\n",
    task=TaskType.cloze_generative,
)


class GaokaoClozeHintPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Gaokao English Cloze Hint",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.cloze_generative,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-002",
                max_tokens=40,
                temperature=0.0,
            )
        }

    def _software_configs(self):
        return {"gaokao_cloze_hint": gaokao_cloze_hint}
