import pathlib
import shutil
from os import listdir
from os.path import isfile, join

import typer
from dotenv import load_dotenv

from kclii.database.database import Base, engine
from kclii.modules.profiles import profiles
import kclii.modules.profiles.models

load_dotenv()
app = typer.Typer(pretty_exceptions_enable=False)
app.add_typer(profiles.app, name="profile")


@app.command()
def init():
    print("Init configurations")
    current_path = pathlib.Path().resolve()
    files = [
        f
        for f in listdir(f"{current_path}/bin")
        if isfile(join(f"{current_path}/bin", f))
    ]

    for file in files:
        shutil.copyfile(f"{current_path}/bin/{file}", "/usr/local/bin")


@app.command()
def hello(name: str = ""):
    print(f"Welcome sr! {name}")


@app.command()
def version() -> None:
    print("0.1.2")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app()
