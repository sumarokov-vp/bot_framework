from enum import Enum


class RoleName(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"
    SUPERVISORS = "supervisors"
    CONTENT_MANAGER = "content_manager"
    FOUNDER = "founder"
    CLIENT = "client"
    PROJECT_MANAGER = "project_manager"
    INVOICES_MANAGER = "invoices_manager"
    EMPLOYEE = "employee"
