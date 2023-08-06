from importlib import metadata

import typer

app = typer.Typer()
__version__ = metadata.version(__package__)


def version_callback(value: bool) -> None:
    if value:
        print(__version__)
        raise typer.Exit()


@app.callback()
def callback(
    _: bool = typer.Option(None, "--version", "-v", callback=version_callback)
) -> None:
    """My app description"""


@app.command()
def hello(
    name: str = typer.Argument(default="World", help="The person to greet.")
) -> None:
    """Say hello to NAME"""
    emoji = "🌎" if name == "World" else "👋"
    typer.echo(f"Hello {name}! {emoji}")
