from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    message: str = Field(..., description="Health status message")
