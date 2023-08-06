from typing import Mapping, Sequence
from tinybones.columns import Columns
from tinybones.rows import Rows


DataMapping = Mapping[str, Sequence]


class Table:
    def __init__(self, data: DataMapping) -> None:
        self.data = data