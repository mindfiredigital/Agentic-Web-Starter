from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RoleCreate(BaseModel):
    """Request body for creating a role."""
    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    """Request body for updating a role (all fields optional)."""
    name: Optional[str] = None
    description: Optional[str] = None


class RoleResponse(BaseModel):
    """Response body for role endpoints."""
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    description: Optional[str] = None

