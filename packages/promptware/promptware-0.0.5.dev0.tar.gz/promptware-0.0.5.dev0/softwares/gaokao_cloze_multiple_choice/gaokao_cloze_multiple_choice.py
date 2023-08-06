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


gaokao_cloze_multiple_choice = PromptConfig(
    name="gaokao_cloze_multiple_choice",
    description="Gaokao English Cloze Multiple Choice",
    instruction="",
    demonstration=[
        "If anyone had told me three years ago that I would be spending"
        " most of my weekends camping. I would have laughed heartily. Campers,"
        " in my eyes, were people who enjoyed insects bites, ill-cooked meals,"
        " and uncomfortable sleeping bags. They had nothing in common with"
        " me. <Q36> The friends who introduced me to camping thought that it"
        " meant to be a pioneer. <Q37> We sleep in a tent, cooked over an open"
        " fire, and walked a long distance to take the shower and use the"
        " bathroom. This brief visit with Mother Nature cost me two days off"
        " from work, recovering from a bad case of sunburn and the doctor's bill"
        " for my son's food poisoning. I was, nevertheless, talked into going"
        " on another fun-filled holiday in the wilderness. <Q38> Instead,"
        " we had a pop-up camper with comfortable beds and an air conditioner."
        " My nature-loving friends had remembered to bring all the necessities"
        " of life. <Q39> We have done a lot of it since. Recently, we bought a"
        " twenty-eight-foot travel trailer complete with a bathroom and a"
        " built-in TV set. There is a separate bedroom, a modern kitchen"
        " with a refrigerator. The trailer even has matching carpet and"
        " curtains. <Q40> It must be true that sooner or later, everyone"
        " finds his or her way back to nature. I recommend that you find"
        " your way in style. \nWhat should be filled in at the <Q36>"
        ' position? "This time there was no tent.", "Things are going'
        ' to be improved.", "The trip they took me on was a rough'
        ' one.", "I was to learn a lot about camping since then,'
        ' however.", "I must say that I have certainly come to enjoy'
        ' camping.", "After the trip, my family became quite interested'
        ' in camping." or "There was no shade as the trees were no more'
        ' than 3 feet tall."?\nI was to learn a lot about camping since'
        " then, however.\n",
        "If anyone had told me three years ago that I would be spending most"
        " of my weekends camping. I would have laughed heartily. Campers, in my"
        " eyes, were people who enjoyed insects bites, ill-cooked meals, and"
        " uncomfortable sleeping bags. They had nothing in common with me. I"
        " was to learn a lot about camping since then, however. The friends"
        " who introduced me to camping thought that it meant to be a pioneer."
        " The trip they took me on was a rough one. We sleep in a tent, cooked"
        " over an open fire, and walked a long distance to take the shower and"
        " use the bathroom. This brief visit with Mother Nature cost me two "
        "days off from work, recovering from a bad case of sunburn and the"
        " doctor's bill for my son's food poisoning. I was, nevertheless,"
        " talked into going on another fun-filled holiday in the wilderness."
        " <Q38> Instead, we had a pop-up camper with comfortable beds and"
        " an air conditioner. My nature-loving friends had remembered to"
        " bring all the necessities of life. <Q39> We have done a lot of"
        " it since. Recently, we bought a twenty-eight-foot travel trailer"
        " complete with a bathroom and a built-in TV set. There is a separate"
        " bedroom, a modern kitchen with a refrigerator. The trailer even has"
        " matching carpet and curtains. <Q40> It must be true that sooner or"
        " later, everyone finds his or her way back to nature. I recommend that"
        " you find your way in style. \nWhat should be filled in at the <Q38>"
        ' position? "This time there was no tent.", "Things are going to'
        ' be improved.", "The trip they took me on was a rough one.", "I'
        ' was to learn a lot about camping since then, however.", "I must'
        ' say that I have certainly come to enjoy camping.", "After the'
        ' trip, my family became quite interested in camping." or "There'
        ' was no shade as the trees were no more than 3 feet tall."?\nThis'
        " time there was no tent.\n",
    ],
    prompt_template=lambda input: f"{normalize_text(input['context'])}\n"
    f"What should be filled in at the "
    f"{input['question_mark']} position? {preprocess_options(input['options'])}?\n",
    task=TaskType.cloze_mutiple_choice,
)


class GaokaoClozeMultipleChoicePromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="gaokao_cloze_multiple_choice",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.cloze_mutiple_choice,
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
        return {"gaokao_cloze_multiple_choice": gaokao_cloze_multiple_choice}
