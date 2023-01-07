from fastapi import APIRouter, Depends, Path, Request

from app.models import NoteSchema

from .schema import (
    CreateNoteRequest,
    CreateNoteResponse,
    ReadAllNoteResponse,
    ReadNoteResponse,
    UpdateNoteRequest,
    UpdateNoteResponse,
)
from .use_cases import CreateNote, DeleteNote, ReadAllNote, ReadNote, UpdateNote

router = APIRouter(prefix="/notes")


@router.post("", response_model=CreateNoteResponse)
async def create(
    request: Request,
    data: CreateNoteRequest,
    use_case: CreateNote = Depends(CreateNote),
) -> NoteSchema:
    return await use_case.execute(data.notebook_id, data.title, data.content)


@router.get("", response_model=ReadAllNoteResponse)
async def read_all(
    request: Request,
    use_case: ReadAllNote = Depends(ReadAllNote),
) -> ReadAllNoteResponse:
    return ReadAllNoteResponse(notes=[note async for note in use_case.execute()])


@router.get("/{note_id}", response_model=ReadNoteResponse)
async def read(
    request: Request,
    note_id: int = Path(..., description=""),
    use_case: ReadNote = Depends(ReadNote),
) -> NoteSchema:
    return await use_case.execute(note_id)


@router.put(
    "/{note_id}",
    response_model=UpdateNoteResponse,
)
async def update(
    request: Request,
    data: UpdateNoteRequest,
    note_id: int = Path(..., description=""),
    use_case: UpdateNote = Depends(UpdateNote),
) -> NoteSchema:
    return await use_case.execute(note_id, data.notebook_id, data.title, data.content)


@router.delete("/{note_id}", status_code=204)
async def delete(
    request: Request,
    note_id: int = Path(..., description=""),
    use_case: DeleteNote = Depends(DeleteNote),
) -> None:
    await use_case.execute(note_id)
