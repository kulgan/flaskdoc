import sys

import click

from flaskdoc.examples.app import run_examples


@click.group(name="flaskdoc")
def flaskdoc():
    pass


@click.command(name="start")
def start_examples():
    run_examples()


flaskdoc.add_command(start_examples)


if __name__ == "__main__":
    flaskdoc(sys.argv[1:])
