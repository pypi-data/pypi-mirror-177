from viktor._vendor import libcst


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()

    def leave_FunctionDef(self, original_node: "FunctionDef", updated_node: "FunctionDef"):

        if updated_node.params.star_kwarg:
            return updated_node

        params = updated_node.params.params
        if len(params) == 2:

            if params[0].name.value == 'params' and params[1].name.value == 'entity_id':

                new_params = libcst.Parameters(
                    params=params,
                    star_kwarg=libcst.Param(
                        libcst.Name('kwargs')
                    )
                )

                return updated_node.with_changes(params=new_params)

        return updated_node
