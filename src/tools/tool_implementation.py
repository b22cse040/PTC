from typing import Callable, Dict, Any, List


# ============================================================
# Employee data
# ============================================================

EMPLOYEES: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Alice",
        "department": "Engineering",
        "salary": 45000,
    },
    {
        "id": 2,
        "name": "Bob",
        "department": "Engineering",
        "salary": 28000,
    },
    {
        "id": 3,
        "name": "Charlie",
        "department": "HR",
        "salary": 50000,
    },
    {
        "id": 4,
        "name": "David",
        "department": "Engineering",
        "salary": 35000,
    },
    {
        "id": 5,
        "name": "Eve",
        "department": "Marketing",
        "salary": 32000,
    },
]


# ============================================================
# Relevant tools
# ============================================================

def get_employees_by_department(
    department: str,
) -> List[Dict[str, Any]]:
    """Return employees belonging to a specified department."""

    return [
        employee
        for employee in EMPLOYEES
        if employee["department"].lower() == department.lower()
    ]


def filter_employees_by_salary(
    employees: List[Dict[str, Any]],
    minimum_salary: float,
) -> List[Dict[str, Any]]:
    """Return employees whose salary is greater than the specified amount."""

    return [
        employee
        for employee in employees
        if employee["salary"] > minimum_salary
    ]


def search_employees(
    department: str | None = None,
    minimum_salary: float | None = None,
) -> List[Dict[str, Any]]:
    """Search employees using optional department and minimum salary filters."""

    employees = EMPLOYEES

    if department:
        employees = [
            employee
            for employee in employees
            if employee["department"].lower() == department.lower()
        ]

    if minimum_salary is not None:
        employees = [
            employee
            for employee in employees
            if employee["salary"] > minimum_salary
        ]

    return employees


def get_employee_department() -> List[Dict[str, str]]:
    """Return the name and department of every employee."""

    return [
        {
            "name": employee["name"],
            "department": employee["department"],
        }
        for employee in EMPLOYEES
    ]


def get_employee_salary() -> List[Dict[str, Any]]:
    """Return the name and salary of every employee."""

    return [
        {
            "name": employee["name"],
            "salary": employee["salary"],
        }
        for employee in EMPLOYEES
    ]


# ============================================================
# Irrelevant tools
# ============================================================

def get_employee_benefits(
    employee_id: int,
) -> dict:
    """Return benefits information associated with a specific employee."""

    return {
        "employee_id": employee_id,
        "health_insurance": True,
        "paid_leave_days": 25,
        "retirement_contribution": 0.05,
    }


def calculate_employee_bonus(
    employee_id: int,
    performance_score: float,
) -> float:
    """Calculate an employee's annual bonus using their performance score."""

    return performance_score * 1000


def get_company_holidays(
    year: int,
) -> List[str]:
    """Return the company's holidays for a specified year."""

    return [
        f"{year}-01-01",
        f"{year}-05-01",
        f"{year}-08-15",
        f"{year}-12-25",
    ]


def get_employee_attendance(
    employee_id: int,
) -> dict:
    """Return attendance statistics for a specific employee."""

    attendance_data = {
        1: {
            "employee_id": 1,
            "days_present": 218,
            "days_absent": 10,
            "attendance_rate": 0.956,
        },
        2: {
            "employee_id": 2,
            "days_present": 201,
            "days_absent": 27,
            "attendance_rate": 0.881,
        },
        3: {
            "employee_id": 3,
            "days_present": 224,
            "days_absent": 4,
            "attendance_rate": 0.982,
        },
        4: {
            "employee_id": 4,
            "days_present": 211,
            "days_absent": 17,
            "attendance_rate": 0.925,
        },
        5: {
            "employee_id": 5,
            "days_present": 205,
            "days_absent": 23,
            "attendance_rate": 0.899,
        },
    }

    if employee_id not in attendance_data:
        raise ValueError(
            f"No attendance data found for employee {employee_id}"
        )

    return attendance_data[employee_id]


# ============================================================
# Tool registry
# ============================================================

TOOLS: Dict[str, Callable] = {
    # Relevant
    "get_employees_by_department": get_employees_by_department,
    "filter_employees_by_salary": filter_employees_by_salary,
    "search_employees": search_employees,
    "get_employee_department": get_employee_department,
    "get_employee_salary": get_employee_salary,

    # Irrelevant
    "get_employee_benefits": get_employee_benefits,
    "calculate_employee_bonus": calculate_employee_bonus,
    "get_company_holidays": get_company_holidays,
    "get_employee_attendance": get_employee_attendance,
}