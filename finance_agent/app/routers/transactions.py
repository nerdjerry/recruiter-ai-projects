from __future__ import annotations

from fastapi import APIRouter, Request, UploadFile, File, Query
from typing import Optional

from app.models.schemas import SyncResponse, Transaction

router = APIRouter(tags=["transactions"])


@router.post("/sync", response_model=SyncResponse)
async def sync_transactions(
    request: Request, file: UploadFile = File(...)
) -> SyncResponse:
    importer = request.app.state.csv_importer
    categorizer = request.app.state.categorizer
    content = (await file.read()).decode("utf-8")
    transactions = importer.import_csv(content)

    for txn in transactions:
        if txn.category == "other":
            try:
                txn.category = categorizer.categorize(txn.description)
            except Exception:
                pass

    importer.save_transactions(transactions)
    return SyncResponse(
        imported_count=len(transactions),
        message=f"Imported {len(transactions)} transactions.",
    )


@router.get("/transactions", response_model=list[Transaction])
async def get_transactions(
    request: Request,
    days: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
) -> list[Transaction]:
    importer = request.app.state.csv_importer
    return importer.get_transactions(days=days, category=category, min_amount=min_amount)
