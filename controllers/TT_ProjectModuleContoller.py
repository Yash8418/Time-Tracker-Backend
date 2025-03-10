# moduleId	integer	primary key	
# projectId	integer	foreign key 	project
# moduleName	varchar	not null	
# description	varchar		
# estimatedHours			
# status 			
# startDate	



from models.TT_ProjectModule import ProjectModule,ProjectModuleOut
from bson import ObjectId
from config.TT_Db import timetracker_projet_module_collection,timetracker_projet_collection
from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse


async def addProjectModule(project_module:ProjectModule):
    savedProjectModule=await timetracker_projet_module_collection.insert_one(project_module.dict())
    return JSONResponse(content={"message":"Project Module added successfully"})

async def getProjectModule():
    projectModules = await timetracker_projet_module_collection.find().to_list(length=None)
    print(projectModules)
    for project in projectModules:

        # Fetch project details
        if "projectId" in project:
            project_data = await timetracker_projet_collection.find_one({"_id": ObjectId(project["projectId"])})
            if project_data:
                project_data["_id"] = str(project_data["_id"])
                project["project_id"] = project_data
            else:
                project["project_id"] = None

    return [ProjectModuleOut(**project) for project in projectModules]