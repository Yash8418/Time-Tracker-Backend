from pydantic import BaseModel,validator,Field
from typing import Optional,Dict,Any
from bson import ObjectId
from datetime import datetime


class Project(BaseModel):
    # projectId	integer	primary key
    # title	varchar	not null
    # description	varchar	
    # technology	varchar	
    # estimatedHours	integer	
    # startDate	date	
    # completionDate	date	

    title:str
    description:str
    technology:str
    estimatedHours:int
    startDate:datetime
    completionDate:datetime

class ProjectOut(Project):
    id:str=Field(alias="_id")

    @validator('id', pre=True, always=True)
    def convert_obectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v