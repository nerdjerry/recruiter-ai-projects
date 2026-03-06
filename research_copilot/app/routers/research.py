"""Research router — POST /research, POST /documents, GET /documents."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile

from app.models.schemas import (
    DocumentInfo,
    DocumentListResponse,
    ResearchRequest,
    ResearchResponse,
)

router = APIRouter(tags=["research"])


def _get_agent():
    from app.main import get_agent
    return get_agent()


def _get_vectorstore():
    from app.main import get_vectorstore
    return get_vectorstore()


@router.post("/research", response_model=ResearchResponse)
async def research(body: ResearchRequest, agent=Depends(_get_agent)):
    return agent.research(body.question, body.document_ids or None)


@router.post("/documents", response_model=DocumentInfo)
async def upload_document(
    file: UploadFile = File(...),
    vectorstore=Depends(_get_vectorstore),
):
    raw = await file.read()
    filename = file.filename or "untitled"

    if filename.lower().endswith(".pdf"):
        import io
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        text = raw.decode("utf-8", errors="ignore")

    return vectorstore.add_document(filename, text)


@router.get("/documents", response_model=DocumentListResponse)
async def list_documents(vectorstore=Depends(_get_vectorstore)):
    return DocumentListResponse(documents=vectorstore.list_documents())
