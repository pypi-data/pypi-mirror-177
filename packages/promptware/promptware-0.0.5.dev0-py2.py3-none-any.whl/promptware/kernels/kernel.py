from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import Any, Optional

from promptware.software import SoftwareConfig


@dataclass
class KernelConfig:
    @abc.abstractmethod
    def to_kernel(self) -> Kernel:
        return Kernel(self)


class Kernel:
    def __init__(self, config: KernelConfig):
        self.config = config

    def execute(
        self, input: Any, software_config: Optional[SoftwareConfig] = None
    ) -> Any:
        ...
