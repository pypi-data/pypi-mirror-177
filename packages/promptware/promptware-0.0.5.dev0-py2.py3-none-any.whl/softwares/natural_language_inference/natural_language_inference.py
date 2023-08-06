from __future__ import annotations

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.licenses import LicenseType
from promptware.promptware import PromptConfig, Promptware
from promptware.tasks import TaskType


class NaturalLanguageInferencePromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="This promptware is used to identify the semantic"
            " relationship between",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.text_pair_classification,
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
            "sentiment_classification": PromptConfig(
                name="natural_language_inference",
                description="This promptware is used to identify the semantic"
                " relationship between"
                " two sentences",
                instruction="Give two sentences, predict which of the following"
                " categories their"
                " relationship falls into: entailment, contradiction, neutral",
                demonstration=[
                    "A person on a horse jumps over a broken down airplane.\t"
                    "A person is training his horse for a competition.\nneutral",
                    "A person on a horse jumps over a broken down airplane.\t"
                    "A person is outdoors, on a horse.\nentailment",
                    "Children smiling and waving at camera\tThe kids are"
                    " frowning.\ncontradiction",
                ],
                prompt_template=lambda input: f"{input['text1']}\t{input['text2']}",
                task=TaskType.text_pair_classification,
            )
        }
