import os
from typing import List, Tuple, Optional

import typer
from rich.console import Console
from rich.table import Table

from kclii.consts.envs import K_DEFAULT_PROFILE
from kclii.helper.message import new_message
from kclii.helper.data import request_value
from kclii.envs.envs import set_env
from .core import EnvironmentVariablesIn, ProfileCoreIn
from .repository import Repository


TITLE = "👤 Profile"

app = typer.Typer()
repository = Repository()
console = Console()


def request_profile_data(
    skip_name: Optional[bool] = False,
    skip_environment_variables: Optional[bool] = False,
    force: Optional[bool] = False,
) -> Tuple[str, List[EnvironmentVariablesIn]]:
    current_profile = os.getenv(K_DEFAULT_PROFILE)

    if current_profile and not force:
        name = current_profile
    elif not skip_name:
        name = request_value(
            message="Profile name",
            description="Type the profile name should be unique",
            example="company",
        )
    else:
        name = ""

    if not skip_environment_variables:
        environment_variables = request_value(
            description="Add all the environments variables you need to this profile.",
            message="Environment Variables",
            example="MY_TOKEN=thisismyawesometoken!",
            rules="Once you finish please type stop",
            multiple=True,
            key_value=True,
        )

        environment_variables = [
            EnvironmentVariablesIn(key=list(env.keys())[0], value=list(env.values())[0])
            for env in environment_variables
        ]
    else:
        environment_variables = []

    return name, environment_variables


def print_list_environment_variables_by_profile(name: str) -> None:
    saved_profile = repository.get_profile_by_name(name=name)
    saved_environment_variables = repository.get_environment_variables_by_profile(
        profile_id=saved_profile.id
    )

    table = Table("ID", "Name", "Value")
    for saved_environment_variable in saved_environment_variables:

        table.add_row(
            str(saved_environment_variable.id),
            saved_environment_variable.key,
            saved_environment_variable.value,
        )

    console.print(table)


def print_list_profiles() -> None:
    saved_profiles = repository.get_all()

    table = Table("ID", "Name", "CreatedAt")
    for saved_profile in saved_profiles:

        table.add_row(
            str(saved_profile.id),
            saved_profile.name,
            str(saved_profile.created_at),
        )

    console.print(table)


@app.command()
def new() -> None:
    new_message(
        title=TITLE,
        status="info",
        title_type="bold",
        message="Create a new profile",
    )
    name, environment_variables = request_profile_data(force=True)
    profile = ProfileCoreIn(name=name, environment_variables=environment_variables)
    saved_profile = repository.create_profile(profile=profile)
    repository.add_environment_variables(
        profile_id=saved_profile.id, environment_variables=profile.environment_variables
    )


@app.command()
def update(add: Optional[bool] = False, delete: Optional[bool] = False) -> None:

    if add:
        new_message(
            title=TITLE,
            status="info",
            title_type="bold",
            message="Add environment variables",
        )
        name, environment_variables = request_profile_data()
        saved_profile = repository.get_profile_by_name(name=name)
        repository.add_environment_variables(
            profile_id=saved_profile.id, environment_variables=environment_variables
        )

    if delete:
        new_message(
            title=TITLE,
            status="info",
            title_type="bold",
            message="Delete environment variables",
        )
        name, _ = request_profile_data(skip_environment_variables=True)
        print_list_environment_variables_by_profile(name=name)
        delete_ids = input("Choose all the ids you want to delete (13,15,19): ")
        delete_ids = [int(id) for id in delete_ids.split(",")]
        repository.delete_environment_variables(delete_ids=delete_ids)


@app.command()
def ls() -> None:
    new_message(
        title=TITLE,
        status="info",
        title_type="bold",
        message="List all profiles",
    )

    print_list_profiles()


@app.command()
def ls_env() -> None:
    new_message(
        title=TITLE,
        status="info",
        title_type="bold",
        message="List all environment variables by pofile",
    )

    name, _ = request_profile_data(skip_environment_variables=True)
    print_list_environment_variables_by_profile(name=name)


@app.command("set")
def _set(name: str) -> None:
    saved_profile = repository.get_profile_by_name(name=name)
    new_message(
        title=TITLE,
        status="success",
        title_type="bold",
        message=f"{saved_profile.name} ACTIVE",
    )
    variables_to_set = [f"{K_DEFAULT_PROFILE}={saved_profile.name}\n"]

    for environment_variables in saved_profile.environment_variables:
        variables_to_set.append(
            f"{environment_variables.key}={environment_variables.value}\n"
        )

    set_env(values=variables_to_set)


@app.command()
def current() -> None:
    print(os.getenv(K_DEFAULT_PROFILE))
