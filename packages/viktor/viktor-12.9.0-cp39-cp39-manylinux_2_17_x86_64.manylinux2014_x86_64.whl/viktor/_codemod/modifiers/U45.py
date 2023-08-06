from viktor._vendor import libcst


_KEYWORDS = (
    "ui_name",
    "view",
    "name",
    "prefix",
    "icon",
    "suffix",
    "visible",
    "flex",
    "flex_sm",
    "disabled",
    "output_value"
)

_REMOVED_KEYWORDS = (
    "view",
    "name",
    "icon",
    "flex_sm",
    "disabled"
)


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    ImportALIAS = None
    RequiredLookupImport = None

    def __init__(self, visitor):
        super().__init__()

    def leave_ImportAlias_asname(self, node) -> None:
        if node.name.value == 'OutputField':
            if node.asname:
                self.ImportALIAS = node.asname.name.value
        if node.name.value == 'Lookup':
            self.RequiredLookupImport = False

    def leave_Module(self, original_node, updated_node):
        reversed_body = []
        import_added = False

        # walk through lines in reverse order and add 'from viktor.parametrization import Lookup' before the
        # first occurrence of an import if necessary (i.e. if 'view=...' is converted to 'value=Lookup(...)'
        for line in reversed(updated_node.body):
            if not import_added and self.RequiredLookupImport:
                if type(line) == libcst.SimpleStatementLine:
                    if type(line.body[0]) is libcst.Import or type(line.body[0]) is libcst.ImportFrom:
                        reversed_body.append(libcst.SimpleStatementLine(body=tuple([
                            libcst.ImportFrom(
                                module=libcst.Attribute(
                                    value=libcst.Name('viktor'),
                                    attr=libcst.Name('parametrization')
                                ),
                                names=[libcst.ImportAlias(name=libcst.Name('Lookup'))]
                            )])))
                        import_added = True

            reversed_body.append(line)

        updated_body = reversed(reversed_body)

        return updated_node.with_changes(body=updated_body)

    def leave_Call(self, node, updated_node):

        try:
            if node.func.value != (self.ImportALIAS or 'OutputField'):
                return updated_node
        except AttributeError:  # func may not have 'value'
            return updated_node

        new_args = []
        keywords = []
        view = None
        for arg_index, arg in enumerate(node.args):

            if arg_index > 0:
                if arg.keyword is None:
                    keyword = _KEYWORDS[arg_index]
                else:
                    keyword = arg.keyword.value

                if keyword == 'output_value':
                    keyword = 'value'

                if keyword in _REMOVED_KEYWORDS:
                    if keyword == 'view':
                        view = arg.value
                    continue

                arg = arg.with_changes(keyword=libcst.Name(keyword),
                                       equal=libcst.AssignEqual(
                                           whitespace_before=libcst.SimpleWhitespace(value=''),
                                           whitespace_after=libcst.SimpleWhitespace(value=''),
                                       ))
                keywords.append(keyword)

            new_args.append(arg)

        # convert view='field_x' -> value=Lookup('field_x')
        if view is not None and 'value' not in keywords:
            new_args.append(libcst.Arg(keyword=libcst.Name('value'),
                                       equal=libcst.AssignEqual(
                                           whitespace_before=libcst.SimpleWhitespace(value=''),
                                           whitespace_after=libcst.SimpleWhitespace(value='')
                                       ),
                                       value=libcst.Call(
                                           func=libcst.Name('Lookup'),
                                           args=[
                                               libcst.Arg(value=view)
                                           ]))
                            )
            if self.RequiredLookupImport is None:
                self.RequiredLookupImport = True

        new_args[-1] = new_args[-1].with_changes(comma=None)

        return updated_node.with_changes(args=new_args)
