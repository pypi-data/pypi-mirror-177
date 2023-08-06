import click
from .scripts.sync import sync
from .scripts.doctor import doctor


@click.group(help="Michael\'s fun utilities")
def cli():
    pass


cli.add_command(sync)
cli.add_command(doctor)