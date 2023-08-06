from viktor._vendor import libcst

from viktor._codemod.helpers import match_controller_class


def dfs(visited, graph, method):
    """ Depth-first search to find all methods that will subsequently be called 'method' is called. """
    if method not in visited:
        visited.add(method)

        try:
            for neighbour in graph[method]:
                dfs(visited, graph, neighbour)
        except KeyError:
            pass


class Visitor(libcst.CSTVisitor):

    def __init__(self):
        super().__init__()

        self.within_controller = False
        self.add_params_in_signature = False
        self.add_entity_id_in_signature = False

        self.called_methods = []

        self.method_graph = {}
        self.methods_with_params = []
        self.methods_with_entity_id = []

        self.method_nesting_level = 0

    def visit_ClassDef(self, node: "ClassDef"):
        self.within_controller = match_controller_class(node)

    def leave_ClassDef(self, original_node: "ClassDef") -> None:
        self.within_controller = False

    def leave_Attribute(self, original_node: "Attribute") -> None:
        if not self.within_controller:
            return

        try:
            if original_node.value.value == 'self':
                if original_node.attr.value == "_params":
                    self.add_params_in_signature = True
                if original_node.attr.value == "_entity_id":
                    self.add_entity_id_in_signature = True
        except AttributeError:
            return

    def leave_Call_func(self, node: "Call") -> None:
        if not self.within_controller:
            return

        try:
            if node.func.value.value == 'self':
                self.called_methods.append(node.func.attr.value)
                return
        except AttributeError:  # func may not have 'attr'
            pass

        try:
            if type(node.func.value) == str:
                self.called_methods.append(node.func.value)
        except AttributeError:  # func may not have 'value'
            pass

    def visit_FunctionDef(self, node: "FunctionDef"):
        if not self.within_controller:
            return

        self.method_nesting_level += 1

    def leave_FunctionDef(self, original_node: "FunctionDef") -> None:
        if not self.within_controller:
            return

        self.method_nesting_level -= 1
        self.method_graph[original_node.name.value] = list(self.called_methods)

        if self.method_nesting_level == 0:
            self.called_methods = []
        if self.add_params_in_signature:
            self.methods_with_params.append(original_node.name.value)
            self.add_params_in_signature = False
        if self.add_entity_id_in_signature:
            self.methods_with_entity_id.append(original_node.name.value)
            self.add_entity_id_in_signature = False


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()

        self.within_controller = False

        self.method_graph = visitor.method_graph
        self.methods_with_params = visitor.methods_with_params
        self.methods_with_entity_id = visitor.methods_with_entity_id

    def visit_ClassDef(self, node: "ClassDef"):
        self.within_controller = match_controller_class(node)

    def leave_ClassDef(self, original_node: "ClassDef", updated_node: "ClassDef"):
        self.within_controller = False
        return updated_node

    def leave_FunctionDef(self, original_node: "FunctionDef", updated_node: "FunctionDef"):
        params_in_signature = False
        entity_id_in_signature = False
        new_args = []
        new_kwargs = []
        for param in updated_node.params.params:

            if type(param.equal) == libcst.AssignEqual:
                new_kwargs.append(param)
            else:
                new_args.append(param)

            if param.name.value == 'params':
                params_in_signature = True
            if param.name.value == 'entity_id':
                entity_id_in_signature = True

        called_methods = set()
        dfs(called_methods, self.method_graph, updated_node.name.value)

        if not params_in_signature:
            if any([m in self.methods_with_params for m in called_methods]):
                new_args.append(
                    libcst.Param(
                        name=libcst.Name('params'),
                    )
                )
        if not entity_id_in_signature:
            if any([m in self.methods_with_entity_id for m in called_methods]):
                new_args.append(
                    libcst.Param(
                        name=libcst.Name('entity_id'),
                    )
                )

        new_params = updated_node.params.with_changes(params=new_args + new_kwargs)

        return updated_node.with_changes(params=new_params)

    def leave_Attribute(self, original_node: "Attribute", updated_node: "Attribute") -> "BaseExpression":
        if not self.within_controller:
            return updated_node

        try:
            if original_node.value.value == 'self':
                if original_node.attr.value == "_params":
                    return libcst.Name('params')
                if original_node.attr.value == "_entity_id":
                    return libcst.Name('entity_id')
        except AttributeError:  # call may not have 'value'
            pass

        return updated_node

    def leave_Call(self, original_node: "Call", updated_node: "Call") -> "BaseExpression":
        new_args = list(updated_node.args)

        called_methods = set()
        try:
            dfs(called_methods, self.method_graph, updated_node.func.attr.value)
        except AttributeError:  # func may not have 'attr'
            pass
        try:
            dfs(called_methods, self.method_graph, updated_node.func.value)
        except AttributeError:  # func may not have 'value'
            pass

        if len(called_methods) == 0:
            return updated_node

        if any([m in self.methods_with_params for m in called_methods]):
            new_args.append(self._create_kwarg('params'))
        if any([m in self.methods_with_entity_id for m in called_methods]):
            new_args.append(self._create_kwarg('entity_id'))

        return updated_node.with_changes(args=new_args)

    @staticmethod
    def _create_kwarg(arg: str):
        return libcst.Arg(
            value=libcst.Name(arg),
            keyword=libcst.Name(arg),
            equal=libcst.AssignEqual(
                whitespace_before=libcst.SimpleWhitespace(
                    value='',
                ),
                whitespace_after=libcst.SimpleWhitespace(
                    value='',
                )
            )
        )
