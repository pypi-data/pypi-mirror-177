from __future__ import annotations

from promptware.info import SoftwareInfo
from promptware.kernels.plm import PLMKernelConfig
from promptware.kernels.python import PythonKernelConfig
from promptware.licenses import LicenseType
from promptware.promptware import PromptConfig, Promptware
from promptware.tasks import TaskType

instruction = """
You are GPT-3, and you can't do math.
You can do basic math, and your memorization abilities are impressive. If anyone gives
 you a hard math problem, just use this format and we’ll take care of the rest:
Question: ${{Question with hard calculation.}}
```python
${{Code that prints what you need to know}}
```
"""

demonstration = """
Question: What is 37593 * 67?
```python
result = 37593 * 67
```
"""


def isfloat(num: str):
    try:
        float(num)
        return True
    except ValueError:
        return False


math_calculation = PromptConfig(
    name="math_calculation",
    description="math calculation",
    instruction=instruction,
    demonstration=[demonstration],
    prompt_template=lambda input: f"Question: {input['question']}",
    task=TaskType.others,
)


class MathCalculationPromptware(Promptware):
    def _info(self) -> SoftwareInfo:
        return SoftwareInfo(
            description="math calculation",
            creator="Promptware Authors",
            homepage="https://github.com/expressai/promptware",
            reference="",
            codebase_url="https://github.com/expressai/promptware/tree/main/softwares",
            license=LicenseType.apache_2_0,
            task=TaskType.others,
        )

    def _kernel_configs(self):
        return {
            "openai": PLMKernelConfig(
                platform="openai",
                model_name="text-davinci-002",
                max_tokens=512,
                temperature=0,
            ),
            "python": PythonKernelConfig(version=3.9),
        }

    def _software_configs(self):
        return {"math_calculation": math_calculation}

    def execute(self, input):

        openai_kernel = self.kernel_configs["openai"].to_kernel()
        python_kernel = self.kernel_configs["python"].to_kernel()

        result = openai_kernel.execute(input, self.software_configs["math_calculation"])
        result = result.strip()
        if result.startswith("```python"):
            return python_kernel.execute(result[9:-4])
        elif isfloat(result):
            return result
        else:
            raise ValueError(f"Illegal python code: {result}")
