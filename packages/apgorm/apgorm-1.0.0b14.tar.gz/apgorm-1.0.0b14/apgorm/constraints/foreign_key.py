from __future__ import annotations

from enum import Enum
from typing import Any, Iterable, Sequence
from typing import cast as typingcast

from apgorm.exceptions import BadArgument
from apgorm.field import BaseField
from apgorm.sql.sql import Block, join, raw

from .constraint import Constraint


class ForeignKeyAction(Enum):
    """Action for ON UPDATE or ON DELETE of ForeignKey."""

    CASCADE = "CASCADE"
    """Carry the changes"""
    RESTRICT = "RESTRICT"
    """Prevent the changes"""
    NO_ACTION = "NO ACTION"
    """Do nothing"""


class ForeignKey(Constraint):
    __slots__: Iterable[str] = (
        "fields",
        "ref_fields",
        "ref_table",
        "match_full",
        "on_delete",
        "on_update",
    )

    def __init__(
        self,
        fields: Sequence[Block[Any] | BaseField[Any, Any, Any] | str]
        | Block[Any]
        | BaseField[Any, Any, Any]
        | str,
        ref_fields: Sequence[Block[Any] | BaseField[Any, Any, Any] | str]
        | Block[Any]
        | BaseField[Any, Any, Any]
        | str,
        ref_table: Block[Any] | str | None = None,
        match_full: bool = False,
        on_delete: ForeignKeyAction = ForeignKeyAction.CASCADE,
        on_update: ForeignKeyAction = ForeignKeyAction.CASCADE,
    ) -> None:
        """Specify a ForeignKey constraint for a table.

        Args:
            fields (Sequence[Block | BaseField]): A list of fields or raw
            field names on the current table.
            ref_fields (Sequence[Block | BaseField]): A list of fields or raw
            field names on the referenced table.
            ref_table (Block, optional): If all of `ref_fields` are `Block`,
            specify the raw tablename of the referenced table. Defaults to
            None.
            match_full (bool, optional): Whether or not a full match is
            required. If False, MATCH SIMPLE is used instead. Defaults to
            False.
            on_delete (Action, optional): The action to perform if the
            referenced row is deleted. Defaults to Action.CASCADE.
            on_update (Action, optional): The action to perform if the
            referenced row is updated. Defaults to Action.CASCADE.

        Raises:
            BadArgument: Bad arguments were sent to ForeignKey.
        """

        self.fields: Sequence[BaseField[Any, Any, Any] | Block[Any]] = [
            raw(f) if isinstance(f, str) else f
            for f in (fields if isinstance(fields, Sequence) else [fields])
        ]
        self.ref_fields: Sequence[BaseField[Any, Any, Any] | Block[Any]] = [
            raw(f) if isinstance(f, str) else f
            for f in (
                ref_fields
                if isinstance(ref_fields, Sequence)
                else [ref_fields]
            )
        ]
        self.ref_table = (
            raw(ref_table) if isinstance(ref_table, str) else ref_table
        )
        self.match_full = match_full
        self.on_delete = on_delete
        self.on_update = on_update

        if len(self.ref_fields) != len(self.fields):
            raise BadArgument(
                "Must have same number of fields and ref_fields."
            )

        if not self.fields:
            raise BadArgument("Must specify at least on field and ref_field.")

    def _creation_sql(self) -> Block[Any]:

        if (
            len(
                {
                    f.model.tablename
                    for f in self.ref_fields
                    if isinstance(f, BaseField)
                }
            )
            > 1
        ):
            raise BadArgument(
                "All fields in ref_fields must be of the same table."
            )

        if self.ref_table is None:
            _ref_fields = self.ref_fields
            if not all(isinstance(f, BaseField) for f in _ref_fields):
                raise BadArgument(
                    "ref_fields must either all be BaseFields or "
                    "ref_table must be specified."
                )
            _ref_fields = typingcast(
                Sequence[BaseField[Any, Any, Any]], _ref_fields
            )

            ref_table = raw(_ref_fields[0].model.tablename)

        else:
            ref_table = self.ref_table

        ref_fields = (
            raw(f.name) if isinstance(f, BaseField) else f
            for f in self.ref_fields
        )
        fields = (
            raw(f.name) if isinstance(f, BaseField) else f for f in self.fields
        )

        return Block(
            raw("CONSTRAINT"),
            raw(self.name),
            raw("FOREIGN KEY ("),
            join(raw(","), *fields),
            raw(") REFERENCES"),
            ref_table,
            raw("("),
            join(raw(","), *ref_fields),
            raw(") MATCH"),
            raw("FULL" if self.match_full else "SIMPLE"),
            raw(f"ON DELETE {self.on_delete.value}"),
            raw(f"ON UPDATE {self.on_update.value}"),
            wrap=True,
        )
