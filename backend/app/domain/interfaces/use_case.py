from abc import ABC, abstractmethod
from ast import TypeVar
from typing import Generic

InputSchema = TypeVar("InputSchema")
OutputSchema = TypeVar("OutputSchema")


class UseCase(ABC, Generic[InputSchema, OutputSchema]):
    @abstractmethod
    def run(self, input: InputSchema) -> OutputSchema: ...

    def __call__(self, input: InputSchema) -> OutputSchema:
        return self.run(input)
