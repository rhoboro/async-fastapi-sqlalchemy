from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from .base import Base

if TYPE_CHECKING:
    from .notes import Note


class Notebook(Base):
    __tablename__ = "notebooks"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    title: Mapped[str] = mapped_column("title", String(length=64), nullable=False)

    notes: Mapped[list[Note]] = relationship(
        "Note",
        back_populates="notebook",
        order_by="Note.id",
        cascade="save-update, merge, refresh-expire, expunge, delete, delete-orphan",
    )

    @classmethod
    async def read_all(cls, session: AsyncSession, include_notes: bool) -> AsyncIterator[Notebook]:
        stmt = select(cls)
        if include_notes:
            stmt = stmt.options(selectinload(cls.notes))
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_id(
        cls, session: AsyncSession, notebook_id: int, include_notes: bool = False
    ) -> Notebook | None:
        stmt = select(cls).where(cls.id == notebook_id)
        if include_notes:
            stmt = stmt.options(selectinload(cls.notes))
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def create(cls, session: AsyncSession, title: str, notes: list[Note]) -> Notebook:
        notebook = Notebook(
            title=title,
            notes=notes,
        )
        session.add(notebook)
        await session.flush()
        # To fetch notes
        new = await cls.read_by_id(session, notebook.id, include_notes=True)
        if not new:
            raise RuntimeError()
        return new

    async def update(self, session: AsyncSession, title: str, notes: list[Note]) -> None:
        self.title = title
        self.notes = notes
        await session.flush()

    @classmethod
    async def delete(cls, session: AsyncSession, notebook: Notebook) -> None:
        await session.delete(notebook)
        await session.flush()
