"""

"""
from collections import defaultdict

API_SPECS = defaultdict(list)


def register_spec(func, spec):
    API_SPECS[func].append(spec)


def get_docs():
    return API_SPECS.items()


def parse_flask_rule(rule: str):
    """Parses a flask rule (URL), and returns an openapi compatible version of the url"""

    parsed_rule = []
    index = -1

    while index < len(rule):

        index += 1
        if index > len(rule) - 1:
            break
        char = rule[index]

        if char != "<":
            parsed_rule.append(char)
            continue

        # skip '<'
        # only interested in variable name after ':'
        variable_name = ["{"]
        index += 1
        cs = False  # colon seen flag
        char = rule[index]

        while char != ">":
            if cs:
                variable_name.append(char)
            elif char == ":":
                cs = True
            index += 1
            char = rule[index]

        variable_name.append("}")
        parsed_rule += variable_name

    return "".join(parsed_rule)
