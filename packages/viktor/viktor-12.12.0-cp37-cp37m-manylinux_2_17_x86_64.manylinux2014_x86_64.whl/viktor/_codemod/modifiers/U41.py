from viktor._vendor import libcst

from viktor._codemod.helpers import ControllerFlagTransformer


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(ControllerFlagTransformer):
    controller_flag = 'viktor_typed_empty_fields'
    controller_flag_value = True
