from typing import Optional, Union
from ..types.Reference import Reference
import subprocess


class EditableSubCommand:
    # noinspection PyMethodMayBeStatic
    def add(self, path: str, reference: Union[str, Reference], layout: Optional[str] = None):
        if isinstance(reference, Reference):
            reference = str(reference)

        command = ["conan", "editable", "add", path, reference]
        if layout:
            command += ["-l", layout]

        subprocess.run(command)

    # noinspection PyMethodMayBeStatic
    def remove(self, reference: Union[str, Reference]):
        if isinstance(reference, Reference):
            reference = str(reference)

        command = ["conan", "editable", "remove", reference]
        subprocess.run(command)
