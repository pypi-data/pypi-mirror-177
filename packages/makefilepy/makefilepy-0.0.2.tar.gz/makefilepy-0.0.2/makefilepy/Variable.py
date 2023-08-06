from typing import Any

from pydantic import BaseModel


class Variable(BaseModel):
    key: str
    value: Any

    def build(self) -> str:
        return f'{self.key}={self.value}'

    def reference(self) -> str:
        return f'${{{self.key}}}'
