import dataclasses

from specifipy.parsers.structure.code_structure_definitions import FunctionStructureDefinition, ClassStructureDefinition, \
    FieldStructureDefinition


@dataclasses.dataclass
class ParsingResult:
    classes: list[ClassStructureDefinition]
    functions: list[FunctionStructureDefinition]
    class_fields: list[FieldStructureDefinition]
