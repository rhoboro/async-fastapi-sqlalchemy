from pydantic import BaseModel, Field

from app.models import NotebookSchema


class CreateNotebookRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=64)
    notes: list[int] = Field(min_length=0)


class CreateNotebookResponse(NotebookSchema):
    pass


class ReadNotebookResponse(NotebookSchema):
    pass


class ReadAllNotebookResponse(BaseModel):
    notebooks: list[NotebookSchema]


class UpdateNotebookRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=64)
    notes: list[int] = Field(min_length=0)


class UpdateNotebookResponse(NotebookSchema):
    pass
