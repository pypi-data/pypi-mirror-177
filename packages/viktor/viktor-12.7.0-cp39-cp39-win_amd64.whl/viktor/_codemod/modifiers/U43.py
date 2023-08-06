from viktor._vendor import libcst

MAP_ReturnType = {
    'MODEL_ONLY': ('False', 'True'),
    'RESULT_ONLY': ('True', 'False'),
    'MODEL_AND_RESULT': ('True', 'True')
}


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    ImportALIAS = None

    def __init__(self, visitor):
        super().__init__()

    def leave_ImportAlias_asname(self, node) -> None:
        if node.name.value == 'AxisVMAnalysis':
            if node.asname:
                self.ImportALIAS = node.asname.name.value

    def leave_Call(self, original_node, updated_node):
        new_args = []

        try:
            if original_node.func.value != (self.ImportALIAS or 'AxisVMAnalysis'):
                return original_node
        except AttributeError:  # func may not have 'value'
            return original_node

        for arg_index, arg in enumerate(original_node.args):

            if arg_index > 0:
                if arg.keyword is None:
                    keyword = 'return_type'
                else:
                    keyword = arg.keyword.value

                if keyword == 'return_type':

                    val1, val2 = MAP_ReturnType[str(arg.value.attr.value)]

                    arg1 = arg.with_changes(keyword=libcst.Name('return_results'),
                                            value=libcst.Name(val1),
                                            equal=libcst.AssignEqual(
                                                whitespace_before=libcst.SimpleWhitespace(value=''),
                                                whitespace_after=libcst.SimpleWhitespace(value=''),
                                            ))

                    arg2 = arg1.with_changes(keyword=libcst.Name('return_model'),
                                             value=libcst.Name(val2))

                    new_args.extend([arg1, arg2])
                    return updated_node.with_changes(args=new_args)

            new_args.append(arg)

        return original_node
