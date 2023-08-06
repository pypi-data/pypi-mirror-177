from viktor._vendor import libcst


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    ImportALIAS = None

    def __init__(self, visitor):
        super().__init__()

    def leave_ImportFrom(self, original_node, updated_node):

        if not hasattr(updated_node.module, 'attr'):
            return updated_node

        if updated_node.module.attr.value == 'parametrization':

            new_names = []

            for name in updated_node.names:

                if name.name.value == 'Group':
                    new_names.append(name.with_changes(name=libcst.Name("Tab"), asname=None))
                    new_names.append(name.with_changes(name=libcst.Name("Section"), asname=None))
                    continue

                new_names.append(name)

            return updated_node.with_changes(names=new_names)

        return updated_node

    def leave_ImportAlias_asname(self, node) -> None:
        if node.name.value == 'Group':
            if node.asname:
                self.ImportALIAS = node.asname.name.value

    def leave_ClassDef(self, original_node, updated_node):

        body = updated_node.body
        class_body: list = list(body.body)

        new_statements = []
        for statement in class_body:
            if type(statement) == libcst.SimpleStatementLine:
                if type(statement.body[0]) == libcst.Assign:

                    try:
                        if statement.body[0].value.func.value in (self.ImportALIAS, 'Group'):
                            if type(statement.body[0].targets[0].target) == libcst.Name:
                                new_statement = create_simple_statement_line(statement, "Tab")
                            else:  # Section
                                new_statement = create_simple_statement_line(statement, "Section")

                            new_statements.append(new_statement)
                            continue
                    except Exception:
                        pass

            new_statements.append(statement)

        body = body.with_changes(body=new_statements)

        return updated_node.with_changes(body=body)


def create_simple_statement_line(statement, class_name: str):
    return libcst.SimpleStatementLine(
        body=[
            libcst.Assign(
                targets=statement.body[0].targets,
                value=statement.body[0].value.with_changes(func=libcst.Name(class_name))
            )
        ],
        leading_lines=statement.leading_lines,
        trailing_whitespace=statement.trailing_whitespace
    )
