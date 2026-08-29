from typing import List, Dict, Any

EMPLOYEES: List[Dict[str, Any]] = [
    {"id": 1, "name": "Alice", "department": "Engineering", "salary": 45000},
    {"id": 2, "name": "Bob", "department": "Engineering", "salary": 28000},
    {"id": 3, "name": "Charlie", "department": "HR", "salary": 50000},
    {"id": 4, "name": "David", "department": "Engineering", "salary": 35000},
    {"id": 5, "name": "Eve", "department": "Marketing", "salary": 32000},
    {"id": 6, "name": "Frank", "department": "Engineering", "salary": 52000},
    {"id": 7, "name": "Grace", "department": "Finance", "salary": 48000},
    {"id": 8, "name": "Henry", "department": "Engineering", "salary": 41000},
    {"id": 9, "name": "Ivy", "department": "HR", "salary": 38000},
    {"id": 10, "name": "Jack", "department": "Marketing", "salary": 36000},
    {"id": 11, "name": "Karen", "department": "Engineering", "salary": 47000},
    {"id": 12, "name": "Leo", "department": "Finance", "salary": 55000},
    {"id": 13, "name": "Mia", "department": "Engineering", "salary": 39000},
    {"id": 14, "name": "Nathan", "department": "Sales", "salary": 44000},
    {"id": 15, "name": "Olivia", "department": "Engineering", "salary": 58000},
    {"id": 16, "name": "Paul", "department": "HR", "salary": 42000},
    {"id": 17, "name": "Quinn", "department": "Engineering", "salary": 33000},
    {"id": 18, "name": "Rachel", "department": "Marketing", "salary": 46000},
    {"id": 19, "name": "Sam", "department": "Engineering", "salary": 51000},
    {"id": 20, "name": "Tina", "department": "Finance", "salary": 49000},
    {"id": 21, "name": "Uma", "department": "Sales", "salary": 37000},
    {"id": 22, "name": "Victor", "department": "Engineering", "salary": 43000},
    {"id": 23, "name": "Wendy", "department": "Marketing", "salary": 34000},
    {"id": 24, "name": "Xavier", "department": "Engineering", "salary": 56000},
    {"id": 25, "name": "Yara", "department": "HR", "salary": 40000},
]


ATTENDANCE_DATA = {
    1: {"days_present": 218, "days_absent": 10, "attendance_rate": 0.956},
    2: {"days_present": 201, "days_absent": 27, "attendance_rate": 0.881},
    3: {"days_present": 224, "days_absent": 4, "attendance_rate": 0.982},
    4: {"days_present": 211, "days_absent": 17, "attendance_rate": 0.925},
    5: {"days_present": 205, "days_absent": 23, "attendance_rate": 0.899},
    6: {"days_present": 220, "days_absent": 8, "attendance_rate": 0.965},
    7: {"days_present": 214, "days_absent": 14, "attendance_rate": 0.939},
    8: {"days_present": 216, "days_absent": 12, "attendance_rate": 0.947},
    9: {"days_present": 222, "days_absent": 6, "attendance_rate": 0.974},
    10: {"days_present": 208, "days_absent": 20, "attendance_rate": 0.912},
    11: {"days_present": 219, "days_absent": 9, "attendance_rate": 0.961},
    12: {"days_present": 223, "days_absent": 5, "attendance_rate": 0.978},
    13: {"days_present": 207, "days_absent": 21, "attendance_rate": 0.908},
    14: {"days_present": 212, "days_absent": 16, "attendance_rate": 0.930},
    15: {"days_present": 221, "days_absent": 7, "attendance_rate": 0.969},
    16: {"days_present": 215, "days_absent": 13, "attendance_rate": 0.943},
    17: {"days_present": 202, "days_absent": 26, "attendance_rate": 0.886},
    18: {"days_present": 217, "days_absent": 11, "attendance_rate": 0.952},
    19: {"days_present": 220, "days_absent": 8, "attendance_rate": 0.965},
    20: {"days_present": 209, "days_absent": 19, "attendance_rate": 0.917},
    21: {"days_present": 213, "days_absent": 15, "attendance_rate": 0.934},
    22: {"days_present": 218, "days_absent": 10, "attendance_rate": 0.956},
    23: {"days_present": 204, "days_absent": 24, "attendance_rate": 0.895},
    24: {"days_present": 216, "days_absent": 12, "attendance_rate": 0.947},
    25: {"days_present": 222, "days_absent": 6, "attendance_rate": 0.974},
}


