from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.software import Software, SoftwareConfig
from promptware.tasks import TaskType
from promptware.utils.naming import camelcase_to_snakecase
from promptware.utils.prompt_utils import get_template


@dataclass
class DataLabConfig:
    dataset_name: str
    sub_dataset: Optional[str] = None
    split_name: str = "test"
    n_samples: int = 3


@dataclass
class PromptConfig(SoftwareConfig):
    # Name
    name: str
    # Describe what the promptware is designed for
    description: str
    # Instruction text of promptware
    instruction: str | Callable[[Any], str]
    # Demonstration of promptware
    demonstration: Optional[list[str]]
    # Prompt template defines how a user's input will be formatted
    prompt_template: Callable[[Any], str]
    # The most appropriate tasks that the promptware could be applied to
    task: TaskType

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "instruction": self.instruction
            if not callable(self.instruction)
            else get_template(self.instruction),
            "demonstration": self.demonstration,
            "prompt_template": get_template(self.prompt_template),
            "task": self.task,
        }


class Promptware(Software):
    def __init__(
        self,
        config_name: Optional[str] = None,
    ):

        self.config_name = config_name or "default"
        self.info = self._info()

        self.kernel_configs = self._kernel_configs()
        self.software_configs = self._software_configs()
        # Set other values for info
        self.info.module_name = camelcase_to_snakecase(self.__class__.__name__)
        self.info.config_name = self.config_name
        self.info.kernel_configs = self.kernel_configs
        self.info.software_configs = self.software_configs

    def _info(self) -> SoftwareInfo:
        raise NotImplementedError

    def _kernel_configs(self) -> dict[str, PLMKernelConfig]:
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                max_tokens=64,
                temperature=0,
            )
        }

    def normalize_output(self, output: str) -> str:
        return output.strip()

    def _software_configs(self) -> dict[str, SoftwareConfig]:
        raise NotImplementedError

    def evaluate(self):
        ...

    def execute(self, input):

        kernel = self.kernel_configs["openai"].to_kernel()
        first_software_config = list(self.software_configs.values())[0]
        output = kernel.execute(input, first_software_config)

        result = self.normalize_output(output["text"])

        return result

    def infer_batch_samples(self, samples: list[dict]):
        """

        Args:
            samples: evaluated samples

        Returns:
            predictions

        """
        predictions = []
        # Create a promptware
        for sample in samples:
            result = self.execute(sample)
            predictions.append(result)
        return predictions
