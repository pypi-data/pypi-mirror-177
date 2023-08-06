from viktor._vendor import libcst


_FIELD_NAME = "DateField"

_KEYWORDS = (
    "ui_name",
    "name",
    "prefix",
    "suffix",
    "default",
    "flex",
    "flex_sm",
    "visible"
)


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()

        self._import_alias = None
        self._required_datetime_import = None

    def leave_ImportAlias_asname(self, node) -> None:
        if node.name.value == _FIELD_NAME:
            if node.asname:
                self._import_alias = node.asname.name.value
        if node.name.value == 'datetime':
            self._required_datetime_import = False

    def leave_Module(self, original_node, updated_node):
        reversed_body = []
        import_added = False

        # walk through lines in reverse order and add 'from viktor.parametrization import Lookup' before the
        # first occurrence of an import if necessary (i.e. if 'default=...' is converted to 'default=datetime.date(...)'
        for line in reversed(updated_node.body):
            if not import_added and self._required_datetime_import:
                if type(line) == libcst.SimpleStatementLine:
                    if type(line.body[0]) is libcst.Import or type(line.body[0]) is libcst.ImportFrom:
                        reversed_body.append(libcst.SimpleStatementLine(body=tuple([
                            libcst.Import(
                                names=[libcst.ImportAlias(name=libcst.Name('datetime'))]
                            )])))
                        import_added = True

            reversed_body.append(line)

        updated_body = reversed(reversed_body)

        return updated_node.with_changes(body=updated_body)

    def leave_Call(self, node, updated_node):

        try:
            if node.func.value != (self._import_alias or _FIELD_NAME):
                return updated_node
        except AttributeError:  # func may not have 'value'
            return updated_node

        new_args = []
        for arg_index, arg in enumerate(node.args):

            if arg_index > 0:
                if arg.keyword is None:
                    keyword = _KEYWORDS[arg_index]
                else:
                    keyword = arg.keyword.value

                if keyword == 'default':
                    default = arg.value
                    if type(default) == libcst.SimpleString:
                        default = _convert_simple_string_to_datetime_call(default)
                        arg = arg.with_changes(value=default)

                        if self._required_datetime_import is None:
                            self._required_datetime_import = True

                    elif type(default) == libcst.Name:  # e.g. a date as variable
                        default = _convert_name_to_datetime_call(default)
                        arg = arg.with_changes(value=default)

                        if self._required_datetime_import is None:
                            self._required_datetime_import = True

            new_args.append(arg)

        new_args[-1] = new_args[-1].with_changes(comma=None)

        return updated_node.with_changes(args=new_args)


def _convert_simple_string_to_datetime_call(simple_string: libcst.SimpleString) -> libcst.Call:
    # [1:-1] to strip outer (double)quotes, e.g. "'...'" -> '...' or "'...'" -> '...'
    year, month, day = simple_string.value[1:-1].split('-')
    return libcst.Call(
        func=libcst.Attribute(
            value=libcst.Name('datetime'),
            attr=libcst.Name('date')
        ),
        args=[
            libcst.Arg(
                value=libcst.Integer(str(int(year)))
            ),
            libcst.Arg(
                value=libcst.Integer(str(int(month)))
            ),
            libcst.Arg(
                value=libcst.Integer(str(int(day)))
            )
        ],
    )


def _convert_name_to_datetime_call(name: libcst.Name) -> libcst.Call:
    return libcst.Call(
        func=libcst.Attribute(
            value=libcst.Call(
                func=libcst.Attribute(
                    value=libcst.Attribute(
                        value=libcst.Name('datetime'),
                        attr=libcst.Name('datetime')
                    ),
                    attr=libcst.Name('strptime')
                ),
                args=[
                    libcst.Arg(
                        value=name
                    ),
                    libcst.Arg(
                        value=libcst.SimpleString("'%Y-%m-%d'")
                    )
                ],
            ),
            attr=libcst.Name('date')
        )
    )
