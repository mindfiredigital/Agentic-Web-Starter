from typing import Optional

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    """User domain model for IAM."""

    model_config = ConfigDict(frozen=True)

    id: str
    username: str
    email: Optional[str]
    hashed_password: str
    created_at: str
    created_by: Optional[str]
    updated_at: Optional[str]
    updated_by: Optional[str]


class Role(BaseModel):
    """Role domain model for IAM."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    description: Optional[str]
    created_at: str
    created_by: Optional[str]
    updated_at: Optional[str]
    updated_by: Optional[str]


class Component(BaseModel):
    """Component (resource/feature) domain model for ACL."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    component_uri: str
    created_at: str
    created_by: Optional[str]
    updated_at: Optional[str]
    updated_by: Optional[str]
