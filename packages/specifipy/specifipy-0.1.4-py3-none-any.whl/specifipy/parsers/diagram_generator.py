import os

from specifipy.parsers.generic_parser import GenericParser
from specifipy.parsers.results import ParsingResult


class DiagramGenerator(GenericParser):
    header = f"""
from diagrams import Diagram, Edge
from diagrams.custom import Custom

param_icon = "{os.path.dirname(os.path.dirname(__file__)) + "/resources"}/icons/param_icon.png"
function_icon = "{os.path.dirname(os.path.dirname(__file__)) + "/resources"}/icons/function_icon.png"
class_icon = "{os.path.dirname(os.path.dirname(__file__)) + "/resources"}/icons/class_icon.png"
field_icon = "{os.path.dirname(os.path.dirname(__file__)) + "/resources"}/icons/field_icon.png"
dotted_line = Edge(style="dotted")
"""

    def generate_diagram(self, source_file_content: str, source_file_name: str, base_path=None):
        parsing_result: ParsingResult = self.parse(source_file_content)
        elements_to_generate = []
        links_to_generate = []

        for clazz in parsing_result.classes:
            class_element_definition = f"class_{clazz.name} = Custom('{clazz.name}', class_icon)"
            elements_to_generate.append(class_element_definition)
            if clazz.inherits_from:
                links_to_generate.append(
                    f"class_{clazz.inherits_from} >> dotted_line >> class_{clazz.name}"
                )
                if clazz.inherits_from not in [x.name for x in
                                               parsing_result.classes] and f"class_{clazz.inherits_from} = Custom('{clazz.inherits_from}', class_icon)" not in elements_to_generate:
                    elements_to_generate.append(
                        f"class_{clazz.inherits_from} = Custom('{clazz.inherits_from}', class_icon)"
                    )

        for func in parsing_result.functions:
            function_element_definition = f"func_{func.name}_{func.parent_class} = Custom('{func.name}', function_icon)"
            elements_to_generate.append(function_element_definition)
            links_to_generate.append(f"func_{func.name}_{func.parent_class} >> class_{func.parent_class}")
            for param in func.params:
                param_definition = f"param_{param}_{func.name}_{func.parent_class} = Custom('{param}', param_icon)"
                elements_to_generate.append(param_definition)
                links_to_generate.append(
                    f"param_{param}_{func.name}_{func.parent_class} >> func_{func.name}_{func.parent_class}")

        for field in parsing_result.class_fields:
            field_element_definition = f"field_{field.name}_{field.parent_class.name} = Custom('{field.name}', field_icon)"
            elements_to_generate.append(field_element_definition)
            links_to_generate.append(
                f"field_{field.name}_{field.parent_class.name} >> class_{field.parent_class.name}"
            )

        joined_elements_to_generate = "\t" + "\n\t".join(elements_to_generate)
        joined_links_to_generate = "\t" + "\n\t".join(links_to_generate)

        diagram_definition = f'with Diagram("{source_file_name}", show=False, filename="{base_path if base_path else ""}{source_file_name}"):\n'
        generated_file = f"{self.header}\n{diagram_definition}\n{joined_elements_to_generate}\n{joined_links_to_generate}"
        exec(f"{generated_file}")
