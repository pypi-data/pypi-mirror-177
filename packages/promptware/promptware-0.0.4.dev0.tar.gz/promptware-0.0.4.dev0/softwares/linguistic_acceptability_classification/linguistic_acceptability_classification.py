from __future__ import annotations

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.licenses import LicenseType
from promptware.promptware import PromptConfig, Promptware
from promptware.tasks import TaskType


class LinguisticAcceptabilityClassificationPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to identify whether a"
            " sentence is a grammatical English sentence based on some learning"
            " samples from the cola dataset.",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.text_classification,
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
        return {
            "linguistic_acceptability_classification": PromptConfig(
                name="linguistic_acceptability_classification",
                description="This promptware is used to identify whether a"
                " sentence is a grammatical English sentence based on some learning"
                " samples from the cola dataset.",
                instruction="Is the following sentence a grammatical English sentence?",
                demonstration=[
                    "They drank the pub.\nno",
                    "When Bill smokes, all the more does Susan hate him.\nyes",
                ],
                prompt_template=lambda input: f"{input['text']}",
                task=TaskType.text_classification,
            )
        }
