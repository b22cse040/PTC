from mcp.server.mcpserver import MCPServer
from typing import Any, Dict, List
from src.tools.data import PROJECTS, PROJECT_STATUS, ATTENDANCE_DATA

mcp = MCPServer("Employee-details")

@mcp.tool()
def get_employee_benefits(employee_id: int) -> Dict[str, Any]:
    """Return benefits information associated with a specific employee."""

    return {
        "employee_id": employee_id,
        "health_insurance": True,
        "paid_leave_days": 25,
        "retirement_contribution": 0.05,
    }


@mcp.tool()
def calculate_employee_bonus(
    employee_id: int,
    performance_score: float,
) -> Dict[str, Any]:
    """Calculate an employee's annual bonus using their performance score."""

    return {
        "employee_id": employee_id,
        "performance_score": performance_score,
        "bonus": performance_score * 1000,
    }


@mcp.tool()
def get_company_holidays(year: int) -> List[str]:
    """Return the company's holidays for a specified year."""

    return [
        f"{year}-01-01",
        f"{year}-05-01",
        f"{year}-08-15",
        f"{year}-12-25",
    ]


@mcp.tool()
def get_employee_attendance(employee_id: int) -> Dict[str, Any]:
    """Return attendance statistics for a specific employee."""

    if employee_id not in ATTENDANCE_DATA:
        raise ValueError(
            f"No attendance data found for employee {employee_id}"
        )

    return ATTENDANCE_DATA[employee_id]


@mcp.tool()
def get_employee_projects(employee_id: int) -> List[Dict[str, Any]]:
    """Return projects currently assigned to a specific employee."""

    if employee_id not in PROJECTS:
        raise ValueError(
            f"No project data found for employee {employee_id}"
        )

    return PROJECTS[employee_id]


@mcp.tool()
def get_project_status(project_id: int) -> Dict[str, Any]:
    """Return the current status and completion percentage of a project."""

    if project_id not in PROJECT_STATUS:
        raise ValueError(
            f"No project found with ID {project_id}"
        )

    return PROJECT_STATUS[project_id]
