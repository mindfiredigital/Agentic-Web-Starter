from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Request body for login endpoint."""

    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Response body with JWT access token."""

    access_token: str
    token_type: str = "bearer"
