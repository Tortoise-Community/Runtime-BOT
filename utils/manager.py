import asyncpg

class Database:

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(self.dsn)

    async def close(self):
        if self.pool:
            await self.pool.close()

class RuntimeManager:
    def __init__(self, db: Database):
        self.db = db
        self.cache: dict[int, bool] = {}

    async def setup(self):
        await self.db.pool.execute(
            """
            CREATE TABLE IF NOT EXISTS runtime_config (
                guild_id BIGINT PRIMARY KEY,
                enabled  BOOLEAN NOT NULL DEFAULT TRUE
            )
            """
        )

    async def load_cache(self):
        rows = await self.db.pool.fetch(
            "SELECT guild_id, enabled FROM runtime_config"
        )
        self.cache = {r["guild_id"]: r["enabled"] for r in rows}

    def is_enabled(self, guild_id: int) -> bool:
        return self.cache.get(guild_id, True)

    async def set_enabled(self, guild_id: int, value: bool):
        await self.db.pool.execute(
            """
            INSERT INTO runtime_config (guild_id, enabled)
            VALUES ($1, $2)
            ON CONFLICT (guild_id)
            DO UPDATE SET enabled = EXCLUDED.enabled
            """,
            guild_id,
            value,
        )
        self.cache[guild_id] = value