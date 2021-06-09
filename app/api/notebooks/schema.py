from __future__ import annotations

from pydantic import BaseModel, Field

from app.models import NotebookSchema


class CreateNotebookRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=64, description="")
    notes: list[int] = Field(min_items=0, description="")


class CreateNotebookResponse(NotebookSchema):
    pass


class ReadNotebookResponse(NotebookSchema):
    pass


class ReadAllNotebookResponse(BaseModel):
    notebooks: list[NotebookSchema]


class UpdateNotebookRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=64, description="")
    notes: list[int] = Field(min_items=0, description="")


class UpdateNotebookResponse(NotebookSchema):
    pass
