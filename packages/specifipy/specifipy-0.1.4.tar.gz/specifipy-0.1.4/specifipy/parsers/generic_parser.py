import ast

from specifipy.parsers.results import ParsingResult
from specifipy.parsers.structure.code_structure_definitions import ClassStructureDefinition, FunctionStructureDefinition, \
    StructureEnum, TypeAnnotatedFieldStructureDefinition, NotTypeAnnotatedFieldStructureDefinition


class GenericParser:
    def __init__(self):
        pass

    def __classify_node(self, node: ast.AST, parsing_result: ParsingResult, parent=None) -> None:
        match type(node):
            case ast.ClassDef:
                node: ast.ClassDef
                name: str = node.name
                inherits_from = ""
                if len(node.bases) > 0:
                    if isinstance(node.bases[0], ast.Name):
                        inherits_from = node.bases[0].id
                    if isinstance(node.bases[0], ast.Attribute):
                        inherits_from = f"{node.bases[0].value.id}_{node.bases[0].attr}"

                class_definition = ClassStructureDefinition(StructureEnum.CLASS, name, node.lineno, node.end_lineno,
                                                            inherits_from)

                if class_definition not in parsing_result.classes:
                    parsing_result.classes.append(class_definition)
                sub_node: ast.AST
                for sub_node in node.body:
                    self.__classify_node(sub_node, parsing_result, parent=class_definition)

            case ast.FunctionDef:
                node: ast.FunctionDef
                name: str = node.name
                params: ast.arguments = node.args
                params_string: list[str] = [x.arg for x in params.args]
                function_definition = FunctionStructureDefinition(StructureEnum.FUNCTION, name,
                                                                  node.lineno, node.end_lineno, params_string,
                                                                  (parent.name if parent else None))
                if function_definition not in parsing_result.functions:
                    parsing_result.functions.append(function_definition)

            case ast.AnnAssign:
                if isinstance(parent, ClassStructureDefinition) and parent:
                    node: ast.AnnAssign
                    name: str = node.target.id
                    type_annotation: str = (node.annotation.id if not type(node.annotation) == ast.Subscript else node.annotation.value.id)
                    field = TypeAnnotatedFieldStructureDefinition(StructureEnum.CLASS_FIELD, name, node.lineno,
                                                                  node.end_lineno,
                                                                  parent, type_annotation)
                    parsing_result.class_fields.append(field)

            case ast.Assign:
                if isinstance(parent, ClassStructureDefinition) and parent:
                    node: ast.Assign
                    name: str = node.targets[0].id
                    field = NotTypeAnnotatedFieldStructureDefinition(StructureEnum.CLASS_FIELD, name, node.lineno,
                                                                     node.end_lineno,
                                                                     parent)
                    parsing_result.class_fields.append(field)

    def parse(self, source_code_file_content: str) -> ParsingResult:
        code = ast.parse(source_code_file_content)
        parsing_result: ParsingResult = ParsingResult([], [], [])
        for node in ast.walk(code):
            self.__classify_node(node, parsing_result)
        return parsing_result
