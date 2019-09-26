def api_response():

    def decorator():
        return 1
    return decorator


def parameter(name, location, description=None, required=False, deprecated=False, allow_empty_value=False):

    def decorator(f):
        return f()
    return decorator
