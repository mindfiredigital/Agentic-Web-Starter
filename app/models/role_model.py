from typing import Optional

from pydantic import BaseModel, ConfigDict


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
