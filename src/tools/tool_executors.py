from src.tool_search_module.tool_executor import ToolExecutor, NativeToolExecutor, MCPToolExecutor
from src.tools.native_tools import *
# from mcp_tools import *

TOOL_EXECUTORS: Dict[str, ToolExecutor] = {
    "get_employees": NativeToolExecutor(get_employees),
    "get_employees_by_department": NativeToolExecutor(get_employees_by_department),
    "get_employee_department": NativeToolExecutor(get_employee_department),
    "get_employee_salary": NativeToolExecutor(get_employee_salary),
    "get_employee_benefits": MCPToolExecutor("get_employee_benefits"),
    "calculate_employee_bonus": MCPToolExecutor("calculate_employee_bonus"),
    "get_company_holidays": MCPToolExecutor("get_company_holidays"),
    "get_employee_attendance": MCPToolExecutor("get_employee_attendance"),
    "get_employee_projects": MCPToolExecutor("get_employee_projects"),
    "get_project_status": MCPToolExecutor("get_project_status"),
}