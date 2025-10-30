"""Report API endpoints."""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_report_repo
from src.api.schemas.report import ReportCreate, ReportResponse
from src.database.repositories.report_repo import ReportRepository

router = APIRouter()


@router.get("/", response_model=List[ReportResponse])
async def get_reports(
    limit: int = 100,
    offset: int = 0,
    start_date: Optional[date] = None,
    repo: ReportRepository = Depends(get_report_repo),
):
    """Get all reports with pagination."""
    reports = await repo.get_all(limit=limit, offset=offset, start_date=start_date)
    return reports


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: int, repo: ReportRepository = Depends(get_report_repo)):
    """Get report by ID."""
    report = await repo.get_by_id(report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.post("/", response_model=ReportResponse, status_code=201)
async def create_report(
    report_data: ReportCreate, repo: ReportRepository = Depends(get_report_repo)
):
    """Create new report."""
    report = await repo.create(
        employee_id=report_data.employee_id,
        report_date=report_data.report_date,
        equipment_number=report_data.equipment_number,
        brigade_number=report_data.brigade_number,
        work_description=report_data.work_description,
        transcription=report_data.transcription,
        structured_data=report_data.structured_data,
    )
    return report


@router.delete("/{report_id}", status_code=204)
async def delete_report(report_id: int, repo: ReportRepository = Depends(get_report_repo)):
    """Delete report by ID."""
    success = await repo.delete(report_id)
    if not success:
        raise HTTPException(status_code=404, detail="Report not found")
    return None