PROJECTS: Dict[int, List[Dict[str, Any]]] = {
    1: [
        {"project_id": 101, "name": "Employee Portal", "role": "Lead"},
        {"project_id": 102, "name": "Analytics Platform", "role": "Developer"},
    ],
    2: [
        {"project_id": 102, "name": "Analytics Platform", "role": "Developer"},
        {"project_id": 105, "name": "Cloud Migration", "role": "Developer"},
    ],
    3: [
        {"project_id": 103, "name": "Hiring Automation", "role": "Owner"},
    ],
    4: [
        {"project_id": 101, "name": "Employee Portal", "role": "Developer"},
        {"project_id": 106, "name": "Security Modernization", "role": "Developer"},
    ],
    5: [
        {"project_id": 104, "name": "Marketing Insights", "role": "Owner"},
    ],
    6: [
        {"project_id": 105, "name": "Cloud Migration", "role": "Lead"},
        {"project_id": 107, "name": "API Gateway", "role": "Developer"},
    ],
    7: [
        {"project_id": 108, "name": "Financial Forecasting", "role": "Owner"},
    ],
    8: [
        {"project_id": 101, "name": "Employee Portal", "role": "Developer"},
        {"project_id": 107, "name": "API Gateway", "role": "Developer"},
    ],
    9: [
        {"project_id": 103, "name": "Hiring Automation", "role": "Developer"},
    ],
    10: [
        {"project_id": 104, "name": "Marketing Insights", "role": "Developer"},
        {"project_id": 109, "name": "Campaign Automation", "role": "Lead"},
    ],
    11: [
        {"project_id": 102, "name": "Analytics Platform", "role": "Lead"},
        {"project_id": 106, "name": "Security Modernization", "role": "Developer"},
    ],
    12: [
        {"project_id": 108, "name": "Financial Forecasting", "role": "Developer"},
    ],
    13: [
        {"project_id": 105, "name": "Cloud Migration", "role": "Developer"},
        {"project_id": 107, "name": "API Gateway", "role": "Developer"},
    ],
    14: [
        {"project_id": 110, "name": "CRM Modernization", "role": "Lead"},
    ],
    15: [
        {"project_id": 106, "name": "Security Modernization", "role": "Lead"},
        {"project_id": 102, "name": "Analytics Platform", "role": "Developer"},
    ],
    16: [
        {"project_id": 103, "name": "Hiring Automation", "role": "Developer"},
    ],
    17: [
        {"project_id": 107, "name": "API Gateway", "role": "Developer"},
    ],
    18: [
        {"project_id": 104, "name": "Marketing Insights", "role": "Lead"},
        {"project_id": 109, "name": "Campaign Automation", "role": "Developer"},
    ],
    19: [
        {"project_id": 105, "name": "Cloud Migration", "role": "Developer"},
        {"project_id": 106, "name": "Security Modernization", "role": "Developer"},
    ],
    20: [
        {"project_id": 108, "name": "Financial Forecasting", "role": "Developer"},
    ],
    21: [
        {"project_id": 110, "name": "CRM Modernization", "role": "Developer"},
    ],
    22: [
        {"project_id": 101, "name": "Employee Portal", "role": "Developer"},
        {"project_id": 107, "name": "API Gateway", "role": "Lead"},
    ],
    23: [
        {"project_id": 109, "name": "Campaign Automation", "role": "Developer"},
    ],
    24: [
        {"project_id": 102, "name": "Analytics Platform", "role": "Developer"},
        {"project_id": 105, "name": "Cloud Migration", "role": "Lead"},
    ],
    25: [
        {"project_id": 103, "name": "Hiring Automation", "role": "Owner"},
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
    105: {
        "project_id": 105,
        "name": "Cloud Migration",
        "status": "in_progress",
        "completion_percentage": 61,
    },
    106: {
        "project_id": 106,
        "name": "Security Modernization",
        "status": "in_progress",
        "completion_percentage": 37,
    },
    107: {
        "project_id": 107,
        "name": "API Gateway",
        "status": "in_progress",
        "completion_percentage": 82,
    },
    108: {
        "project_id": 108,
        "name": "Financial Forecasting",
        "status": "in_progress",
        "completion_percentage": 55,
    },
    109: {
        "project_id": 109,
        "name": "Campaign Automation",
        "status": "planned",
        "completion_percentage": 18,
    },
    110: {
        "project_id": 110,
        "name": "CRM Modernization",
        "status": "in_progress",
        "completion_percentage": 43,
    },
}