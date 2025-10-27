from enum import Enum


class UserRoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class LevelEnum(str, Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"
    LEAD = "lead"


class ProjectStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"
    COMPLETED = "completed"


class ApplicationStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"
