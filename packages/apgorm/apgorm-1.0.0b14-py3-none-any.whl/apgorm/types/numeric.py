from __future__ import annotations

from decimal import Decimal
from typing import Iterable, TypeVar, Union

from apgorm.exceptions import BadArgument
from apgorm.field import Field

from .base_type import SqlType

INT = Union["SmallInt", "Int", "BigInt"]
"""All integral types (excluding serials)."""
FLOAT = Union["Real", "DoublePrecision", "Numeric"]
"""All floating-point types."""
SERIAL = Union["SmallSerial", "Serial", "BigSerial"]
"""All serial types."""

NUMBER = Union[INT, FLOAT, SERIAL]
"""All integral, floating-point, and serial types."""


class SmallInt(SqlType[int]):
    """Small integer, 2 bytes, -32768 to +32767.

    https://www.postgresql.org/docs/14/datatype-numeric.html
    """

    __slots__: Iterable[str] = ()

    _sql = "SMALLINT"


class Int(SqlType[int]):
    """Integer, 4 bytes, -2147483648 to +2147483647.

    https://www.postgresql.org/docs/14/datatype-numeric.html
    """

    __slots__: Iterable[str] = ()

    _sql = "INTEGER"


Integer = Int


class BigInt(SqlType[int]):
    """Big integer, 8 bytes, -9223372036854775808 to +9223372036854775807.

    https://www.postgresql.org/docs/14/datatype-numeric.html
    """

    __slots__: Iterable[str] = ()

    _sql = "BIGINT"


class Numeric(SqlType[Decimal]):
    """Numeric (AKA decimal) type with a user specified precision and scale.

    Up to 131072 digits before the decimal point and 16383 digits after.

    Args:
        precision (int, optional): The total number of significant digits
        (`55.55` has 4). Defaults to None.
        scale (int, optional): The total number of digits after the
        decimal. Specifying a precision without a scale sets the scale to
        0. Defaults to None.

    Raises:
        BadArgument: You tried to specify a scale without a precision.

    https://www.postgresql.org/docs/14/datatype-numeric.html
    """

    __slots__: Iterable[str] = ("_precision", "_scale")

    def __init__(
        self, precision: int | None = None, scale: int | None = None
    ) -> None:
        self._precision = precision
        self._scale = scale

        self._sql = "NUMERIC"

        if precision is not None and scale is not None:
            self._sql += f"({precision}, {scale})"
        elif precision is not None:
            self._sql += f"({precision})"
        elif scale is not None:
            raise BadArgument("Cannot specify scale without precision.")

    @property
    def precision(self) -> int | None:
        """The precision (total number of significant digits) of the type.

        Returns:
            int | None
        """

        return self._precision

    @property
    def scale(self) -> int | None:
        """The scale (digits after the decimal point) of the type.

        Returns:
            int | None
        """

        return self._scale


class Real(SqlType[float]):
    """4 byte floating-point number (inexact).

    https://www.postgresql.org/docs/14/datatype-numeric.html
    """

    __slots__: Iterable[str] = ()

    _sql = "REAL"


class DoublePrecision(SqlType[float]):
    """8 byte floating-point number (inexact).

    https://www.postgresql.org/docs/14/datatype-numeric.html
    """

    __slots__: Iterable[str] = ()

    _sql = "DOUBLE PRECISION"


_S = TypeVar("_S", bound="_BaseSerial", covariant=True)


class _BaseSerial(SqlType[int]):
    __slots__: Iterable[str] = ()

    def field(  # type: ignore
        self: _S, use_repr: bool = True
    ) -> Field[_S, int]:
        return Field(sql_type=self, not_null=True, use_repr=use_repr)

    def nullablefield(  # type: ignore
        self: _S, use_repr: bool = True
    ) -> Field[_S, int | None]:
        return Field(sql_type=self, not_null=False, use_repr=use_repr)


class SmallSerial(_BaseSerial):
    """Small autoincrementing integer. You cannot cast to this type.

    Accepts any value accepted by SmallInt, but the default values are
    positive only (starting at 1).

    https://www.postgresql.org/docs/14/datatype-numeric.html
    """

    __slots__: Iterable[str] = ()

    _sql = "SMALLSERIAL"


class Serial(_BaseSerial):
    """Autoincrementing integer. You cannot cast to this type.

    Accepts any value accepted by Int, but the default values are positive
    only (starting at 1).

    https://www.postgresql.org/docs/14/datatype-numeric.html
    """

    __slots__: Iterable[str] = ()

    _sql = "SERIAL"


class BigSerial(_BaseSerial):
    """Large autoincrementing integer. You cannot cast to this type.

    Accepts any value accepted by BigInt, but the default values are positive
    only (starting at 1).

    https://www.postgresql.org/docs/14/datatype-numeric.html
    """

    __slots__: Iterable[str] = ()

    _sql = "BIGSERIAL"
