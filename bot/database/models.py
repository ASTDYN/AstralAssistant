from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Member(Base):
    __tablename__ = "members"

    discord_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    guild_id: Mapped[int | None] = mapped_column(BigInteger)
    rsi_username: Mapped[str | None] = mapped_column(String(64))
    timezone: Mapped[str | None] = mapped_column(String(64))
    gameplay_style: Mapped[str | None] = mapped_column(String(32))
    recruiter_id: Mapped[int | None] = mapped_column(BigInteger)
    verification_code: Mapped[str | None] = mapped_column(String(16))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    applied_to_org: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GuildRole(Base):
    __tablename__ = "guild_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    role_name: Mapped[str] = mapped_column(String(64))
    role_id: Mapped[int] = mapped_column(BigInteger)
