from __future__ import annotations

from datetime import date, datetime
from typing import Any, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from ares.domain.enums import MembershipRole, ProjectStatus, UserStatus

T = TypeVar("T")

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseSchema):
    email: EmailStr
    password: str
    display_name: str | None = None

class UserLogin(BaseSchema):
    email: EmailStr
    password: str

class UserResponse(BaseSchema):
    id: UUID
    email: EmailStr
    display_name: str | None
    status: UserStatus
    created_at: datetime
    updated_at: datetime | None

class TokenResponse(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class OrganizationCreate(BaseSchema):
    name: str
    slug: str

class OrganizationResponse(BaseSchema):
    id: UUID
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime | None

class MembershipCreate(BaseSchema):
    user_id: UUID
    role: MembershipRole

class MembershipResponse(BaseSchema):
    id: UUID
    organization_id: UUID
    user_id: UUID
    role: MembershipRole
    created_at: datetime
    updated_at: datetime | None

class ProjectCreate(BaseSchema):
    name: str
    description: str | None = None
    research_question: str | None = None
    inclusion_criteria: str | None = None
    exclusion_criteria: str | None = None
    date_from: date | None = None
    date_to: date | None = None

class ProjectUpdate(BaseSchema):
    name: str | None = None
    description: str | None = None
    research_question: str | None = None
    inclusion_criteria: str | None = None
    exclusion_criteria: str | None = None
    date_from: date | None = None
    date_to: date | None = None
    status: ProjectStatus | None = None

class ProjectResponse(BaseSchema):
    id: UUID
    organization_id: UUID
    name: str
    description: str | None
    research_question: str | None
    inclusion_criteria: str | None
    exclusion_criteria: str | None
    date_from: date | None
    date_to: date | None
    status: ProjectStatus
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    archived_at: datetime | None

class HealthResponse(BaseSchema):
    status: str
    database: str | None = None
    redis: str | None = None

class ErrorResponse(BaseSchema):
    error: str
    code: str
    details: Any | None = None

class PaginatedResponse[T](BaseSchema):
    items: list[T]
    total: int
    offset: int
    limit: int
    has_more: bool
