from pydantic import BaseModel, ConfigDict


class NoteSchema(BaseModel):
    id: int
    title: str
    content: str
    notebook_id: int
    notebook_title: str

    model_config = ConfigDict(from_attributes=True)


class NotebookSchema(BaseModel):
    id: int
    title: str
    notes: list[NoteSchema]

    model_config = ConfigDict(from_attributes=True)
