from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from typing import Optional

from promptware import config
from promptware.tasks import TaskType


@dataclass
class SoftwareInfo:
    description: str
    creator: Optional[str] = None
    homepage: Optional[str] = None
    reference: Optional[str] = None
    codebase_url: Optional[str] = None
    license: Optional[str] = None
    task: Optional[TaskType] = None

    # Set later by the builder
    module_name: Optional[str] = None
    config_name: Optional[str] = None
    kernel_configs: Optional[dict] = None
    software_configs: Optional[dict] = None

    def serialize(self):
        return {
            "description": self.description,
            "creator": self.creator,
            "homepage": self.homepage,
            "reference": self.reference,
            "codebase_url": self.codebase_url,
            "license": self.license,
            "task": self.task,
            "module_name": self.module_name,
            "config_name": self.config_name,
            "kernel_configs": {
                config_name: asdict(config)
                for config_name, config in self.kernel_configs.items()
            },
            "software_configs": {
                config_name: config.serialize()
                for config_name, config in self.software_configs.items()
            },
        }

    def write_to_directory(
        self,
        path_directory,
        file_name: Optional[str] = None,
        overwrite: bool = True,
    ):

        software_info = self.serialize()

        file_name = (
            file_name if file_name is not None else config.SOFTWARE_INFO_FILENAME
        )
        file_path = os.path.join(path_directory, file_name)

        # Checks the directory.
        if os.path.exists(path_directory):
            if not os.path.isdir(path_directory):
                raise RuntimeError(f"Not a directory: {path_directory}")
        else:
            os.makedirs(path_directory)

        # Checks the file.
        if os.path.exists(file_path):
            if not os.path.isfile(file_path):
                raise RuntimeError(f"Not a file: {file_path}")
            if not overwrite:
                raise RuntimeError(
                    f"Attempted to overwrite the existing file: {file_path}"
                )

        with open(file_path, "w") as f:
            # save dict as json file
            json.dump(software_info, f, indent=4)

        return file_path
