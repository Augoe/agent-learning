# Pydantic 数据模型

from pydantic import BaseModel,Field,ConfigDict
from typing import Any

class ToolCall(BaseModel):

    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1)
    arguments: dict[str, Any]

class AddInput(BaseModel):

    model_config = ConfigDict(extra="forbid")
    a: int = Field(strict=True)
    b: int = Field(strict=True)

class RepeatInput(BaseModel):

    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1)
    count: int = Field(ge=1, le=10, strict=True)

