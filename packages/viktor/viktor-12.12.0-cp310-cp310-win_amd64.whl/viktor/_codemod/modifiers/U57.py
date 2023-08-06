from viktor._vendor import libcst


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()

        self.encoding = None
        self.encoding_line_id = None
        self.within_text_file_controller = False
        self.within_binary_file_controller = False

    def leave_ImportFrom(self, original_node, updated_node):

        # update imports:
        #   from viktor.core import ViktorTextFileController -> from viktor.core import ViktorController, ParamsFromFile
        new_names = []
        for name in updated_node.names:
            if name.name.value in {'ViktorTextFileController', 'ViktorBinaryFileController'}:
                new_names.append(name.with_changes(name=libcst.Name("ViktorController"), asname=None))
                new_names.append(name.with_changes(name=libcst.Name("ParamsFromFile"), asname=None))
                continue
            new_names.append(name)

        return updated_node.with_changes(names=new_names)

    def visit_ClassDef(self, node: "ClassDef"):
        # determine whether we are in one of the deprecated classes
        for base in node.bases:
            if base.value.value == 'ViktorTextFileController':
                self.within_text_file_controller = True
            if base.value.value == 'ViktorBinaryFileController':
                self.within_binary_file_controller = True

        # retrieve encoding and corresponding line if defined on ViktorTextFileController
        if self.within_text_file_controller:
            for line_id, line in enumerate(node.body.body):
                if type(line) == libcst.SimpleStatementLine:
                    target = line.body[0].targets[0].target
                    if target.value == 'encoding':
                        self.encoding = line.body[0].value
                        self.encoding_line_id = line_id
                        break

        return True

    def leave_ClassDef(self, original_node: "ClassDef", updated_node: "ClassDef"):

        # update inheritance: Controller(ViktorTextFileController) -> Controller(ViktorController)
        new_bases = []
        for base in updated_node.bases:
            if base.value.value == 'ViktorTextFileController':
                base = base.with_changes(value=libcst.Name('ViktorController'))
            if base.value.value == 'ViktorBinaryFileController':
                base = base.with_changes(value=libcst.Name('ViktorController'))
            new_bases.append(base)

        # remove encoding if defined as controller attribute
        body = updated_node.body
        if self.encoding_line_id is not None:
            new_body = list(body.body)
            new_body.pop(self.encoding_line_id)
            body = body.with_changes(body=new_body)

        return updated_node.with_changes(bases=new_bases, body=body)

    def leave_FunctionDef(self, original_node: "FunctionDef", updated_node: "FunctionDef"):

        if self.within_text_file_controller or self.within_binary_file_controller:
            if updated_node.name.value == 'process_file':

                # add @ParamsFromFile decorator
                decorators = [libcst.Decorator(decorator=libcst.Call(func=libcst.Name('ParamsFromFile')))]

                # update signature: (self, file_content) -> (self, file, **kwargs)
                new_params = libcst.Parameters(
                    params=[
                        libcst.Param(name=libcst.Name('self')),
                        libcst.Param(name=libcst.Name('file'))
                    ],
                    star_kwarg=libcst.Param(name=libcst.Name('kwargs'))
                )

                # insert line in body:
                #   file_content = file.getvalue()              # if ViktorTextFileController
                #   file_content = file.getvalue(encoding=...)  # if ViktorTextFileController with encoding
                #   file_content = file.getvalue_binary()       # if ViktorBinaryFileController
                body = updated_node.body
                new_body = list(body.body)
                new_body.insert(
                    0,
                    libcst.SimpleStatementLine(
                        body=[
                            libcst.Assign(
                                targets=[
                                    libcst.AssignTarget(libcst.Name('file_content'))
                                ],
                                value=libcst.Call(
                                    func=libcst.Attribute(
                                        value=libcst.Name('file'),
                                        attr=libcst.Name('getvalue') if self.within_text_file_controller else libcst.Name('getvalue_binary'),
                                    ),
                                    args=[
                                        libcst.Arg(
                                            value=self.encoding,
                                            keyword=libcst.Name('encoding'),
                                            equal=libcst.AssignEqual(
                                                whitespace_before=libcst.SimpleWhitespace(''),
                                                whitespace_after=libcst.SimpleWhitespace(''),
                                            ),
                                        )
                                    ] if self.encoding else []
                                ),
                            ),
                        ],
                    ),
                )
                body = body.with_changes(body=new_body)

                return updated_node.with_changes(params=new_params, decorators=decorators, body=body)

        return updated_node
