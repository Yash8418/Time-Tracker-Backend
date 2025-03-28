from pydantic import BaseModel,validator,Field
from typing import Optional,Dict,List,Any
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
    userId:str
    # assignedDevelopers: List[str] 
    assignedDevelopers: str

class ProjectOut(Project):
    id:str=Field(alias="_id")
    # user_id: Optional[Dict[str,Any]] = None
    @validator('id', pre=True, always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
    # @validator('user_id', pre=True, always=True)
    # def convert_user_id(cls,v):
    #     if isinstance(v,Dict) and "_id" in v:
    #         v["_id"] = str(v["_id"])
    #     return v
    
