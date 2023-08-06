from viktor._vendor import libcst

from viktor._codemod.helpers import match_controller_class, collect_class_attributes


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()

    def leave_ClassDef(self, original_node, updated_node):

        if not match_controller_class(original_node):
            return updated_node

        body = original_node.body
        class_body: list = list(body.body)
        simple_statements = collect_class_attributes(updated_node)

        if 'viktor_convert_entity_field' not in simple_statements:

            class_body[0] = class_body[0].with_changes(leading_lines=[libcst.EmptyLine()])

            class_body.insert(0, libcst.SimpleStatementLine(
                body=[
                    libcst.Assign(
                        targets=[
                            libcst.AssignTarget(
                                target=libcst.Name('viktor_convert_entity_field'),
                                whitespace_before_equal=libcst.SimpleWhitespace(' '),
                                whitespace_after_equal=libcst.SimpleWhitespace(' ')
                            )
                        ],
                        value=libcst.Name('True')
                    )
                ],
                leading_lines=[libcst.EmptyLine()]
            ))

            body = body.with_changes(body=class_body)
            return updated_node.with_changes(body=body)

        return updated_node
