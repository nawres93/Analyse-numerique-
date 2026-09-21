# app/schemas/module_schema.py

from pydantic import BaseModel
from typing import Optional


class ModuleCreate(BaseModel):
    title: str
    description: str
    lessons: int
    resources: int
    visibility: str = "Private"
    status: str = "Draft"


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    lessons: Optional[int] = None
    resources: Optional[int] = None
    visibility: Optional[str] = None
    status: Optional[str] = None


class ModuleResponse(BaseModel):
    id: str
    title: str
    description: str
    lessons: int
    resources: int
    visibility: str
    status: str