from pydantic import BaseModel,validator,Field
from typing import Optional,Dict,Any
from bson import ObjectId
from datetime import datetime

# moduleId	integer	primary key	
# projectId	integer	foreign key 	project
# moduleName	varchar	not null	
# description	varchar		
# estimatedHours			
# status 			
# startDate			

class ProjectModule(BaseModel):
    projectId:str
    moduleName:str
    description:str
    estimatedHours:int
    status:str
    startDate:datetime

class ProjectModuleOut(ProjectModule):
    id:str=Field(alias="_id")
    project_id: Optional[Dict[str,Any]] = None
    

    @validator('id', pre=True, always=True)
    def convert_objectId(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v
    
    @validator('project_id', pre=True, always=True)
    def convert_projectId(cls,v):
        if isinstance(v,Dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v