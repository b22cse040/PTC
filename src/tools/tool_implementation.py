from typing import Callable, Dict, Any, List


# ============================================================
# Relevant tools
# ============================================================

def get_employees_by_department(department: str) -> List[Dict[str, Any]]:
    """Return employees belonging to a department."""
    employees : List[Dict[str, Any]] = [
        {"id": 1, "name": "Alice", "department": "Engineering", "salary": 45000},
        {"id": 2, "name": "Bob", "department": "Engineering", "salary": 28000},
        {"id": 3, "name": "Charlie", "department": "HR", "salary": 50000},
        {"id": 4, "name": "David", "department": "Engineering", "salary": 35000},
        {"id": 5, "name": "Eve", "department": "Marketing", "salary": 32000},
    ]

    return [
        employee
        for employee in employees
        if employee["department"].lower() == department.lower()
    ]


def filter_employees_by_salary(
    employees: List[Dict[str, Any]],
    minimum_salary: float
) -> List[Dict[str, Any]]:
    """Return employees whose salary is greater than the specified amount."""
    return [
        employee
        for employee in employees
        if employee["salary"] > minimum_salary
    ]


def search_employees(
    department: str | None = None,
    minimum_salary: float | None = None
) -> List[Dict[str, Any]]:
    """Search employees using optional department and salary filters."""
    employees = [
        {"id": 1, "name": "Alice", "department": "Engineering", "salary": 45000},
        {"id": 2, "name": "Bob", "department": "Engineering", "salary": 28000},
        {"id": 3, "name": "Charlie", "department": "HR", "salary": 50000},
        {"id": 4, "name": "David", "department": "Engineering", "salary": 35000},
        {"id": 5, "name": "Eve", "department": "Marketing", "salary": 32000},
    ]

    if department:
        employees = [
            e for e in employees
            if e["department"].lower() == department.lower()
        ]

    if minimum_salary is not None:
        employees = [
            e for e in employees
            if e["salary"] > minimum_salary
        ]

    return employees


# ============================================================
# Irrelevant tools
# ============================================================

def get_employee_benefits(employee_id: int) -> dict:
    """Return benefits information for a specific employee."""
    return {
        "employee_id": employee_id,
        "health_insurance": True,
        "paid_leave_days": 25,
        "retirement_contribution": 0.05,
    }


def calculate_employee_bonus(
    employee_id: int,
    performance_score: float
) -> float:
    """Calculate an employee's annual bonus based on performance."""
    return performance_score * 1000


def get_company_holidays(year: int) -> list[str]:
    """Return the company's holidays for a given year."""
    return [
        f"{year}-01-01",
        f"{year}-05-01",
        f"{year}-08-15",
        f"{year}-12-25",
    ]


def get_employee_attendance(employee_id: int) -> dict:
    """Return attendance statistics for an employee."""
    return {
        "employee_id": employee_id,
        "days_present": 220,
        "days_absent": 8,
        "attendance_rate": 0.965,
    }


# ============================================================
# Tool registry
# ============================================================

TOOLS: Dict[str, Callable] = {
    # Relevant
    "get_employees_by_department": get_employees_by_department,
    "filter_employees_by_salary": filter_employees_by_salary,
    "search_employees": search_employees,

    # Irrelevant
    "get_employee_benefits": get_employee_benefits,
    "calculate_employee_bonus": calculate_employee_bonus,
    "get_company_holidays": get_company_holidays,
    "get_employee_attendance": get_employee_attendance,
}