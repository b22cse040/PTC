TOOL_DEFINITIONS = [
    {
        "name": "get_employees",
        "description": "Return the complete list of employees.",
        "source": "native",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
        "output_schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": "string",
                    },
                    "department": {
                        "type": "string",
                    },
                    "salary": {
                        "type": "number",
                    },
                },
                "required": [
                    "id",
                    "name",
                    "department",
                    "salary",
                ],
            },
        },
        "input_example": {},
    },
    {
        "name": "get_employees_by_department",
        "description": "Return employees belonging to a specified department.",
        "source": "native",
        "input_schema": {
            "type": "object",
            "properties": {
                "department": {
                    "type": "string",
                    "description": "The department to search for.",
                }
            },
            "required": ["department"],
        },
        "output_schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "name": {
                        "type": "string",
                    },
                    "department": {
                        "type": "string",
                    },
                    "salary": {
                        "type": "number",
                    },
                },
                "required": [
                    "id",
                    "name",
                    "department",
                    "salary",
                ],
            },
        },
        "input_example": {
            "department": "Engineering",
        },
    },
    {
        "name": "get_employee_department",
        "description": "Return the name and department of every employee.",
        "source": "native",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
        "output_schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "department": {
                        "type": "string",
                    },
                },
                "required": [
                    "name",
                    "department",
                ],
            },
        },
        "input_example": {},
    },
    {
        "name": "get_employee_salary",
        "description": "Return the name and salary of every employee.",
        "source": "native",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
        "output_schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                    },
                    "salary": {
                        "type": "number",
                    },
                },
                "required": [
                    "name",
                    "salary",
                ],
            },
        },
        "input_example": {},
    },
    {
        "name": "get_employee_benefits",
        "description": "Return benefits information associated with a specific employee.",
        "source": "mcp",
        "input_schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                    "description": "Unique identifier of the employee.",
                }
            },
            "required": ["employee_id"],
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                },
                "health_insurance": {
                    "type": "boolean",
                },
                "paid_leave_days": {
                    "type": "integer",
                },
                "retirement_contribution": {
                    "type": "number",
                },
            },
            "required": [
                "employee_id",
                "health_insurance",
                "paid_leave_days",
                "retirement_contribution",
            ],
        },
        "input_example": {
            "employee_id": 1,
        },
    },
    {
        "name": "calculate_employee_bonus",
        "description": "Calculate an employee's annual bonus using their performance score.",
        "source": "mcp",
        "input_schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                    "description": "Unique identifier of the employee.",
                },
                "performance_score": {
                    "type": "number",
                    "description": "Employee performance score.",
                },
            },
            "required": [
                "employee_id",
                "performance_score",
            ],
        },
        "output_schema": {
            "type": "number",
            "description": "The calculated annual employee bonus.",
        },
        "input_example": {
            "employee_id": 1,
            "performance_score": 0.9,
        },
    },
    {
        "name": "get_company_holidays",
        "description": "Return the company's holidays for a specified year.",
        "source": "mcp",
        "input_schema": {
            "type": "object",
            "properties": {
                "year": {
                    "type": "integer",
                    "description": "Calendar year.",
                }
            },
            "required": ["year"],
        },
        "output_schema": {
            "type": "array",
            "items": {
                "type": "string",
            },
            "description": "List of company holiday dates.",
        },
        "input_example": {
            "year": 2026,
        },
    },
    {
        "name": "get_employee_attendance",
        "description": "Return attendance statistics for a specific employee.",
        "source": "mcp",
        "input_schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                    "description": "Unique identifier of the employee.",
                }
            },
            "required": ["employee_id"],
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                },
                "days_present": {
                    "type": "integer",
                },
                "days_absent": {
                    "type": "integer",
                },
                "attendance_rate": {
                    "type": "number",
                },
            },
            "required": [
                "employee_id",
                "days_present",
                "days_absent",
                "attendance_rate",
            ],
        },
        "input_example": {
            "employee_id": 1,
        },
    },
    {
        "name": "get_employee_projects",
        "description": "Return projects currently assigned to a specific employee.",
        "source": "mcp",
        "input_schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                    "description": "Unique identifier of the employee.",
                }
            },
            "required": ["employee_id"],
        },
        "output_schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                    },
                    "project_name": {
                        "type": "string",
                    },
                },
                "required": [
                    "project_id",
                    "project_name",
                ],
            },
        },
        "input_example": {
            "employee_id": 1,
        },
    },
    {
        "name": "get_project_status",
        "description": "Return the current status and completion percentage of a project.",
        "source": "mcp",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "integer",
                    "description": "Unique identifier of the project.",
                }
            },
            "required": ["project_id"],
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "integer",
                },
                "status": {
                    "type": "string",
                },
                "completion_percentage": {
                    "type": "number",
                },
            },
            "required": [
                "project_id",
                "status",
                "completion_percentage",
            ],
        },
        "input_example": {
            "project_id": 101,
        },
    },
]