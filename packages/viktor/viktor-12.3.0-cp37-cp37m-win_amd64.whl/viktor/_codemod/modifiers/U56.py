from viktor._vendor import libcst


_OLD_SIGNATURE_BEAM = (
    'name',
    'layer_id',
    'begin_node',
    'end_node',
    'cross_section',
    'ez',
    'lcs_rotation'
)

_OLD_SIGNATURE_PLANE = (
    'name',
    'layer_id',
    'material',
    'plane_type',
    'thickness',
    'corner_nodes',
    'internal_nodes',
    'swap_orientation',
    'lcs_rotation',
    'fem_model',
    'orthotropy'
)


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()

    def leave_Call(self, node, updated_node):

        try:
            if node.func.attr.value == 'create_beam':
                return self._convert_create_beam_signature(updated_node)
            if node.func.attr.value == 'create_plane':
                return self._convert_create_plane_signature(updated_node)
        except AttributeError:  # func may not have 'attr'
            pass

        return updated_node

    @staticmethod
    def _new_signature_used(node) -> bool:
        # find out whether the old or new signature is used:
        #   only kwargs including 'layer_id' -> old signature
        #   only kwargs excluding 'layer_id' -> new signature
        #   positional + kwargs excluding 'name' -> old signature
        #   positional + kwargs including 'name' -> new signature

        kwargs_only = False
        for arg_index, arg in enumerate(node.args):

            if arg_index == 0 and arg.keyword is not None:
                kwargs_only = True
                break

        if kwargs_only:
            for arg in node.args:
                if arg.keyword.value == 'layer_id':
                    return False

            return True
        else:
            for arg in node.args:
                if arg.keyword is not None and arg.keyword.value == 'name':
                    return True

            return False

    @staticmethod
    def _get_args_as_kwargs(node, signature):
        # collect args as kwargs
        kwargs = {}
        for arg_index, arg in enumerate(node.args):

            if arg.keyword is None:
                keyword = signature[arg_index]
            else:
                keyword = arg.keyword.value

            if keyword == 'layer_id':
                continue

            arg = arg.with_changes(keyword=libcst.Name(keyword),
                                   equal=libcst.AssignEqual(
                                       whitespace_before=libcst.SimpleWhitespace(value=''),
                                       whitespace_after=libcst.SimpleWhitespace(value=''),
                                   ))

            kwargs[keyword] = arg

        return kwargs

    def _convert_create_beam_signature(self, node):
        if self._new_signature_used(node):
            return node

        kwargs = self._get_args_as_kwargs(node, _OLD_SIGNATURE_BEAM)
        try:
            new_args = [
                kwargs['begin_node'].with_changes(keyword=None, equal=None),
                kwargs['end_node'].with_changes(keyword=None, equal=None),
                kwargs['cross_section'].with_changes(keyword=None, equal=None)
            ]
        except KeyError:  # kwargs may be missing, e.g. IdeaModel.create_beam(...), SciaModel.create_beam(n1, n2, cs1)
            return node

        for keyword, arg in kwargs.items():
            if keyword not in {'begin_node', 'end_node', 'cross_section'}:
                new_args.append(arg)

        new_args[-1] = new_args[-1].with_changes(comma=None)

        return node.with_changes(args=new_args)

    def _convert_create_plane_signature(self, node):
        if self._new_signature_used(node):
            return node

        kwargs = self._get_args_as_kwargs(node, _OLD_SIGNATURE_PLANE)
        try:
            new_args = [
                kwargs['corner_nodes'].with_changes(keyword=None, equal=None),
                kwargs['thickness'].with_changes(keyword=None, equal=None)
            ]
        except KeyError:  # kwargs may be missing, e.g. SciaModel.create_plane([...], 1, material=material)
            return node

        for keyword, arg in kwargs.items():
            if keyword not in {'corner_nodes', 'thickness'}:
                new_args.append(arg)

        new_args[-1] = new_args[-1].with_changes(comma=None)

        return node.with_changes(args=new_args)
