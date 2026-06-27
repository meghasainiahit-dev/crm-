import os

SERVICES = {
    "company": os.getenv("COMPANY_SERVICE"),
    "department": os.getenv("DEPARTMENT_SERVICE"),
    "employee": os.getenv("EMPLOYEE_SERVICE"),
    "auth": os.getenv("AUTH_SERVICE"),
}