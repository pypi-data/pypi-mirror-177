from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator, Awaitable, Iterable, Sequence

import asyncpg
from asyncpg.cursor import CursorFactory

from .connection import Connection, Pool
from .exceptions import NoMigrationsToCreate
from .indexes import Index
from .migrations import describe
from .migrations.applied_migration import AppliedMigration
from .migrations.apply_migration import apply_migration
from .migrations.create_migration import create_next_migration
from .migrations.migration import Migration
from .model import Model
from .utils.lazy_list import LazyList


class Database:
    """Base database class. You must subclass this, as
    all tables and indexes are stored as classvars.

    Example:
    ```
    class MyDatabase(Database):
        users = User
        games = Game
        players = Players

        indexes = [SomeIndex, SomeOtherIndex]
    ```
    """

    __slots__: Iterable[str] = (
        "_all_models",
        "_migrations_folder",
        "pool",
        "_migrations",
        "default_padding",
    )

    _migrations: type[AppliedMigration]
    """Internal table to track applied migrations."""
    _all_models: list[type[Model]]
    """A list of all models on this database."""

    indexes: Sequence[Index] | None = None
    """A list of indexes for the database."""

    def __init_subclass__(cls) -> None:
        cls._migrations = AppliedMigration
        cls._all_models = []

        for attr_name, model in cls.__dict__.items():
            if not (isinstance(model, type) and issubclass(model, Model)):
                continue

            model.tablename = attr_name
            cls._all_models.append(model)

    def __init__(
        self, migrations_folder: Path | str, padding: int = 4
    ) -> None:
        """Initialize the database.

        Args:
            migrations_folder (pathlib.Path): The folder in which migrations
            are/will be stored.
        """

        self._migrations_folder = (
            Path(migrations_folder)
            if isinstance(migrations_folder, str)
            else migrations_folder
        )

        for model in self._all_models:
            model.database = self

        self.default_padding = padding
        self.pool: Pool | None = None

    # migration functions
    def describe(self) -> describe.Describe:
        """Return the description of the database.

        Returns:
            describe.Describe: The description.
        """

        return describe.Describe(
            tables=[m._describe() for m in self._all_models],
            indexes=[i._describe() for i in self.indexes or []],
        )

    def load_all_migrations(self) -> list[Migration]:
        """Load all migrations and return them.

        Returns:
            list[Migration]: The migrations.
        """

        return Migration._load_all_migrations(self._migrations_folder)

    def load_last_migration(self) -> Migration | None:
        """Loads and returns the most recent migration, if any.

        Returns:
            Migration | None: The migration.
        """

        return Migration._load_last_migration(self._migrations_folder)

    def load_migration_from_id(self, migration_id: int) -> Migration:
        """Loads a migration from its id.

        Args:
            migration_id (int): The id of the migration.

        Returns:
            Migration: The migration.
        """

        return Migration._from_path(
            Migration._path_from_id(
                migration_id, self._migrations_folder, self.default_padding
            )
        )

    def must_create_migrations(self) -> bool:
        """Whether or not you need to call Database.create_migrations()

        Returns:
            bool
        """

        sql = self._create_next_migration()
        return sql is not None

    def create_migrations(self, allow_empty: bool = False) -> Migration:
        """Create migrations.

        Args:
            allow_empty (bool): Whether to allow the migration to be empty
            (useful for creating custom migrations).

        Raises:
            NoMigrationsToCreate: Migrations do not creating.

        Returns:
            Migration: The created migration.
        """

        if (not self.must_create_migrations()) and not allow_empty:
            raise NoMigrationsToCreate
        sql = self._create_next_migration() or ""
        return Migration._create_migration(
            self.describe(), sql, self._migrations_folder, self.default_padding
        )

    async def load_unapplied_migrations(self) -> list[Migration]:
        """Returns a list of migrations that have not been applied on the
        current database.

        Returns:
            list[Migration]: The unapplied migrations.
        """

        try:
            applied = [
                m.id_ for m in await self._migrations.fetch_query().fetchmany()
            ]
        except asyncpg.UndefinedTableError:
            applied = []
        return [
            m
            for m in self.load_all_migrations()
            if m.migration_id not in applied
        ]

    async def must_apply_migrations(self) -> bool:
        """Whether or not there are migrations that need to be applied.

        Returns:
            bool
        """

        return len(await self.load_unapplied_migrations()) > 0

    async def apply_migrations(self) -> None:
        """Applies all migrations that need to be applied."""

        unapplied = await self.load_unapplied_migrations()
        unapplied.sort(key=lambda m: m.migration_id)
        for m in unapplied:
            await self._apply_migration(m)

    # database functions
    async def connect(self, **connect_kwargs: Any) -> None:
        """Connect to a database. Any kwargs that can be passed to
        asyncpg.create_pool() can be used here.
        """

        self.pool = Pool(await asyncpg.create_pool(**connect_kwargs))

    async def cleanup(self, timeout: float = 30) -> None:
        """Close the connection.

        Args:
            timeout (float): The maximum time pool.close() has. Defaults to 30.

        Raises:
            TimeoutError: The operation timed out.
        """

        if self.pool is not None:
            await asyncio.wait_for(self.pool.close(), timeout=timeout)

    async def execute(self, query: str, params: list[Any]) -> None:
        """Execute SQL within a transaction."""

        assert self.pool is not None
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(query, params)

    async def fetchrow(
        self, query: str, params: list[Any]
    ) -> dict[str, Any] | None:
        """Fetch the first matching row.

        Returns:
            dict | None: The row, if any.
        """

        assert self.pool is not None
        async with self.pool.acquire() as con:
            async with con.transaction():
                return await con.fetchrow(query, params)

    async def fetchmany(
        self, query: str, params: list[Any]
    ) -> LazyList[asyncpg.Record, dict[str, Any]]:
        """Fetch all matching rows.

        Returns:
            LazyList[asyncpg.Record, dict]: All matching rows.
        """

        assert self.pool is not None
        async with self.pool.acquire() as con:
            async with con.transaction():
                return await con.fetchmany(query, params)

    async def fetchval(self, query: str, params: list[Any]) -> Any:
        """Fetch a single value."""

        assert self.pool is not None
        async with self.pool.acquire() as con:
            async with con.transaction():
                return await con.fetchval(query, params)

    @asynccontextmanager
    async def cursor(
        self, query: str, params: list[Any], con: Connection | None = None
    ) -> AsyncGenerator[CursorFactory, None]:
        """Yields a CursorFactory.

        Usage:
        ```
        async with db.cursor(query, args) as cursor:
            async for res in cursor:
                print(res)
        ```
        """

        if con:
            yield con.cursor(query, params)

        else:
            assert self.pool is not None
            async with self.pool.acquire() as con:
                async with con.transaction():
                    yield con.cursor(query, params)

    def _create_next_migration(self) -> str | None:
        return create_next_migration(self.describe(), self._migrations_folder)

    def _apply_migration(self, migration: Migration) -> Awaitable[None]:
        return apply_migration(migration, self)
