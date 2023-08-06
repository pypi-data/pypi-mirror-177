from viktor._vendor import libcst


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()

    def leave_Attribute(self, original_node: "Attribute", updated_node: "Attribute") -> "BaseExpression":
        if original_node.attr.value == "top_nap":
            attr = updated_node.attr.with_changes(value="top")
            return updated_node.with_changes(attr=attr)
        if original_node.attr.value == "bottom_nap":
            attr = updated_node.attr.with_changes(value="bottom")
            return updated_node.with_changes(attr=attr)

        return original_node
