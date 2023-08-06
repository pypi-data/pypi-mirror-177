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


gaokao_reading_comprehension = PromptConfig(
    name="gaokao_reading_comprehension",
    description="Gaokao English Reading Comprehension",
    instruction="",
    demonstration=[
        "I work with Volunteers for Wildlife, a rescue and education"
        " organization at Bailey Arboretum in Locust Valley. Trying to help"
        " injured, displaced or sick creatures can be heartbreaking; survival is"
        " never certain. However, when it works, it is simply beautiful."
        " I got a rescue call from a woman in Muttontown. She had found"
        " a young owl on the ground. When I arrived, I saw a 2-to 3-week-old owl."
        " It had already been placed in a carrier for safety. I examined the chick"
        " and it seemed fine. If I could locate the nest, I might have been able to"
        " put it back, but no luck. My next work was to construct a nest and anchor"
        " it in a tree. The homeowner was very helpful. A wire basket was found."
        " I put some pine branches into the basket to make this nest safe and"
        " comfortable. I placed the chick in the nest, and it quickly calmed"
        " down. Now all that was needed were the parents, but they were absent."
        " I gave the homeowner a recording of the hunger screams of owl chicks."
        " These advertise the presence of chicks to adults; they might also"
        " encourage our chick to start calling as well. I gave the owner as much"
        " information as possible and headed home to see what news the night"
        " might bring. A nervous night to be sure, but sometimes the spirits"
        " of nature smile on us all! The homeowner called to say that the parents"
        " had responded to the recordings. I drove over and saw the chick in the"
        " nest looking healthy and active. And it was accompanied in the nest by"
        " the greatest sight of all — LUNCH! The parents had done their duty and"
        " would probably continue to do so.\nWhat is unavoidable in the author's"
        ' rescue work according to paragraph 1? "Efforts made in vain.", "Getting'
        ' injured in his work.", "Feeling uncertain about his'
        ' future." or "Creatures forced out of their homes."?\nEfforts'
        " made in vain.\n",
        "Some of the world's most famous musicians recently gathered in"
        " Paris and New Orleans to celebrate the first annual International"
        " Jazz Day. UNESCO (United Nations Educational, Scientific and"
        " Cultural Organization) recently set April 30 as a day to raise"
        " awareness of jazz music, its significance, and its potential as"
        " a unifying voice across cultures. Despite the celebrations, though"
        ", in the U.S. the jazz audience continues to shrink and grow older,"
        " and the music has failed to connect with younger generations."
        " It's Jason Moran's job to help change that. As the Kennedy Center's"
        " artistic adviser for jazz, Moran hopes to widen the audience for jazz,"
        " make the music more accessible, and preserve its history and"
        " culture. \"Jazz seems like it's not really a part of the American"
        " appetite,\" Moran tells National Public Radio's reporter Neal"
        " Conan. \"What I'm hoping to accomplish is that mu generation and younger"
        " start to reconsider and understand that jazz is not black and write"
        " anymore. It's actually color, and it's actually digital.\" Moran says"
        " one of the problems with jazz today is that the entertainment aspect of"
        " the music has been lost. \"The music can't be presented today the way"
        " it was in 1908 or 1958. It has to continue to move, because the way the"
        ' world works is not the same," says Moran. Last year, Moran worked on'
        " a project that arranged Fats Waller's music for a dance party, \"Just"
        " to kind of put it back in the mind that Waller is dance music as much as"
        ' it is concert music," says Moran. "For me, it\'s the recontextualization.'
        " In music, where does the emotion lie? Are we, as abstract as a Charlie"
        " Parker record gets us into a dialogue about our emotions and our"
        " thoughts? Sometimes we lose sight that the music has a wider"
        ' context," says Moran, "So I want to continue those dialogue. Those'
        ' are the things I want to foster."\nWhy did UNESCO set April 30 as'
        ' International Jazz Day? "To remember the birth of jazz.", "To protect'
        ' cultural diversity.", "To encourage people to study music." or "To'
        ' recognize the value of jazz."?\nTo recognize the value of jazz.\n',
    ],
    prompt_template=lambda input: f"{preprocess_context(input['context'])}\n"
    f"{input['question']} "
    f"{preprocess_options(input['options'])}?",
    task=TaskType.qa_multiple_choice,
)


class GaokaoReadingComprehensionPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="gaokao_reading_comprehension",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.qa_multiple_choice,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-002",
                max_tokens=20,
                temperature=0.0,
            )
        }

    def _software_configs(self):
        return {"gaokao_reading_comprehension": gaokao_reading_comprehension}
