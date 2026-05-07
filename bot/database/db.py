from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import select

from database.models import Base, Member, GuildRole
from config import DATABASE_URL


class Database:
    def __init__(self) -> None:
        url = (
            DATABASE_URL
            .replace("postgresql://", "postgresql+asyncpg://")
        )
        self.engine = create_async_engine(url, pool_pre_ping=True)
        self.session_factory = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def initialize(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # ─── Member operations ────────────────────────────────────────────────────

    async def get_member(self, discord_id: int) -> Member | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(Member).where(Member.discord_id == discord_id)
            )
            return result.scalar_one_or_none()

    async def upsert_member(self, discord_id: int, **kwargs) -> Member:
        async with self.session_factory() as session:
            result = await session.execute(
                select(Member).where(Member.discord_id == discord_id)
            )
            member = result.scalar_one_or_none()
            if member is None:
                member = Member(discord_id=discord_id, **kwargs)
                session.add(member)
            else:
                for key, value in kwargs.items():
                    setattr(member, key, value)
            await session.commit()
            await session.refresh(member)
            return member

    # ─── Role operations ──────────────────────────────────────────────────────

    async def get_role(self, guild_id: int, role_name: str) -> GuildRole | None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(GuildRole).where(
                    GuildRole.guild_id == guild_id,
                    GuildRole.role_name == role_name,
                )
            )
            return result.scalar_one_or_none()

    async def upsert_role(self, guild_id: int, role_name: str, role_id: int) -> None:
        async with self.session_factory() as session:
            result = await session.execute(
                select(GuildRole).where(
                    GuildRole.guild_id == guild_id,
                    GuildRole.role_name == role_name,
                )
            )
            guild_role = result.scalar_one_or_none()
            if guild_role is None:
                session.add(GuildRole(guild_id=guild_id, role_name=role_name, role_id=role_id))
            else:
                guild_role.role_id = role_id
            await session.commit()
