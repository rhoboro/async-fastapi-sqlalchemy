from __future__ import annotations

from typing import AsyncIterator, Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload

from .base import Base


class Notebook(Base):
    __tablename__ = "notebooks"

    id: int = Column(
        "id", Integer(), autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    title: str = Column("title", String(length=64), nullable=False)

    notes: list[Note] = relationship(
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
        stream = await session.stream(stmt.order_by(cls.id))
        async for row in stream:
            yield row.Notebook

    @classmethod
    async def read_by_id(
        cls, session: AsyncSession, notebook_id: int, include_notes: bool = False
    ) -> Optional[Notebook]:
        stmt = select(cls).where(cls.id == notebook_id)
        if include_notes:
            stmt = stmt.options(selectinload(cls.notes))
        result = (await session.execute(stmt.order_by(cls.id))).first()
        if result:
            return result.Notebook
        else:
            return None

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


class NotebookSchema(BaseModel):
    id: int
    title: str
    notes: list[NoteSchema]

    class Config:
        orm_mode = True


from .notes import Note, NoteSchema  # noqa: E402

NotebookSchema.update_forward_refs()
