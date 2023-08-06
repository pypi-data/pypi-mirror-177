from typing import Literal

JSON_VALUES = int | str | float | bool | list | dict | None     # type for json value.
JSON = dict[str, JSON_VALUES]                                   # json type.
Stars = Literal[1, 2, 3, 4, 5]                                  # star value of student.
