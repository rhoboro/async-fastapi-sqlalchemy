from pydantic import BaseModel, Field

from app.models import NoteSchema


class CreateNoteRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=64)
    content: str = Field("", min_length=0, max_length=500)
    notebook_id: int


class CreateNoteResponse(NoteSchema):
    pass


class ReadNoteResponse(NoteSchema):
    pass


class ReadAllNoteResponse(BaseModel):
    notes: list[NoteSchema]


class UpdateNoteRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=64)
    content: str = Field(..., min_length=0, max_length=500)
    notebook_id: int


class UpdateNoteResponse(NoteSchema):
    pass
