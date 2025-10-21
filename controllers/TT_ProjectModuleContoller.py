from bson import ObjectId
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from config.TT_Db import timetracker_projet_module_collection, timetracker_projet_collection, timetracker_user_collection
from models.TT_ProjectModule import ProjectModule, ProjectModuleOut, ProjectModulePartialUpdate


async def addProjectModule(project_module: ProjectModule):
    data = project_module.dict()
    
    # Ensure projectId is stored as a string (do not convert to ObjectId)
    if "projectId" in data and ObjectId.is_valid(data["projectId"]):
        # Ensure it remains as a string (not an ObjectId)
        data["projectId"] = str(data["projectId"])  # Store as string
    else:
        raise HTTPException(status_code=400, detail="Invalid project ID format")

    # Insert the module data
    savedProjectModule = await timetracker_projet_module_collection.insert_one(data)
    return JSONResponse(content={"message": "Project Module added successfully"}, status_code=201)


async def getProjectModule():
    projectModules = await timetracker_projet_module_collection.find().to_list(length=None)

    for project in projectModules:
        # Fetch project details (use the projectId as a string)
        if "projectId" in project:
            project_data = await timetracker_projet_collection.find_one({"_id": ObjectId(project["projectId"])})
            project["project_id"] = project_data if project_data else None

        # Fetch assigned developers
        if "assignedDevelopers" in project and isinstance(project["assignedDevelopers"], list):
            developer_list = []
            for dev_id in project["assignedDevelopers"]:
                if ObjectId.is_valid(dev_id):
                    dev_data = await timetracker_user_collection.find_one({"_id": ObjectId(dev_id)})
                    if dev_data:
                        developer_list.append({
                            "_id": str(dev_data["_id"]),
                            "username": dev_data.get("username", "Unknown Developer")
                        })
            project["dev_id"] = developer_list  # Ensure it's correctly assigned

    return [ProjectModuleOut(**project) for project in projectModules]


async def getProjectModuleByProjectId(projectId: str):
    filter_query = {}

    # Ensure projectId is passed as a string (no conversion to ObjectId needed)
    if projectId:
        filter_query["projectId"] = projectId  # Handle it as a string in the query
    else:
        raise HTTPException(status_code=400, detail="Invalid project ID")

    projectModules = await timetracker_projet_module_collection.find(filter_query).to_list(length=None)
    
    for project in projectModules:
        if "projectId" in project:
            project_data = await timetracker_projet_collection.find_one({"_id": ObjectId(project["projectId"])})
            if project_data:
                project_data["_id"] = str(project_data["_id"])
                project["project_id"] = project_data
            else:
                project["project_id"] = None

    return [ProjectModuleOut(**project) for project in projectModules]


async def partiallyUpadateModule(projectModuleId: str, projectModule: ProjectModulePartialUpdate):
    if not ObjectId.is_valid(projectModuleId):
        raise HTTPException(status_code=400, detail="Invalid module ID format")
    
    update_fields = projectModule.dict(exclude_unset=True)
    
    # Ensure assignedDevelopers is a list of strings
    if "assignedDevelopers" in update_fields:
        update_fields["assignedDevelopers"] = [str(dev_id) for dev_id in update_fields["assignedDevelopers"]]
    
    result = await timetracker_projet_module_collection.update_one(
        {"_id": ObjectId(projectModuleId)},
        {"$set": update_fields}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Project Module not found")
    
    return JSONResponse(content={"message": "Project Module updated successfully"}, status_code=200)
