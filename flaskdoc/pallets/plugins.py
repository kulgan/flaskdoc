from collections import defaultdict


API_SPECS = defaultdict(list)


def register_spec(func, spec):
    API_SPECS[func].append(spec)


def get_docs():
    return API_SPECS.items()
