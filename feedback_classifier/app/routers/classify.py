"""Classify router — POST /classify, POST /classify/bulk, GET /results."""

from __future__ import annotations

import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.core.config import Settings, get_settings
from app.core.prompts import CLASSIFICATION_PROMPT
from app.models.schemas import FeedbackIn, FeedbackOut, PaginatedResults
from app.services.classifier import ClassificationService
from app.services.prioritizer import PriorityService
from app.services.storage import StorageService

router = APIRouter()


def _classifier(settings: Settings = Depends(get_settings)) -> ClassificationService:
    return ClassificationService(settings, CLASSIFICATION_PROMPT)


def _storage(settings: Settings = Depends(get_settings)) -> StorageService:
    return StorageService(settings.db_path)


def _prioritizer() -> PriorityService:
    return PriorityService()


def _build_feedback(
    fb_in: FeedbackIn, result: dict, priority: float
) -> FeedbackOut:
    return FeedbackOut(
        id=0,
        text=fb_in.text,
        sentiment=result["sentiment"],
        topic=result["topic"],
        summary=result["summary"],
        severity=result["severity"],
        priority_score=priority,
        source=fb_in.source,
        submitted_at=fb_in.submitted_at,
        classified_at=datetime.utcnow(),
    )


@router.post("/classify", response_model=FeedbackOut)
def classify_single(
    body: FeedbackIn,
    clf: ClassificationService = Depends(_classifier),
    pri: PriorityService = Depends(_prioritizer),
    store: StorageService = Depends(_storage),
) -> FeedbackOut:
    result = clf.classify(body.text)
    priority = pri.compute_priority(result["severity"], body.submitted_at)
    feedback = _build_feedback(body, result, priority)
    return store.save(feedback)


@router.post("/classify/bulk", response_model=list[FeedbackOut])
async def classify_bulk(
    file: UploadFile = File(...),
    clf: ClassificationService = Depends(_classifier),
    pri: PriorityService = Depends(_prioritizer),
    store: StorageService = Depends(_storage),
) -> list[FeedbackOut]:
    content = (await file.read()).decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    outputs: list[FeedbackOut] = []
    for row in reader:
        fb_in = FeedbackIn(
            text=row["text"],
            source=row.get("source", "csv"),
        )
        result = clf.classify(fb_in.text)
        priority = pri.compute_priority(result["severity"], fb_in.submitted_at)
        feedback = _build_feedback(fb_in, result, priority)
        outputs.append(store.save(feedback))
    return outputs


@router.get("/results", response_model=PaginatedResults)
def get_results(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sentiment: str | None = Query(None),
    min_priority: float | None = Query(None),
    store: StorageService = Depends(_storage),
) -> PaginatedResults:
    return store.get_results(page, page_size, sentiment, min_priority)
