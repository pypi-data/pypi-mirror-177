from viktor._vendor import libcst

_FIELD_NAME = "NumberField"

_KEYWORDS = (
    "ui_name",
    "name",
    "prefix",
    "icon",
    "suffix",
    "default",
    "step",
    "min",
    "max",
    "min_message",
    "max_message",
    "num_decimals",
    "visible",
    "flex",
    "flex_sm",
    "tooltip",
    "integer",
    "variant",
)

_REMOVED_KEYWORDS = (
    "integer",
)


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    ImportALIAS = None

    def __init__(self, visitor):
        super().__init__()

    def leave_ImportAlias_asname(self, node) -> None:
        if node.name.value == _FIELD_NAME:
            if node.asname:
                self.ImportALIAS = node.asname.name.value

    def leave_Call(self, node, updated_node):

        try:
            if node.func.value != (self.ImportALIAS or _FIELD_NAME):
                return updated_node
        except AttributeError:  # func may not have 'value'
            return updated_node

        new_args = []
        append_as_keyword = False
        for arg_index, arg in enumerate(node.args):

            if arg_index > 0:
                if arg.keyword is None:
                    keyword = _KEYWORDS[arg_index]
                else:
                    keyword = arg.keyword.value

                if keyword in _REMOVED_KEYWORDS:
                    append_as_keyword = True
                    continue

                if append_as_keyword:
                    arg = arg.with_changes(keyword=libcst.Name(keyword),
                                           equal=libcst.AssignEqual(
                                               whitespace_before=libcst.SimpleWhitespace(value=''),
                                               whitespace_after=libcst.SimpleWhitespace(value=''),
                                           ))

            new_args.append(arg)

        new_args[-1] = new_args[-1].with_changes(comma=None)

        return updated_node.with_changes(args=new_args)
