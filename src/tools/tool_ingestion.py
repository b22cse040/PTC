TOOL_DEFINITIONS = [
    {
        "name": "get_employees_by_department",
        "description": "Return employees belonging to a specified department.",
        "input-schema": {
            "type": "object",
            "properties": {
                "department": {
                    "type": "string",
                    "description": "The department to search for."
                }
            },
            "required": ["department"]
        },
        "input_example": {
            "department": "Engineering"
        }
    },
    {
        "name": "filter_employees_by_salary",
        "description": "Return employees whose salary is greater than the specified amount.",
        "input-schema": {
            "type": "object",
            "properties": {
                "employees": {
                    "type": "array",
                    "description": "List of employee objects to filter."
                },
                "minimum_salary": {
                    "type": "number",
                    "description": "Minimum salary threshold. Employees must earn more than this value."
                }
            },
            "required": ["employees", "minimum_salary"]
        },
        "input_example": {
            "employees": [
                {
                    "id": 1,
                    "name": "Alice",
                    "department": "Engineering",
                    "salary": 45000
                }
            ],
            "minimum_salary": 30000
        }
    },
    {
        "name": "search_employees",
        "description": "Search employees using optional department and minimum salary filters.",
        "input-schema": {
            "type": "object",
            "properties": {
                "department": {
                    "type": "string",
                    "description": "Department to filter employees by."
                },
                "minimum_salary": {
                    "type": "number",
                    "description": "Minimum salary threshold. Employees must earn more than this value."
                }
            },
            "required": []
        },
        "input_example": {
            "department": "Engineering",
            "minimum_salary": 30000
        }
    },
    {
        "name": "get_employee_department",
        "description": "Return the name and department of every employee.",
        "input-schema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "input_example": {}
    },
    {
        "name": "get_employee_salary",
        "description": "Return the name and salary of every employee.",
        "input-schema": {
            "type": "object",
            "properties": {},
            "required": []
        },
        "input_example": {}
    },
    {
        "name": "get_employee_benefits",
        "description": "Return benefits information associated with a specific employee.",
        "input-schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                    "description": "Unique identifier of the employee."
                }
            },
            "required": ["employee_id"]
        },
        "input_example": {
            "employee_id": 1
        }
    },
    {
        "name": "calculate_employee_bonus",
        "description": "Calculate an employee's annual bonus using their performance score.",
        "input-schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                    "description": "Unique identifier of the employee."
                },
                "performance_score": {
                    "type": "number",
                    "description": "Employee performance score."
                }
            },
            "required": ["employee_id", "performance_score"]
        },
        "input_example": {
            "employee_id": 1,
            "performance_score": 0.9
        }
    },
    {
        "name": "get_company_holidays",
        "description": "Return the company's holidays for a specified year.",
        "input-schema": {
            "type": "object",
            "properties": {
                "year": {
                    "type": "integer",
                    "description": "Calendar year."
                }
            },
            "required": ["year"]
        },
        "input_example": {
            "year": 2026
        }
    },
    {
        "name": "get_employee_attendance",
        "description": "Return attendance statistics for a specific employee.",
        "input-schema": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "integer",
                    "description": "Unique identifier of the employee."
                }
            },
            "required": ["employee_id"]
        },
        "input_example": {
            "employee_id": 1
        }
    }
]