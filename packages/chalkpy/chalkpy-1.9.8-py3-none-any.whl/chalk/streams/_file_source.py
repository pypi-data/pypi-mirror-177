from typing import Any

from pydantic import BaseModel

from chalk.streams._types import StreamSource


class FileSource(BaseModel, StreamSource):
    path: str

    def config_to_json(self) -> Any:
        return self.json(exclude={"message_model"})
