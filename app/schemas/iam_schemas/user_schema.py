from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Request body for creating a user."""

    username: str = Field(..., min_length=1)
    email: Optional[str] = None
    password: str = Field(..., min_length=1)


class UserUpdate(BaseModel):
    """Request body for updating a user (all fields optional)."""

    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    """Response body for user endpoints."""

    model_config = ConfigDict(from_attributes=True)
    id: str
    username: str
    email: Optional[str] = None
