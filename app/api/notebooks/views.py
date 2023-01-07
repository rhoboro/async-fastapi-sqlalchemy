from fastapi import APIRouter, Depends, Path, Request

from app.models import NotebookSchema

from .schema import (
    CreateNotebookRequest,
    CreateNotebookResponse,
    ReadAllNotebookResponse,
    ReadNotebookResponse,
    UpdateNotebookRequest,
    UpdateNotebookResponse,
)
from .use_cases import CreateNotebook, DeleteNotebook, ReadAllNotebook, ReadNotebook, UpdateNotebook

router = APIRouter(prefix="/notebooks")


@router.post("", response_model=CreateNotebookResponse)
async def create(
    request: Request,
    data: CreateNotebookRequest,
    use_case: CreateNotebook = Depends(CreateNotebook),
) -> NotebookSchema:
    return await use_case.execute(data.title, data.notes)


@router.get("", response_model=ReadAllNotebookResponse)
async def read_all(
    request: Request, use_case: ReadAllNotebook = Depends(ReadAllNotebook)
) -> ReadAllNotebookResponse:
    return ReadAllNotebookResponse(notebooks=[nb async for nb in use_case.execute()])


@router.get(
    "/{notebook_id}",
    response_model=ReadNotebookResponse,
)
async def read(
    request: Request,
    notebook_id: int = Path(..., description=""),
    use_case: ReadNotebook = Depends(ReadNotebook),
) -> NotebookSchema:
    return await use_case.execute(notebook_id)


@router.put(
    "/{notebook_id}",
    response_model=UpdateNotebookResponse,
)
async def update(
    request: Request,
    data: UpdateNotebookRequest,
    notebook_id: int = Path(..., description=""),
    use_case: UpdateNotebook = Depends(UpdateNotebook),
) -> NotebookSchema:
    return await use_case.execute(notebook_id, title=data.title, notes=data.notes)


@router.delete("/{notebook_id}", status_code=204)
async def delete(
    request: Request,
    notebook_id: int = Path(..., description=""),
    use_case: DeleteNotebook = Depends(DeleteNotebook),
) -> None:
    await use_case.execute(notebook_id)
