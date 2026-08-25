from typing import Dict, List, Any 
from src.tools.data import EMPLOYEES

def get_employees() -> List[Dict[str, Any]]:
    """Return the complete list of employees."""
    return EMPLOYEES


def get_employees_by_department(
    department: str,
) -> List[Dict[str, Any]]:
    """Return employees belonging to a specified department."""

    return [
        employee
        for employee in EMPLOYEES
        if employee["department"].lower() == department.lower()
    ]


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