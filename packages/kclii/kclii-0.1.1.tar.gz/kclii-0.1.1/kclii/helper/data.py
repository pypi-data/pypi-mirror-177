from typing import List, Union

from rich import print  # pylint: disable=W0622
from rich.prompt import Prompt
from rich.panel import Panel

STOPS_WORDS = ["stop", "Stop", "STOP", "exit", "Exit"]


def request_value(
    message: str,
    description: str = "",
    example: str = "",
    rules: str = " - ",
    multiple: bool = False,
    key_value: bool = False,
) -> Union[List[str], str, List[dict]]:

    text = f"""
[yellow]Description[/yellow]: {description}
[yellow]Example[/yellow]: {example}
[yellow]Rules[/yellow]: {rules}
        """
    print(Panel(text, title=message))

    data = []
    while True:
        if key_value:
            key = Prompt.ask(f"> {message} [Key]")
            if _is_stop(value=key):
                break
            value = Prompt.ask(f"> {message} [Value]")

            data.append({key: value})

        else:
            value = Prompt.ask(f"{message} [Value]")
            if _is_stop(value=value):
                break

            data.append(value)

        if not multiple:
            return data[0]

    return data


def _is_stop(value: str) -> bool:
    if value in STOPS_WORDS:
        return True
    return False
