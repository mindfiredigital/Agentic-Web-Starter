from typing import Optional

from pydantic import BaseModel, ConfigDict


class User(BaseModel):
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
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    description: Optional[str]
    created_at: str
    created_by: Optional[str]
    updated_at: Optional[str]
    updated_by: Optional[str]


class Component(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    component_uri: str
    created_at: str
    created_by: Optional[str]
    updated_at: Optional[str]
    updated_by: Optional[str]
