from __future__ import annotations

from typing import TYPE_CHECKING, AsyncIterator

from sqlalchemy import ForeignKey, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship

if TYPE_CHECKING:
    from .notebooks import Notebook

from .base import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    title: Mapped[str] = mapped_column("title", String(length=64), nullable=False)
    content: Mapped[str] = mapped_column("content", nullable=False, default="")

    notebook_id: Mapped[int] = mapped_column(
        "notebook_id", ForeignKey("notebooks.id"), nullable=False
    )

    notebook: Mapped[Notebook] = relationship("Notebook", back_populates="notes")

    @hybrid_property
    def notebook_title(self) -> str:
        return self.notebook.title

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[Note]:
        stmt = select(cls).options(joinedload(cls.notebook, innerjoin=True))
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def read_by_id(cls, session: AsyncSession, note_id: int) -> Note | None:
        stmt = select(cls).where(cls.id == note_id).options(joinedload(cls.notebook))
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def read_by_ids(cls, session: AsyncSession, note_ids: list[int]) -> AsyncIterator[Note]:
        stmt = (
            select(cls)
            .where(cls.id.in_(note_ids))  # type: ignore
            .options(joinedload(cls.notebook))
        )
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def create(
        cls, session: AsyncSession, notebook_id: int, title: str, content: str
    ) -> Note:
        note = Note(title=title, content=content, notebook_id=notebook_id)
        session.add(note)
        await session.flush()

        # To fetch notebook
        new = await cls.read_by_id(session, note.id)
        if not new:
            raise RuntimeError()
        return new

    async def update(
        self, session: AsyncSession, notebook_id: int, title: str, content: str
    ) -> None:
        self.notebook_id = notebook_id
        self.title = title
        self.content = content
        await session.flush()

    @classmethod
    async def delete(cls, session: AsyncSession, note: Note) -> None:
        await session.delete(note)
        await session.flush()
