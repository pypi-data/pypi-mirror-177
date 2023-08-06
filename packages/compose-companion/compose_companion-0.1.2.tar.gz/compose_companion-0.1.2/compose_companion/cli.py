from os import system as run
from typing import List, Optional

import typer
from rich import print
from rich.table import Table
from rich.console import Console
from rich import box
from rich.panel import Panel
from pathlib import Path

from rich.console import Console

from compose_companion.configurations import Configurations

from compose_companion.functions import (
    container_down,
    container_pause,
    container_up,
    server_down,
    server_pause,
    server_up,
)

app = typer.Typer()
err_console = Console(stderr=True)


@app.command()
def up(
    targets: Optional[List[str]] = typer.Argument(
        None,
        help="Containers in which to run the command. If no targets are passed, runs for all containers.",
    ),
    recreate: bool = typer.Option(
        False,
        "--recreate",
        "-r",
        help="Recreates containers even if their configuration and image haven't changed. Toggles docker compose --force-recreate option.",
    ),
):
    """
    Starts up targeted containers.
    If no target is defined, starts all containers.
    Equivalent to `docker compose up -d`.
    """
    if not targets:
        server_up(recreate)
        return
    for container in targets:
        container_up(container, recreate)


@app.command()
def pause(
    targets: Optional[List[str]] = typer.Argument(
        None,
        help="Containers in which to run the command. If no targets are passed, runs for all containers.",
    ),
):
    """
    Pauses targeted containers.
    If no target is defined, pauses all containers.
    Equivalent to `docker compose stop`.
    """
    if not targets:
        server_pause()
        return
    for container in targets:
        container_pause(container)


@app.command()
def down(
    targets: Optional[List[str]] = typer.Argument(
        None,
        help="Containers in which to run the command. If no targets are passed, runs for all containers.",
    ),
    confirmation: bool = typer.Option(
        False,
        "-f",
        "--force",
        prompt="You're about to shut down your containers. Are you sure?",
        help="Skip confirmation prompt and run.",
    ),
):
    """
    Shuts down target containers.
    If no target is defined, shuts down all containers.
    Equivalent to `docker compose rm -sf` or `docker compose down`.
    """

    if not confirmation:
        return
    if not targets:
        server_down()
        return
    for container in targets:
        container_down(container)


@app.command()
def logs(
    targets: Optional[List[str]] = typer.Argument(
        None,
        help="Containers in which to run the command. If no targets are passed, runs for all containers.",
    ),
    detach: bool = typer.Option(
        False,
        "--detach",
        "-d",
        help="Print logs without following. Negates docker compose --follow/-f flag, which is used by default.",
    ),
    timestamps: bool = typer.Option(
        False,
        "--timestamps",
        "-t",
        help="Show timestamps. Toggles docker compose --timestamps/-t flag.",
    ),
):
    """
    Prints logs for target containers.
    If no target is defined, prints for all running ones.
    Equivalent to `docker compose logs -f`
    """
    compose_file = Configurations().compose_file

    if not targets:
        run(f"docker compose -f {compose_file} logs -f={not detach} -t={timestamps}")
        return
    run(
        f"docker compose -f {compose_file} logs {' '.join(targets)} -f={not detach} -t={timestamps}"
    )


@app.command()
def exec(
    target: str = typer.Argument(
        ...,
        help="The target container.",
    ),
    detach: Optional[bool] = typer.Option(
        False,
        "-d",
        "--detach",
        help="Detached mode: Run command in the background. Equivalent to docker compose -d flag.",
    ),
    command: Optional[List[str]] = typer.Argument(
        None,
        help="Command to be run. By default, runs `sh`.",
    ),
):
    """
    Runs command on the container.
    Equivalent to `docker compose exec`.
    """
    compose_file = Configurations().compose_file

    if not command:
        run(f"docker compose -f {compose_file} exec -d={detach} sh")
        return
    run(
        f"docker compose -f {compose_file} exec -d={detach} {target}  {' '.join(command)}"
    )


@app.command()
def config(
    key: Optional[str] = typer.Argument(
        None,
        help="Configuration key to view/set. If left blank, prints all the conf.",
    ),
    value: Optional[str] = typer.Argument(
        None,
        help="Value to set on the key. If key is passed but not value, current value for the config will be printed.",
    ),
):
    """
    View or change configurations.
    """
    conf = Configurations()

    if key and key in conf.config_keys:
        conf.set_config(key, value) if value else print(conf.get_config(key))
        return

    if key and key not in conf.config_keys:
        err_console.print(
            "Invalid Key. To view all available configurations run the command without any arguments.\n"
        )
        return

    grid = Table.grid(expand=True)
    grid.add_column("Key", style="cyan")
    grid.add_column("Value", style="magenta")
    for key in conf.config_keys:
        grid.add_row(
            key,
            conf.get_config(key),
        )

    panel = Panel(
        grid,
        title="Configurations",
        title_align="left",
        border_style="dim",
    )
    print(panel)


@app.callback(invoke_without_command=True)
def main():
    """
    A companion for Docker Compose.
    """
    Configurations()
