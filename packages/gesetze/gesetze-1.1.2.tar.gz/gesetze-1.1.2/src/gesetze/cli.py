"""
This module is part of the 'py-gesetze' package,
which is released under GPL-3.0-only license.
"""

from os import getcwd
from shutil import rmtree

import click

from .helpers import analyze as analyze_norm
from .scrapers import Buzer, DejureOnline, GesetzeImInternet, Lexparency


@click.group()
@click.pass_context
@click.option("-v", "--verbose", count=True, help="Enable verbose mode.")
@click.version_option("1.1.2")
def cli(ctx, verbose: int) -> None:
    """
    Utilities for indexing & analyzing german legal norms
    """

    # Ensure context object exists & is dictionary
    ctx.ensure_object(dict)

    # Initialize context object & assign verbose mode
    ctx.obj = {"verbose": verbose}


@cli.command()
@click.pass_context
@click.option("-p", "--provider", multiple=True, help="Provider for legal norms.")
@click.option("-d", "--directory", type=click.Path(True), help="Target directory.")
@click.option("-w", "--wait", default=3, help="Time between requests (in seconds).")
def build(ctx, provider: tuple, directory: click.Path, wait: int) -> None:
    """
    Builds index
    """

    if ctx.obj["verbose"] > 0:
        click.echo(f'Selected waiting time: "{wait}"')

    if not directory:
        if ctx.obj["verbose"] > 0:
            click.echo("No directory selected, using fallback ..")

        directory = getcwd()

    if ctx.obj["verbose"] > 0:
        click.echo(f'Selected target directory: "{directory}"')

    databases = [
        {
            "driver": ["buz", "buzer"],
            "class": Buzer,
            "url": "buzer.de",
        },
        {
            "driver": ["djo", "dejure"],
            "class": DejureOnline,
            "url": "dejure.org",
        },
        {
            "driver": ["gii", "gesetze"],
            "class": GesetzeImInternet,
            "url": "gesetze-im-internet.de",
        },
        {
            "driver": ["lex", "lexparency"],
            "class": Lexparency,
            "url": "lexparency.de",
        },
    ]

    # Iterate over providers ..
    for database in databases:
        # .. but skip invalid ones
        if provider and not list(set(provider) & set(database["driver"])):
            continue

        if ctx.obj["verbose"] > 0:
            click.echo(f'Current database: "{database["url"]}" ..')

        driver = database["class"](click.get_app_dir("gesetze"))

        output_file = f"{directory}/{driver.identifier}.json"

        if ctx.obj["verbose"] > 0:
            click.echo(f'Saving data in file "{output_file}" ..')

        driver.scrape(output_file, wait)


@cli.command()
@click.pass_context
def clear(ctx) -> None:
    """
    Clears download cache
    """

    if ctx.obj["verbose"] > 0:
        click.echo("Clearing cache ..", nl=False)

    rmtree(click.get_app_dir("gesetze"))

    if ctx.obj["verbose"] > 0:
        click.echo(" done.")


@cli.command()
@click.pass_context
@click.argument("norm", type=str, nargs=-1)
def analyze(ctx, norm) -> None:
    """
    Analyzes legal NORM
    """

    if ctx.obj["verbose"] > 0:
        click.echo("Analyzing input ..", nl=False)

    result = analyze_norm(" ".join(norm))

    if ctx.obj["verbose"] > 0:
        click.echo(" done.")

    for key, value in result.items():
        click.echo(f"{key.capitalize()}: {value}")
