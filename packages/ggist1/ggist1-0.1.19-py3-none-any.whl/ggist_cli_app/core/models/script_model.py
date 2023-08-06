from dataclasses import dataclass, field
from ggist_cli_app.core.os import OS
from ggist_cli_app.utils.io import DictLoader
from typing import List, Optional, Union
from enum import Enum


class StepRunnerType(Enum):
    SHELL="shell"
    MARKDOWN="markdown"
    PYTHON="python"
    GGIST_SCRIPT="ggist_script"
    LINK="link"


@dataclass(frozen=True)
class StepModel(DictLoader):
    title: str
    runner: StepRunnerType
    content: str
    description: str

@dataclass(frozen=True)    
class StepGlobalModel(StepModel):
    id: str

@dataclass(frozen=True)
class StepRefModel(DictLoader):
    ref: str

@dataclass(frozen=True)
class StepsModel(DictLoader):
    steps: List[Union[StepModel, StepRefModel]]
    env: Optional[OS] = field(default=OS.ANY)
    label: Optional[str] = field(default=None)
    depends: Optional[List[str]] = field(default_factory=list)


@dataclass(frozen=True)
class SpecModel(DictLoader):
    variations: List[StepsModel]
    globals: Optional[List[StepGlobalModel]] = field(default=None)
    alias: Optional[str] = field(default=None)

@dataclass(frozen=True)
class ScriptModel(DictLoader):
    name: str
    title: str
    
    spec: SpecModel

    description: Optional[str] = field(default=None)
    def supports_os(self, os: OS)->bool:
        return any(os==variation.env or variation.env==OS.ANY for variation in  self.spec.variations)

    def get_variations_for_os(self, os: OS)->bool:
        return tuple(variation for variation in  self.spec.variations if os==variation.env or variation.env==OS.ANY)

