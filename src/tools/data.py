from typing import List, Dict, Any

EMPLOYEES: List[Dict[str, Any]] = [
    {"id": 1, "name": "Alice", "department": "Engineering", "salary": 45000},
    {"id": 2, "name": "Bob", "department": "Engineering", "salary": 28000},
    {"id": 3, "name": "Charlie", "department": "HR", "salary": 50000},
    {"id": 4, "name": "David", "department": "Engineering", "salary": 35000},
    {"id": 5, "name": "Eve", "department": "Marketing", "salary": 32000},
]

ATTENDANCE_DATA = {
    1: {"days_present": 218, "days_absent": 10, "attendance_rate": 0.956},
    2: {"days_present": 201, "days_absent": 27, "attendance_rate": 0.881},
    3: {"days_present": 224, "days_absent": 4, "attendance_rate": 0.982},
    4: {"days_present": 211, "days_absent": 17, "attendance_rate": 0.925},
    5: {"days_present": 205, "days_absent": 23, "attendance_rate": 0.899},
}

PROJECTS: Dict[int, List[Dict[str, Any]]] = {
    1: [
        {"project_id": 101, "name": "Employee Portal", "role": "Lead"},
        {"project_id": 102, "name": "Analytics Platform", "role": "Developer"},
    ],
    2: [
        {"project_id": 102, "name": "Analytics Platform", "role": "Developer"},
    ],
    3: [
        {"project_id": 103, "name": "Hiring Automation", "role": "Owner"},
    ],
    4: [
        {"project_id": 101, "name": "Employee Portal", "role": "Developer"},
    ],
    5: [
        {"project_id": 104, "name": "Marketing Insights", "role": "Owner"},
    ],
}


PROJECT_STATUS: Dict[int, Dict[str, Any]] = {
    101: {
        "project_id": 101,
        "name": "Employee Portal",
        "status": "in_progress",
        "completion_percentage": 72,
    },
    102: {
        "project_id": 102,
        "name": "Analytics Platform",
        "status": "in_progress",
        "completion_percentage": 48,
    },
    103: {
        "project_id": 103,
        "name": "Hiring Automation",
        "status": "completed",
        "completion_percentage": 100,
    },
    104: {
        "project_id": 104,
        "name": "Marketing Insights",
        "status": "planned",
        "completion_percentage": 10,
    },
}