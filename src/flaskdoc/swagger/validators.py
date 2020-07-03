from urllib import parse


def validate_url(url: str, label: str):
    parsed = parse.urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        raise ValueError("{label} entry '{url}' is not a valid url".format(label=label, url=url))
