from __future__ import annotations

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.licenses import LicenseType
from promptware.promptware import PromptConfig, Promptware
from promptware.tasks import TaskType

prompt_config = PromptConfig(
    name="gaokao_essay_writing",
    description="Gaokao English essay writing",
    instruction="",
    demonstration=[
        "Suppose you are Li Hua, teaching your English friend Leslie Chinese."
        " Please write an email with your plans for the next class. The"
        " contents include: 1. Time and place; 2. Content: learning Tang"
        " poetry; 3. Preparation before class: briefly understand the history"
        " of the Tang Dynasty. Here are some requirements: 1. The number of"
        " words is about 100; 2. Details can be added appropriately to make"
        " the writing coherent.\nDear Leslie, I am very happy"
        " that you have made"
        " great progress in learning Chinese and you are interested in Chinese"
        " culture. Now I'll tell you the next learning programme. On July 20,"
        " we are going to learn poems of the Tang Dymasty which"
        " you are interested"
        " in in the Lecture Hall. As a foreign learner, it is difficult for you"
        " to understand the true meaning and the culture of them. Therefore,"
        " before class, you can read some books related to the history of the"
        " Tang Dynasty to better appreciate the poems. Be sure to go to the"
        " Lecture Hall on time. You cannot miss the wonderful poems. Best"
        " wishes. Yours, Li Hua\n",
        "Suppose you are Li Hua, and you want to invite Henry, a"
        " foreign teacher,"
        " to visit the Chinese paper-cutting art exhibition."
        " Please write him an"
        " email, including: 1. Exhibition time and location;"
        " 2. Exhibition content."
        " Here are some requirements: 1. The number of words is about 100; 2."
        " Details can be added appropriately to make the writing"
        " coherent.\nDear"
        " Henry, I'm Li Hua, one of your students in your cultural class. I"
        " know you're interested in one of Chinese traditional"
        " art forms papercutting."
        " So I invite you to attend an exhibition of it. It'll"
        " be held from June 10"
        " to July 10 this year and the opening time is from"
        " 9:00 am to 7:00 pm from"
        " Monday to Saturday and the place of the exhibition"
        " is at the City Gallery,"
        " which is located at 118, Jian Guo Road, Hai Dian District."
        " Shall we go"
        " there together this Friday afternoon? I will meet you at 2:00 pm at"
        " the teaching building gate if you like. You know we Chinese have a"
        " lot of traditional art forms, of which papercutting is one of the"
        " most popular. In the exhibition, you will enjoy many special kinds"
        " of papercuttings. Maybe you can learn one or two"
        " skills of the cutting. Looking forward to your early reply."
        " Regards, Li Hua",
    ],
    prompt_template=lambda input: f"{input['source']}",
    task=TaskType.conditional_generation,
)


class GaokaoEssayWritingPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="gaokao_essay_writing",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.conditional_generation,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-002",
                max_tokens=300,
                temperature=0.0,
            )
        }

    def _software_configs(self):
        return {"gaokao_essay_writing": prompt_config}
