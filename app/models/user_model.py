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
