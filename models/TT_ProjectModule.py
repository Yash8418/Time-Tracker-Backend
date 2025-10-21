from pydantic import BaseModel, validator, Field
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

class ProjectModule(BaseModel):
    projectId: str
    moduleName: str
    description: str
    estimatedHours: int
    startDate: datetime
    assignedDevelopers: List[str]

class ProjectModuleOut(ProjectModule):
    id: str = Field(alias="_id")
    project_id: Optional[dict] = None
    dev_id: Optional[List[dict]] = None
    
    @validator('id', pre=True, always=True)
    def convert_objectId(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    @validator('project_id', pre=True, always=True)
    def convert_projectId(cls, v):
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v

    @validator("dev_id", pre=True, always=True)
    def convert_assignedDevelopers(cls, v):
        if isinstance(v, list):
            for dev in v:
                if isinstance(dev, dict) and "_id" in dev:
                    dev["_id"] = str(dev["_id"])
        return v

class ProjectModulePartialUpdate(BaseModel):
    projectId: Optional[str] = None
    moduleName: Optional[str] = None
    description: Optional[str] = None
    estimatedHours: Optional[int] = None
    startDate: Optional[datetime] = None
    assignedDevelopers: Optional[List[str]] = None
