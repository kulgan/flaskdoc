import sys

import click

from flaskdoc.examples.app import run_examples


@click.group(name="flaskdoc")
def flaskdoc():
    pass


@click.command(name="start")
@click.option(
    "--name",
    "-n",
    type=click.Choice(
        ["inventory", "petstore", "all", "mocks", "api-with-examples", "link-example"],
        case_sensitive=False,
    ),
    default="inventory",
)
def start_examples(name):
    run_examples(example=name)


flaskdoc.add_command(start_examples)


if __name__ == "__main__":
    flaskdoc(sys.argv[1:])
