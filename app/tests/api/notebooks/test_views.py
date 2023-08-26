import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.utils import ID_STRING


async def setup_data(session: AsyncSession) -> None:
    from app.models import Note, Notebook

    notebook1 = Notebook(title="Notebook 1", notes=[])
    notebook2 = Notebook(title="Notebook 2", notes=[])
    session.add_all([notebook1, notebook2])
    await session.flush()

    note1 = Note(title="Note 1", content="Content 1", notebook_id=notebook1.id)
    note2 = Note(title="Note 2", content="Content 2", notebook_id=notebook1.id)
    note3 = Note(title="Note 3", content="Content 3", notebook_id=notebook2.id)
    session.add_all([note1, note2, note3])
    await session.flush()

    await session.commit()


@pytest.mark.anyio
async def test_notebooks_read_all(ac: AsyncClient, session: AsyncSession) -> None:
    """Read all notebooks"""
    # setup
    await setup_data(session)

    # execute
    response = await ac.get(
        "/api/notebooks",
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
        "notebooks": [
            {
                "id": ID_STRING,
                "title": "Notebook 1",
                "notes": [
                    {
                        "id": ID_STRING,
                        "title": "Note 1",
                        "content": "Content 1",
                        "notebook_id": ID_STRING,
                        "notebook_title": "Notebook 1",
                    },
                    {
                        "id": ID_STRING,
                        "title": "Note 2",
                        "content": "Content 2",
                        "notebook_id": ID_STRING,
                        "notebook_title": "Notebook 1",
                    },
                ],
            },
            {
                "id": ID_STRING,
                "title": "Notebook 2",
                "notes": [
                    {
                        "id": ID_STRING,
                        "title": "Note 3",
                        "content": "Content 3",
                        "notebook_id": ID_STRING,
                        "notebook_title": "Notebook 2",
                    }
                ],
            },
        ]
    }
    assert expected == response.json()


@pytest.mark.anyio
async def test_notebooks_read(ac: AsyncClient, session: AsyncSession) -> None:
    """Read a notebook"""
    from app.models import Notebook

    # setup
    await setup_data(session)
    notebook = [nb async for nb in Notebook.read_all(session, include_notes=True)][0]

    # execute
    response = await ac.get(
        f"/api/notebooks/{notebook.id}",
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
        "id": notebook.id,
        "title": "Notebook 1",
        "notes": [
            {
                "id": ID_STRING,
                "title": "Note 1",
                "content": "Content 1",
                "notebook_id": ID_STRING,
                "notebook_title": "Notebook 1",
            },
            {
                "id": ID_STRING,
                "title": "Note 2",
                "content": "Content 2",
                "notebook_id": ID_STRING,
                "notebook_title": "Notebook 1",
            },
        ],
    }
    assert expected == response.json()


@pytest.mark.anyio
async def test_notebooks_create(ac: AsyncClient, session: AsyncSession) -> None:
    """Create a notebook"""
    # execute
    response = await ac.post("/api/notebooks", json={"title": "Test Notebook", "notes": []})

    print(response.content)
    assert 200 == response.status_code
    expected = {"id": ID_STRING, "title": "Test Notebook", "notes": []}
    assert expected == response.json()


@pytest.mark.anyio
async def test_notebooks_update(ac: AsyncClient, session: AsyncSession) -> None:
    """Update a notebook"""
    from app.models import Notebook

    # setup
    await setup_data(session)
    notebook = [nb async for nb in Notebook.read_all(session, include_notes=True)][0]
    assert "Notebook 1" == notebook.title
    assert 2 == len(notebook.notes)
    note = notebook.notes[0]

    # execute
    response = await ac.put(
        f"/api/notebooks/{notebook.id}", json={"title": "Test Notebook", "notes": [note.id]}
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
        "id": notebook.id,
        "title": "Test Notebook",
        "notes": [
            {
                "id": ID_STRING,
                "title": "Note 1",
                "content": "Content 1",
                "notebook_id": ID_STRING,
                "notebook_title": "Test Notebook",
            }
        ],
    }
    assert expected == response.json()

    await session.refresh(notebook)
    assert "Test Notebook" == notebook.title
    assert 1 == len(notebook.notes)


@pytest.mark.anyio
async def test_notebooks_delete(ac: AsyncClient, session: AsyncSession) -> None:
    """Delete a notebook"""
    from app.models import Note, Notebook

    # setup
    await setup_data(session)
    notebooks = [nb async for nb in Notebook.read_all(session, include_notes=True)]
    assert 2 == len(notebooks)
    notes = [n async for n in Note.read_all(session)]
    assert 3 == len(notes)

    # execute
    response = await ac.delete(
        f"/api/notebooks/{notebooks[0].id}",
    )

    print(response.content)
    assert 204 == response.status_code

    notebooks = [nb async for nb in Notebook.read_all(session, include_notes=True)]
    assert 1 == len(notebooks)

    # delete-orphan
    notes = [n async for n in Note.read_all(session)]
    assert 1 == len(notes)
