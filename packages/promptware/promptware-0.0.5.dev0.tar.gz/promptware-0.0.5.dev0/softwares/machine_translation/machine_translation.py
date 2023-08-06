from __future__ import annotations

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.licenses import LicenseType
from promptware.promptware import PromptConfig, Promptware
from promptware.tasks import TaskType

machine_translation_enzh = PromptConfig(
    name="machine_translation_enzh",
    description="Machine translation from English to Chinese.",
    instruction="Translate this into Chinese:",
    demonstration=[
        "He knew how to manipulate the media. He knew exactly"
        " how to get the"
        " front page, Fiddes, who was Jackson's bodyguard for 10 years, "
        'said. "90 per cent of the time it worked, by putting'
        " a mask on his face,"
        " or sticky tape on his hands - or tape on his nose"
        " was a favourite one."
        " He would say he wanted his life to be the greatest"
        " mystery on Earth.\n"
        "他知道如何操纵媒体。他完全知道如何登上头条新闻，做了杰克逊 10 "
        "年保镖的菲德斯说道。脸上戴上口罩，或者用胶带粘在手上，或者用"
        "胶带粘在鼻子上"
        "（这个他最喜欢做），在 90% 的情况下，这种方法很奏效。他会说，"
        "他希望自己的一生成为全球最大的谜。”\n",
        "The country is also developing historic sites such as"
        " the  centuries-old"
        " Mada'in Saleh, home to sandstone tombs of the same"
        " civilisation which"
        " built the Jordanian city of Petra.\n"
        "该国还正在开发历史遗迹，如有着数百年历史的玛甸沙勒，这里是与建造约旦佩特"
        "拉城的同一文明遗留下来的砂岩陵墓所在地。\n",
    ],
    prompt_template=lambda input: f"{input['translation']['en']}",
    task=TaskType.machine_translation,
)

machine_translation_zhen = PromptConfig(
    name="machine_translation_zhen",
    description="Machine translation from Chinese to English.",
    instruction="Translate this into English:",
    demonstration=[
        "他知道如何操纵媒体。他完全知道如何登上头条新闻，做了杰克逊 10 "
        "年保镖的菲德斯说道。脸上戴上口罩，或者用胶带粘在手上，或者用"
        "胶带粘在鼻子上"
        "（这个他最喜欢做），在 90% 的情况下，这种方法很奏效。他会说，"
        "他希望自己的一生成为全球最大的谜。”\n",
        "He knew how to manipulate the media. He knew exactly"
        " how to get the"
        " front page, Fiddes, who was Jackson's bodyguard for 10 years, "
        'said. "90 per cent of the time it worked, by putting'
        " a mask on his face,"
        " or sticky tape on his hands - or tape on his nose"
        " was a favourite one."
        " He would say he wanted his life to be the greatest"
        " mystery on Earth.\n"
        "该国还正在开发历史遗迹，如有着数百年历史的玛甸沙勒，这里是与建造约旦佩特"
        "拉城的同一文明遗留下来的砂岩陵墓所在地。\n",
        "The country is also developing historic sites such as"
        " the  centuries-old"
        " Mada'in Saleh, home to sandstone tombs of the same"
        " civilisation which"
        " built the Jordanian city of Petra.\n",
    ],
    prompt_template=lambda input: f"{input['translation']['zh']}",
    task=TaskType.machine_translation,
)


class MachineTranslationPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="Machine translation from English to Chinese.",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.machine_translation,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=64,
                temperature=0,
            )
        }

    def _software_configs(self):
        if self.config_name == "default" or "enzh":
            return {"machine_translation_enzh": machine_translation_enzh}
        elif self.config_name == "zhen":
            return {"machine_translation_zhen": machine_translation_zhen}
        else:
            raise ValueError("Unknown language pair: {self.config_name}")
