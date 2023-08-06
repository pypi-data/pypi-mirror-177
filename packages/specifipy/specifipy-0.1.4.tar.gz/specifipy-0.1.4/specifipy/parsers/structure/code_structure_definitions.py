import dataclasses
from enum import Enum


class StructureEnum(Enum):
    CLASS = 1,
    FUNCTION = 2,
    VARIABLE = 3,
    CLASS_FIELD = 4


class ParamDefinition:
    name: str
    type: str


@dataclasses.dataclass
class Docstring:
    description: str


@dataclasses.dataclass
class StructureDefinition:
    structure_type: StructureEnum
    name: str
    start_line: int
    end_line: int


@dataclasses.dataclass
class ClassStructureDefinition(StructureDefinition):
    inherits_from: str


@dataclasses.dataclass
class FunctionStructureDefinition(StructureDefinition):
    params: list[str]
    parent_class: ClassStructureDefinition

    def __eq__(self, other):
        return (self.name, self.params, self.start_line, self.end_line, self.structure_type) == (
            other.name, other.params, other.start_line, other.end_line, other.structure_type)


@dataclasses.dataclass
class FieldStructureDefinition(StructureDefinition):
    parent_class: ClassStructureDefinition


@dataclasses.dataclass
class TypeAnnotatedFieldStructureDefinition(FieldStructureDefinition):
    type_annotation: str


@dataclasses.dataclass
class NotTypeAnnotatedFieldStructureDefinition(FieldStructureDefinition):
    pass
