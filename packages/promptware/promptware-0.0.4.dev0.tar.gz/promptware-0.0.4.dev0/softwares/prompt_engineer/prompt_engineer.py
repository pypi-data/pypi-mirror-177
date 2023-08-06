from __future__ import annotations

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.licenses import LicenseType
from promptware.promptware import PromptConfig, Promptware
from promptware.tasks import TaskType
from promptware.utils.logprobs_utils import average_logprobs

prompt_engineer_complete = PromptConfig(
    name="prompt_engineer_complete",
    description="This promptware is used to generate an instruction based "
    "on given input pairs",
    instruction="GPT3 is a good prompt engineer and it can help us to "
    "generate instruction based on input and output pairs.\n",
    demonstration=[
        "I gave a friend an instruction. Based on the instruction they "
        "produced the following input-output pairs:\n\nInput: I love this "
        "movie.\nOutput: positive\n\nInput: The movie is boring.\nOutput: "
        "negative\n\nThe instruction was to  find: the sentiment of the "
        "movie review.\n",
    ],
    prompt_template=lambda input: f"I gave a friend an instruction."
    f" Based on the instruction "
    f"they produced the following input-output p"
    f"airs:\n\n{get_paired_text(input)}\nThe instruction was "
    f"to find:",
    task=TaskType.conditional_generation,
)

prompt_engineer_insert = PromptConfig(
    name="prompt_engineer_insert",
    description="This promptware is used to generate an instruction based "
    "on given input pairs",
    instruction="GPT3 is a good prompt engineer and it can help us to "
    "generate instruction based on input and output pairs.\n",
    demonstration=[
        "I instructed my friend to find the sentiment of the movie review. "
        "The friend read the instruction and wrote an output for "
        "every one of the inputs. "
        "Here are the input-output pairs:\n\nInput: I love this "
        "movie.\nOutput: positive\n\nInput: The movie is boring.\nOutput: "
        "negative\n\nInput: I love this book.\nOutput: positive\n",
    ],
    prompt_template=lambda input: f"I instructed my friend to [INSERT]. "
    f"The friend read the instruction and wrote an output "
    f"for every one of the inputs. "
    f"Here are the input-output pairs:\n\n{get_paired_text(input)}\n",
    task=TaskType.conditional_generation,
)


def get_paired_text(data: list[tuple]) -> str:
    """
    Given a list of tuples, return the text that is paired.

    :param data: A list of tuples.
    :return: The text that is paired.
    """
    if len(data) == 0:
        raise ValueError("No paired data")

    pairs = ""
    for i in range(len(data)):
        if i != len(data) - 1:
            pairs += f"Input:{data[i][0]}\nOutput:{data[i][1]}\n\n"
        else:
            pairs += f"Input:{data[i][0]}\nOutput:{data[i][1]}\n"
    return pairs


class PromptEngineerPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="GPT3 is a good prompt engineer and it can help us to "
            "generate an instruction based on input and output pairs.",
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
                max_tokens=256,
                temperature=0,
                logprobs=1,
                top_p=1,
            )
        }

    def _software_configs(self):
        if self.config_name == "default" or self.config_name == "complete":
            return {"prompt_engineer_complete": prompt_engineer_complete}
        elif self.config_name == "insert":
            return {"prompt_engineer_insert": prompt_engineer_insert}
        else:
            raise ValueError("Unknown prompt engineer type: {self.config_name}")

    def execute(self, input):

        kernel = self.kernel_configs["openai"].to_kernel()

        if self.config_name == "default" or self.config_name == "complete":

            output = kernel.execute(
                input, self.software_configs["prompt_engineer_complete"]
            )
            score = average_logprobs(
                token_logprobs=output["token_logprobs"][1:], tokens=output["tokens"][1:]
            )

            return {
                "text": self.normalize_output(output["text"]),
                "score": score,
            }

        elif self.config_name == "insert":

            output = kernel.execute(
                input, self.software_configs["prompt_engineer_insert"]
            )
            score = average_logprobs(
                token_logprobs=output["token_logprobs"][1:], tokens=output["tokens"][1:]
            )

            return {
                "text": self.normalize_output(output["text"]),
                "score": score,
            }

        else:
            raise ValueError("Unknown prompt engineer type: {self.config_name}")
