from copy import deepcopy
from typing import List, Set


class Resource:

    def __init__(self, category):
        self._category = category
        self._errors: List[str] = []

    @property
    def category(self) -> str:
        return self._category

    @property
    def errors(self) -> List[str]:
        copy = deepcopy(self._errors)
        if not copy == None:
            return copy
        raise Exception('None errors copy')

    @property
    def is_valid(self) -> bool:
        return len(self._errors) == 0

    def has_error(self, error_type: str) -> bool:
        return error_type in self._errors

    def add_error(self, error_type: str) -> None:
        self._errors.append(error_type)

    def remove_error(self, error_type:str) -> None:
        self._errors.remove(error_type)