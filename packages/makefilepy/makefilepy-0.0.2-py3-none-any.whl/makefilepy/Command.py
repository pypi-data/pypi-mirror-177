from typing import List

from pydantic import BaseModel, conlist


class Command(BaseModel):
    target: str
    prerequisites: List[str] = []
    recipes: conlist(str, min_items=1)
    phony: bool = True

    def build(self) -> str:
        return self._make_phony() \
               + self._make_target() \
               + self._make_recipe()

    def _make_phony(self) -> str:
        return f'.PHONY: {self.target}\n' if self.phony else ''

    def _make_target(self) -> str:
        return f'{self.target}:' \
               + ''.join([' ' + prerequisite for prerequisite in self.prerequisites]) \
               + '\n'

    def _make_recipe(self) -> str:
        return ''.join(['\t' + recipe + '\n' for recipe in self.recipes])
