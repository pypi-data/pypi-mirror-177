def set_env(values: str):
    with open("./.env", "w+", encoding="utf-8") as file:
        file.writelines(values)
