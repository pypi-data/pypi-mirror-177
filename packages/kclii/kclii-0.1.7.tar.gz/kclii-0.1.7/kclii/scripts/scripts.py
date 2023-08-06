from .kon import SCRIPT as kon
from .koff import SCRIPT as koff


def install_scripts() -> None:
    with open("/usr/local/bin/kon.sh", "w+") as file:
        file.write(kon)

    with open("/usr/local/bin/koff.sh", "w+") as file:
        file.write(koff)
