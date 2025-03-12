# taskId	integer	primary key	
# moduleId	integer	foreign key	module
# projectId	integer	foreign key	project
# title			
# priority	varcahr		
# description	varchar	not null	
# statusId	integer	foreign key	status 
# totalMinutes	integer		

from pydantic import BaseModel,validator,Field
from typing import Optional,Dict,Any
from bson import ObjectId

class Task(BaseModel):
    moduleId:str
    projectId:str
    title:str
    priority:str
    description:str
    statusId:str
    totalMinutes:int

class TaskOut(Task):
    id:str=Field(alias="_id")
    module_id: Optional[Dict[str,Any]] = None
    project_id: Optional[Dict[str,Any]] = None
    status_id: Optional[Dict[str,Any]] = None

    @validator('id', pre=True, always=True)
    def convert_task_id(cls,v):
        if isinstance(v,ObjectId):
            return str(v)
        return v

    @validator('module_id', pre=True, always=True)
    def convert_module_id(cls,v):
        if isinstance(v,Dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v
    
    @validator('project_id', pre=True, always=True)
    def convert_project_id(cls,v):
        if isinstance(v,Dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v    
    
    @validator('status_id', pre=True, always=True)
    def convert_status_id(cls,v):
        if isinstance(v,Dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v