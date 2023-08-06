from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional

import cohere
import openai

import promptware
from promptware.kernels.kernel import Kernel, KernelConfig


@dataclass
class PLMKernelConfig(KernelConfig):
    platform: str
    model_name: str
    max_tokens: int
    temperature: float
    top_p: float = 1
    suffix: str = ""
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    logprobs: float = 1
    n: int = 1
    echo: bool = False

    def to_kernel(self) -> Kernel:
        return PLMKernel(self)


class PLMKernel(Kernel):
    def __init__(self, config: Optional[PLMKernelConfig] = None):

        self.config = (
            config
            if config is not None
            else PLMKernelConfig(
                platform="openai",
                model_name="text-curie-001",
                suffix="",
                temperature=0,
                max_tokens=10,
                logprobs=1,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                n=1,
                echo=False,
            )
        )

    def get_instantiated_instruction(
        self, input: dict, instruction: str | Callable[[Any], str]
    ) -> str:
        return instruction if not callable(instruction) else instruction(input)

    def get_instantiated_prompt(self, input: dict, prompt: Callable[[Any], str]) -> str:
        """

        Args:
            input: the input with the original format that software need to process

        Returns:
            the input with format specified by prompt_template

        """

        return prompt(input)

    def initial_code(self, input: dict, software_config) -> str:
        """

        Args:
            input: the input with the original format that software need to process

        Returns:
            the combined information of promptware's instruction, prompted input
             and demonstration

        """
        delimiter = "\n"
        instantiated_instruction = (
            self.get_instantiated_instruction(input, software_config.instruction)
            + delimiter
            if software_config.instruction != ""
            else ""
        )

        demonstration = (
            "\n".join(software_config.demonstration) + delimiter
            if software_config.demonstration is not None
            else ""
        )

        instantiated_prompt = self.get_instantiated_prompt(
            input, software_config.prompt_template
        )

        result = instantiated_instruction + demonstration + instantiated_prompt
        return result

    def execute(self, input: Any, software_config) -> dict[str, str]:

        initial_code = self.initial_code(input, software_config)
        # print(initial_code)
        if self.config.platform == "openai":
            openai.api_key = promptware.os_api_key
            if initial_code.find("[INSERT]") == -1:
                response = openai.Completion.create(
                    model=self.config.model_name,
                    prompt=initial_code,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    frequency_penalty=self.config.frequency_penalty,
                    presence_penalty=self.config.presence_penalty,
                    logprobs=self.config.logprobs,
                    n=self.config.n,
                    echo=self.config.echo,
                )
            else:
                prefix = initial_code.split("[INSERT]")[0]
                suffix = initial_code.split("[INSERT]")[1]
                response = openai.Completion.create(
                    model=self.config.model_name,
                    prompt=prefix,
                    suffix=suffix,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    frequency_penalty=self.config.frequency_penalty,
                    presence_penalty=self.config.presence_penalty,
                    logprobs=self.config.logprobs,
                    n=self.config.n,
                    echo=self.config.echo,
                )

            out = {
                "text": response["choices"][0]["text"],
                "token_logprobs": response["choices"][0]["logprobs"]["token_logprobs"],
                "tokens": response["choices"][0]["logprobs"]["tokens"],
            }

        elif self.config.platform == "cohere":
            co = cohere.Client(promptware.os_api_key)
            response = co.generate(
                model=self.config.model_name,
                prompt=initial_code,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                k=0,
                p=0.75,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
                stop_sequences=[],
                return_likelihoods="NONE",
            )
            out = {
                "text": response.generations[0].text,
                "token_logprobs": None,
                "tokens": None,
            }

        #
        # output = self.normalize_output(out)

        return out
