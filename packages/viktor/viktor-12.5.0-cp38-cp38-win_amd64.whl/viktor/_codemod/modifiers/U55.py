from typing import List

from viktor._vendor import libcst


_KEYWORDS = (
        'name',
        'plane',
        'edge',
        'freedom',
        'stiffness',
        'c_sys',
        'c_def',
        'position_x1',
        'position_x2',
        'origin'
    )

_TUPLE_KEYWORDS = {
    'freedom': (
        'x',
        'y',
        'z',
        'rx',
        'ry',
        'rz'
    ),
    'stiffness': (
        'stiffness_x',
        'stiffness_y',
        'stiffness_z',
        'stiffness_rx',
        'stiffness_ry',
        'stiffness_rz'
    )
}


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()

    def leave_Call(self, node, updated_node):

        try:
            if node.func.attr.value == 'create_line_force_surface':
                return self._convert_line_force_surface(updated_node)
            if node.func.attr.value == 'create_line_support_surface':
                return self._convert_line_support_surface(updated_node)
        except AttributeError:  # func may not have 'attr'
            pass

        return updated_node

    @staticmethod
    def _convert_line_force_surface(node):
        new_args = []
        for arg_index, arg in enumerate(node.args):

            if arg.keyword is not None:
                if arg.keyword.value == 'plane':
                    plane_val = arg.value
                    continue
                if arg.keyword.value == 'edge':
                    edge_val = arg.value
                    continue

            new_args.append(arg)

        new_args.insert(0, libcst.Arg(
            value=libcst.Tuple([libcst.Element(value=plane_val), libcst.Element(value=edge_val)])
        ))

        new_args[-1] = new_args[-1].with_changes(comma=None)

        func = node.func.with_changes(attr=libcst.Name('create_line_load_on_plane'))
        return node.with_changes(func=func, args=new_args)

    @staticmethod
    def _convert_line_support_surface(node):
        new_args = []
        for arg_index, arg in enumerate(node.args):

            if arg.keyword is None:
                keyword = _KEYWORDS[arg_index]
            else:
                keyword = arg.keyword.value

            if keyword == 'plane':
                plane_val = arg.value
                continue
            if keyword == 'edge':
                edge_val = arg.value
                if edge_val.attr.value == 'ONE':
                    edge_val = libcst.Integer('1')
                elif edge_val.attr.value == 'TWO':
                    edge_val = libcst.Integer('2')
                elif edge_val.attr.value == 'THREE':
                    edge_val = libcst.Integer('3')
                else:
                    edge_val = libcst.Integer('4')
                continue
            if keyword in ('freedom', 'stiffness'):
                _add_tuple_kwarg(arg, new_args, keyword)
                continue

            arg = arg.with_changes(keyword=libcst.Name(keyword),
                                   equal=libcst.AssignEqual(
                                       whitespace_before=libcst.SimpleWhitespace(value=''),
                                       whitespace_after=libcst.SimpleWhitespace(value=''),
                                   ))
            new_args.append(arg)

        new_args.insert(0, libcst.Arg(
            value=libcst.Tuple([libcst.Element(value=plane_val), libcst.Element(value=edge_val)])
        ))

        new_args[-1] = new_args[-1].with_changes(comma=None)

        func = node.func.with_changes(attr=libcst.Name('create_line_support_on_plane'))
        return node.with_changes(func=func, args=new_args)


def _add_tuple_kwarg(arg: libcst.Arg, new_args: List[libcst.Arg], keyword: str) -> None:
    """ Convert a single tuple argument to multiple keyword arguments, e.g.:

    freedom: Tuple[float, float, float, float, float]
    func(freedom)  ->  func(x=freedom[0], y=freedom[1], z=freedom[2], rx=freedom[3], ry=freedom[4], rz=freedom[5])
    func((0, 1, 2, 3, 4, 5))  ->  func(x=0, y=1, z=2, rx=3, ry=4, rz=5)
    """
    value = arg.value
    keywords = _TUPLE_KEYWORDS[keyword]
    if type(value) == libcst.Tuple:
        for element_id, element in enumerate(value.elements, 0):
            new_args.append(libcst.Arg(
                keyword=libcst.Name(keywords[element_id]),
                value=element.value,
                equal=libcst.AssignEqual(
                    whitespace_before=libcst.SimpleWhitespace(value=''),
                    whitespace_after=libcst.SimpleWhitespace(value=''),
                )
            ))
    else:
        for f in range(6):
            f_val = libcst.Subscript(
                value=libcst.Name(value.value),
                slice=[
                    libcst.SubscriptElement(
                        slice=libcst.Index(
                            value=libcst.Integer(str(f)),
                        ),
                    ),
                ]
            )

            new_args.append(libcst.Arg(
                keyword=libcst.Name(keywords[f]),
                value=f_val,
                equal=libcst.AssignEqual(
                    whitespace_before=libcst.SimpleWhitespace(value=''),
                    whitespace_after=libcst.SimpleWhitespace(value=''),
                )
            ))

    new_args[-1] = arg.with_changes(
        keyword=new_args[-1].keyword,
        value=new_args[-1].value,
        equal=libcst.AssignEqual(
            whitespace_before=libcst.SimpleWhitespace(value=''),
            whitespace_after=libcst.SimpleWhitespace(value=''),
        )
    )
