from typing import Dict


class NotRecordFound(Exception):
    def __init__(self, filter_by: Dict[str, str]) -> None:
        super().__init__(*filter_by)
