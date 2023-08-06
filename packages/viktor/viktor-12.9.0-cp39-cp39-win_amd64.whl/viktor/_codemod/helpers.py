from viktor._vendor.libcst import matchers as m
from typing import List


##########
# MATCHERS
##########

def match_controller_class(node) -> bool:
    matcher = m.ClassDef(bases=[m.Arg(value=m.Name('ViktorController'))])
    return m.matches(node, matcher)


############
# COLLECTORS
############

def collect_class_attributes(node) -> List[str]:
    body = node.body.body

    simple_statements = []
    for statement in body:
        if m.matches(statement, m.SimpleStatementLine()):
            if m.matches(statement.body[0], m.Assign()):
                simple_statements.extend([s.target.value for s in statement.body[0].targets])
            elif m.matches(statement.body[0], m.AnnAssign()):
                simple_statements.append(statement.body[0].target.value)

    return simple_statements
