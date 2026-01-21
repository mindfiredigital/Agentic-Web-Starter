import tempfile
from typing import List

from fastapi import APIRouter, File, Form, UploadFile

from src.agents.supervisor import SupervisorAgent


router = APIRouter()
supervisor = SupervisorAgent()


@router.post("/ingest")
async def ingest_pdfs(
    thread_id: str = Form(...),
    files: List[UploadFile] = File(...),
):
    file_paths: List[str] = []
    for upload in files:
        suffix = f"_{upload.filename}" if upload.filename else ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await upload.read()
            tmp.write(content)
            file_paths.append(tmp.name)

    result = supervisor.handle(thread_id=thread_id, file_paths=file_paths)
    return {"thread_id": thread_id, "status": result}
