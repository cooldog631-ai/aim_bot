"""Employee API endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import get_employee_repo
from src.api.schemas.employee import EmployeeResponse
from src.database.repositories.employee_repo import EmployeeRepository

router = APIRouter()


@router.get("/", response_model=List[EmployeeResponse])
async def get_employees(
    limit: int = 100, offset: int = 0, repo: EmployeeRepository = Depends(get_employee_repo)
):
    """Get all employees with pagination."""
    employees = await repo.get_all(limit=limit, offset=offset)
    return employees


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, repo: EmployeeRepository = Depends(get_employee_repo)):
    """Get employee by ID."""
    employee = await repo.get_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.get("/messenger/{messenger_id}", response_model=EmployeeResponse)
async def get_employee_by_messenger(
    messenger_id: str, repo: EmployeeRepository = Depends(get_employee_repo)
):
    """Get employee by messenger ID."""
    employee = await repo.get_by_messenger_id(messenger_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
