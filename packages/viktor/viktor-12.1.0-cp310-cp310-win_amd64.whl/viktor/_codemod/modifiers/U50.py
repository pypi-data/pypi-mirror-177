from viktor._vendor import libcst


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()

    def leave_ClassDef(self, original_node, updated_node):

        body = original_node.body
        class_body: list = list(body.body)

        simple_statements = []

        for statement in class_body:
            if type(statement) == libcst.SimpleStatementLine:
                if type(statement.body[0]) == libcst.Assign:
                    simple_statements.extend([s.target.value for s in statement.body[0].targets])
                elif type(statement.body[0]) == libcst.AnnAssign:
                    simple_statements.append(statement.body[0].target.value)

        if 'summary' in simple_statements:  # Controller
            if 'viktor_convert_date_field' not in simple_statements:

                class_body[0] = class_body[0].with_changes(leading_lines=[libcst.EmptyLine()])

                class_body.insert(0, libcst.SimpleStatementLine(
                    body=[
                        libcst.Assign(
                            targets=[
                                libcst.AssignTarget(
                                    target=libcst.Name('viktor_convert_date_field'),
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

        return original_node
