from __future__ import annotations

from typing import Iterable

from .base_type import SqlType


class VarChar(SqlType[str]):
    """Variable length string with limit.

    Args:
        max_length (int, optional): The maximum length of the string. If
        None, any length will be accepted. Defaults to None.

    https://www.postgresql.org/docs/14/datatype-character.html
    """

    __slots__: Iterable[str] = ("_max_length",)

    def __init__(self, max_length: int | None = None) -> None:
        self._max_length = max_length
        self._sql = "VARCHAR"
        if max_length is not None:
            self._sql += f"({max_length})"

    @property
    def max_length(self) -> int | None:
        """The maximum length of the VarChar type.

        Returns:
            int | None
        """

        return self._max_length


class Char(SqlType[str]):
    """Fixed length string. If a passed string is too short, it will be
    padded with spaces.

    Args:
        max_length (int, optional): The length of the string. If None,
        postgres will use 1. Defaults to None.

    https://www.postgresql.org/docs/14/datatype-character.html
    """

    def __init__(self, length: int | None = None) -> None:
        self._length = length
        self._sql = "CHAR"
        if length is not None:
            self._sql += f"({length})"

    @property
    def length(self) -> int | None:
        """The length of the string.

        Returns:
            int | None
        """

        return self._length


class Text(SqlType[str]):
    """Variable unlimited length string.

    https://www.postgresql.org/docs/14/datatype-character.html
    """

    _sql = "TEXT"
