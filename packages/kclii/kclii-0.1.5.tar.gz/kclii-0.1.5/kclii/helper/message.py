from rich import print  # pylint: disable=W0622


def get_status_color(status: str) -> str:
    if status == "success":
        return "green"
    if status == "danger":
        return "red"
    if status == "info":
        return "#00d8ff"


def create_title(title: str, status: str, title_type: str) -> str:
    if not title:
        return ""

    beauty_title = f"[ {title} ]: "

    if status or title_type:
        need_space = " " if title_type else ""
        title_tag_start = f"[{title_type}{need_space}{get_status_color(status=status)}]"
        title_tag_end = title_tag_start[0] + "/" + title_tag_start[1::]

        beauty_title = f"{title_tag_start}{beauty_title}{title_tag_end}"

    return beauty_title


def new_message(
    message: str, title: str = "", status: str = "", title_type: str = ""
) -> None:
    title = create_title(title=title, status=status, title_type=title_type)
    print(f"{title}{message}")
