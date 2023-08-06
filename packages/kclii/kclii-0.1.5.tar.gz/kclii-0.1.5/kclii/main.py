import os

import typer
from dotenv import load_dotenv

from kclii.database.database import Base, engine
from kclii.modules.profiles import profiles
from kclii.scripts.scripts import install_scripts

import kclii.modules.profiles.models

load_dotenv()
app = typer.Typer(pretty_exceptions_enable=False)
app.add_typer(profiles.app, name="profile")


@app.command()
def init():
    print("Init configurations")
    install_scripts()


@app.command()
def hello(name: str = ""):
    print(f"Welcome sr! {name}")


@app.command()
def version() -> None:
    print("0.1.5")


if __name__ == "__main__":
    if os.getuid() != 0:
        Base.metadata.create_all(engine)
    app()
