from os import system as run
from typing import List
import typer


from compose_companion.configurations import Configurations


def container_up(
    container: str, recreate: bool = typer.Option(False, "--recreate", "-r")
):
    scripts = Configurations().scripts
    compose_file = Configurations().compose_file

    if scripts.get("x-before-up", {}).get(container):
        for script in scripts["x-before-up"][container]:
            run(script)

    run(
        f"docker compose -f {compose_file} up -d {container} --force-recreate={recreate}"
    )

    if scripts.get("x-after-up", {}).get(container):
        for script in scripts["x-after-up"][container]:
            run(script)


def server_up(recreate: bool):
    scripts = Configurations().scripts
    compose_file = Configurations().compose_file

    if scripts.get("x-before-up"):
        for script_list in scripts["x-before-up"].values():
            for script in script_list:
                run(script)

    run(f"docker compose -f {compose_file} up -d --force-recreate={recreate}")

    if scripts.get("x-after-up"):
        for script_list in scripts["x-after-up"].values():
            for script in script_list:
                run(script)


def container_down(container: str):
    scripts = Configurations().scripts
    compose_file = Configurations().compose_file

    if scripts.get("x-before-down", {}).get(container):
        for script in scripts["x-before-down"][container]:
            run(script)

    run(f"docker compose -f {compose_file} rm -sf {container}")

    if scripts.get("x-after-down", {}).get(container):
        for script in scripts["x-after-down"][container]:
            run(script)


def server_down():
    scripts = Configurations().scripts
    compose_file = Configurations().compose_file

    if scripts.get("x-before-down"):
        for script_list in scripts["x-before-down"].values():
            for script in script_list:
                run(script)
    print()

    run(f"docker compose -f {compose_file} down")
    print()

    if scripts.get("x-after-down"):
        for script_list in scripts["x-after-down"].values():
            for script in script_list:
                run(script)
    print()


def container_pause(container: str):
    compose_file = Configurations().compose_file
    run(f"docker compose -f {compose_file} stop {container}")


def server_pause():
    compose_file = Configurations().compose_file
    run(f"docker compose -f {compose_file} stop")
