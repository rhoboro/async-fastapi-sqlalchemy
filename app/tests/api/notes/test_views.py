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
async def test_notes_read_all(ac: AsyncClient, session: AsyncSession) -> None:
    """Read all notes"""
    # setup
    await setup_data(session)

    # execute
    response = await ac.get(
        "/api/notes",
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
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
            {
                "id": ID_STRING,
                "title": "Note 3",
                "content": "Content 3",
                "notebook_id": ID_STRING,
                "notebook_title": "Notebook 2",
            },
        ]
    }
    assert expected == response.json()


@pytest.mark.anyio
async def test_notes_read(ac: AsyncClient, session: AsyncSession) -> None:
    """Read a note"""
    from app.models import Notebook

    # setup
    await setup_data(session)
    notebook = [nb async for nb in Notebook.read_all(session, include_notes=True)][0]
    note = notebook.notes[0]

    # execute
    response = await ac.get(
        f"/api/notes/{note.id}",
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
        "id": note.id,
        "title": "Note 1",
        "content": "Content 1",
        "notebook_id": notebook.id,
        "notebook_title": "Notebook 1",
    }
    assert expected == response.json()


@pytest.mark.anyio
async def test_notes_create(ac: AsyncClient, session: AsyncSession) -> None:
    """Create a note"""
    from app.models import Notebook

    # setup
    await setup_data(session)
    notebook = [nb async for nb in Notebook.read_all(session, include_notes=True)][0]
    notes_count = len(notebook.notes)

    # execute
    response = await ac.post(
        "/api/notes",
        json={"title": "Test Note", "content": "Test Content", "notebook_id": notebook.id},
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
        "id": ID_STRING,
        "title": "Test Note",
        "content": "Test Content",
        "notebook_id": notebook.id,
        "notebook_title": notebook.title,
    }
    assert expected == response.json()

    await session.refresh(notebook)
    assert notes_count + 1 == len(notebook.notes)


@pytest.mark.anyio
async def test_notes_update(ac: AsyncClient, session: AsyncSession) -> None:
    """Update a note"""
    from app.models import Notebook

    # setup
    await setup_data(session)
    notebook = [nb async for nb in Notebook.read_all(session, include_notes=True)][0]
    note = notebook.notes[0]
    assert "Note 1" == note.title
    assert "Content 1" == note.content

    # execute
    response = await ac.put(
        f"/api/notes/{note.id}",
        json={
            "title": "Test Note",
            "content": "Test Content",
            "notebook_id": note.notebook_id,
        },
    )

    print(response.content)
    assert 200 == response.status_code
    expected = {
        "id": note.id,
        "title": "Test Note",
        "content": "Test Content",
        "notebook_id": notebook.id,
        "notebook_title": notebook.title,
    }
    assert expected == response.json()

    await session.refresh(note)
    assert "Test Note" == note.title
    assert "Test Content" == note.content


@pytest.mark.anyio
async def test_notes_delete(ac: AsyncClient, session: AsyncSession) -> None:
    """Delete a note"""
    from app.models import Notebook

    # setup
    await setup_data(session)
    notebook = [nb async for nb in Notebook.read_all(session, include_notes=True)][0]
    notes_count = len(notebook.notes)
    note = notebook.notes[0]

    # execute
    response = await ac.delete(
        f"/api/notes/{note.id}",
    )

    print(response.content)
    assert 204 == response.status_code

    await session.refresh(notebook)
    assert notes_count - 1 == len(notebook.notes)
