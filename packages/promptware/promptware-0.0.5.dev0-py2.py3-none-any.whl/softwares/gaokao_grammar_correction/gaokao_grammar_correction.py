from __future__ import annotations

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.licenses import LicenseType
from promptware.promptware import PromptConfig, Promptware
from promptware.tasks import TaskType

prompt_config = PromptConfig(
    name="gaokao_grammar_correction",
    description="Gaokao English Grammar Correction",
    instruction="",
    demonstration=[
        "In the summer holiday following my eighteen birthday,"
        " I took driving lessons. I still remember how hard first day was."
        " Before getting into the car, I thought I had learned the instructor's"
        " orders, so once I started the car, my mind goes blank, I forgot what"
        " he had said to me altogether. The instructor kept repeating the word,"
        ' "Speed up!" "Slow down!" "Turning left!" I was so much nervous that'
        " I could hardly tell which direction was left. A few minutes late, the"
        " instructor asked me to stop the car. It was a relief and I came to a"
        " suddenly stop just in the middle on the road.\nPlease fix"
        " the grammatical"
        " errors in the above paragraph.\nIn the summer holiday following my"
        " eighteenth birthday, I took driving lessons. I still remember how"
        " hard the first day was. Before getting into the car, I thought I had"
        " learned the instructor's orders, but once I started the car, my mind"
        " went blank, I forgot what he had said to me altogether."
        " The instructor"
        ' kept repeating the words, "Speed up!" "Slow down!" "Turn left!" I'
        " was so nervous that I could hardly tell which direction was left."
        " A few minutes later, the instructor asked me to stop"
        " the car. It was a relief and I came to a sudden stop just in the"
        " middle on the road.\n",
        "Mr. and Mrs. Zhang all work in our school. They live far from the"
        " school, and it takes them about a hour and a half to go to"
        " work every day."
        " In their spare time, they are interesting in planting vegetables"
        " in their garden, that is on the rooftop of their house. They often"
        " get up earlier and water the vegetables together. They have"
        " also bought"
        " for some gardening tools. Beside, they often get some useful"
        " informations"
        " from the Internet. When summer came, they will invite their students"
        " pick the fresh vegetables!\nPlease fix the grammatical errors in"
        " the above paragraph.\nMr. and Mrs. Zhang both work in our school."
        " They live far from the school, and it takes them about an hour and"
        " a half to go to work every day. In their spare time, they"
        " are interested"
        " in planting vegetables in their garden, which is on the rooftop of"
        " their house. They often get up early and water the vegetables"
        " together."
        " They have also bought some gardening tools. Besides, they often get"
        " some useful information from the Internet. When summer"
        " comes, they will"
        " invite their students to pick the fresh vegetables!\n",
    ],
    prompt_template=lambda input: f"{input['text']}\nPlease fix the"
    f" grammatical errors in the"
    f" above paragraph.\n",
    task=TaskType.grammatical_error_correction,
)


class GaokaoGrammarCorrectionPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Gaokao English Grammar Correction",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.grammatical_error_correction,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-002",
                max_tokens=200,
                temperature=0.0,
            )
        }

    def _software_configs(self):
        return {"gaokao_grammar_correction": prompt_config}
