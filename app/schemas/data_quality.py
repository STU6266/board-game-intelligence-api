from pydantic import BaseModel, Field


class DataQualityIssue(BaseModel):
    field: str
    message: str


class DataQualityResult(BaseModel):
    is_valid: bool
    errors: list[DataQualityIssue] = Field(default_factory=list)
    warnings: list[DataQualityIssue] = Field(default_factory=list)