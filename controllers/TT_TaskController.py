from models.TT_TaskModel import Task,TaskOut
from bson import ObjectId
from config.TT_Db import timetracker_task_collection,timetracker_projet_module_collection,timetracker_projet_collection,timetracker_status_collection
from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse

async def addTask(task:Task):
    savedTask=await timetracker_task_collection.insert_one(task.dict())
    return JSONResponse(content={"message":"Task added successfully"})

async def getTask():
    tasks = await timetracker_task_collection.find().to_list(length=None)
    for task in tasks:

        # Fetch module details
        if "moduleId" in task:
            module_data = await timetracker_projet_module_collection.find_one({"_id": ObjectId(task["moduleId"])})
            if module_data:
                module_data["_id"] = str(module_data["_id"])
                task["module_id"] = module_data
            else:
                task["module_id"] = None

        # Fetch project details
        if "projectId" in task:
            project_data = await timetracker_projet_collection.find_one({"_id": ObjectId(task["projectId"])})
            if project_data:
                project_data["_id"] = str(project_data["_id"])
                task["project_id"] = project_data
            else:
                task["project_id"] = None

        # Fetch status details
        if "statusId" in task:
            status_data = await timetracker_status_collection.find_one({"_id": ObjectId(task["statusId"])})
            if status_data:
                status_data["_id"] = str(status_data["_id"])
                task["status_id"] = status_data
            else:
                task["status_id"] = None

    return [TaskOut(**task) for task in tasks]