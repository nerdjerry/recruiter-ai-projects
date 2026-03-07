from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.core.config import Settings, get_settings
from app.models.schemas import ScreeningResponse
from app.services.embedder import EmbeddingService
from app.services.parser import ParserFactory
from app.services.scorer import ScoringService

router = APIRouter()


def _get_embedder(settings: Settings = Depends(get_settings)) -> EmbeddingService:
    return EmbeddingService(settings)


def _get_scorer(settings: Settings = Depends(get_settings)) -> ScoringService:
    return ScoringService(settings)


@router.post("/screen", response_model=ScreeningResponse)
async def screen_resumes(
    job_description: str = Form(...),
    resumes: list[UploadFile] = File(...),
    settings: Settings = Depends(get_settings),
    embedder: EmbeddingService = Depends(_get_embedder),
    scorer: ScoringService = Depends(_get_scorer),
) -> ScreeningResponse:
    max_bytes = settings.max_upload_mb * 1024 * 1024
    jd_embedding = await embedder.aget_embedding(job_description)

    candidates = []
    for upload in resumes:
        file_bytes = await upload.read()
        if len(file_bytes) > max_bytes:
            raise HTTPException(status_code=413, detail=f"{upload.filename} exceeds size limit")

        parser = ParserFactory.get_parser(upload.filename or "file.pdf")
        resume_text = parser.parse(file_bytes, upload.filename or "file.pdf")
        resume_embedding = await embedder.aget_embedding(resume_text)
        similarity = EmbeddingService.compute_similarity(jd_embedding, resume_embedding)
        result = await scorer.aexplain_match(job_description, resume_text, similarity)
        candidates.append(result)

    candidates.sort(key=lambda c: c.score, reverse=True)
    return ScreeningResponse(job_description=job_description, candidates=candidates)
