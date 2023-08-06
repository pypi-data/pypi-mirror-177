import typer
from rich import print

from pyxrayc import __version__

# Central CLI app to group other typer apps together
app = typer.Typer(name="PyXrayC", help="Managing Xray VPN servers made easy!")


def version_callback(value: bool) -> None:
    if value:
        print(f"[bold cyan]PyXrayC version[/]: [red]{__version__}[/]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(  # noqa
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the PyXrayC version number.",
    ),
) -> None:
    ...
