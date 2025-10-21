from models.TT_TaskModel import Task, TaskOut, TaskUpdate
from bson import ObjectId
from config.TT_Db import (
    timetracker_task_collection,
    timetracker_projet_module_collection,
    timetracker_projet_collection,
    timetracker_status_collection,
    timetracker_user_collection
)
from fastapi.responses import JSONResponse
from datetime import datetime

def format_seconds_to_hhmmss(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) % 60 // 60
    secs = seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"

async def addTask(task: Task):
    await timetracker_task_collection.insert_one(task.dict())
    return JSONResponse(content={"message": "Task added successfully"})

async def getTask():
    tasks = await timetracker_task_collection.find().to_list(length=None)
    enriched_tasks = []

    for task in tasks:
        task["_id"] = str(task["_id"])

        # Convert assignedDevelopers to detailed dev_id list
        if "assignedDevelopers" in task:
            dev_ids = task["assignedDevelopers"]
            task["dev_id"] = [
                {
                    **dev,
                    "_id": str(dev["_id"])
                }
                for dev_id in dev_ids
                if (dev := await timetracker_user_collection.find_one({"_id": ObjectId(dev_id)}))
            ]

        # Enrich references
        if "moduleId" in task:
            module = await timetracker_projet_module_collection.find_one({"_id": ObjectId(task["moduleId"])})
            if module:
                module["_id"] = str(module["_id"])
                task["module_id"] = module

        if "projectId" in task:
            project = await timetracker_projet_collection.find_one({"_id": ObjectId(task["projectId"])})
            if project:
                project["_id"] = str(project["_id"])
                task["project_id"] = project

        if "statusId" in task:
            status = await timetracker_status_collection.find_one({"_id": ObjectId(task["statusId"])})
            if status:
                status["_id"] = str(status["_id"])
                task["status_id"] = status

        if "timeSpent" in task:
            task["formattedTimeSpent"] = format_seconds_to_hhmmss(task["timeSpent"])

        if "totalMinutes" in task:
            task["formattedExpectedTime"] = format_seconds_to_hhmmss(task["totalMinutes"] * 60)
        task["assignedDevelopers"] = [str(dev_id) for dev_id in task.get("assignedDevelopers", [])]

        enriched_tasks.append(TaskOut(**task))

    return enriched_tasks

async def getAllTasksByDeveloperId(developerId: str):
    tasks = await timetracker_task_collection.find({"assignedDevelopers": developerId}).to_list(None)
    enriched_tasks = []

    for task in tasks:
        task["_id"] = str(task["_id"])

        # Convert assignedDevelopers to detailed dev_id list
        if "assignedDevelopers" in task:
            dev_ids = task["assignedDevelopers"]
            task["dev_id"] = [
                {
                    **dev,
                    "_id": str(dev["_id"])
                }
                for dev_id in dev_ids
                if (dev := await timetracker_user_collection.find_one({"_id": ObjectId(dev_id)}))
            ]

        if "moduleId" in task:
            module = await timetracker_projet_module_collection.find_one({"_id": ObjectId(task["moduleId"])})
            if module:
                module["_id"] = str(module["_id"])
                task["module_id"] = module

        if "projectId" in task:
            project = await timetracker_projet_collection.find_one({"_id": ObjectId(task["projectId"])})
            if project:
                project["_id"] = str(project["_id"])
                task["project_id"] = project

        if "statusId" in task:
            status = await timetracker_status_collection.find_one({"_id": ObjectId(task["statusId"])})
            if status:
                status["_id"] = str(status["_id"])
                task["status_id"] = status
        task["assignedDevelopers"] = [str(dev_id) for dev_id in task.get("assignedDevelopers", [])]

        enriched_tasks.append(TaskOut(**task))

    return enriched_tasks

async def startTask(taskId: str):
    task = await timetracker_task_collection.find_one({"_id": ObjectId(taskId)})
    if not task:
        return JSONResponse(content={"message": "Task not found"}, status_code=404)

    if "startTime" in task and task["startTime"]:
        return JSONResponse(content={"message": "Task is already running"}, status_code=400)

    running_status = await timetracker_status_collection.find_one({"statusName": "running"})
    if not running_status:
        return JSONResponse(content={"message": "Running status not found"}, status_code=500)

    now_iso = datetime.utcnow().isoformat()
    await timetracker_task_collection.update_one(
        {"_id": ObjectId(taskId)},
        {"$set": {"startTime": now_iso, "statusId": str(running_status["_id"])}}
    )
    return JSONResponse(content={"message": "Task started successfully", "startTime": now_iso})

async def stopTask(taskId: str):
    task = await timetracker_task_collection.find_one({"_id": ObjectId(taskId)})
    if not task:
        return JSONResponse(content={"message": "Task not found"}, status_code=404)

    if "startTime" not in task or not task["startTime"]:
        return JSONResponse(content={"message": "Task has not been started yet"}, status_code=400)

    try:
        start_time = datetime.fromisoformat(task["startTime"])
        elapsed_seconds = int((datetime.utcnow() - start_time).total_seconds())

        pending_status = await timetracker_status_collection.find_one({"statusName": "pending"})
        if not pending_status:
            return JSONResponse(content={"message": "Pending status not found"}, status_code=500)

        await timetracker_task_collection.update_one(
            {"_id": ObjectId(taskId)},
            {
                "$set": {
                    "statusId": str(pending_status["_id"]),
                    "timeSpent": task.get("timeSpent", 0) + elapsed_seconds
                },
                "$unset": {"startTime": ""}
            }
        )

        return JSONResponse(content={"message": "Task stopped successfully", "timeSpent": elapsed_seconds})
    except ValueError as e:
        return JSONResponse(content={"message": f"Invalid startTime format: {str(e)}"}, status_code=500)

async def completeTask(taskId: str):
    task = await timetracker_task_collection.find_one({"_id": ObjectId(taskId)})
    if not task:
        return JSONResponse(content={"message": "Task not found"}, status_code=404)

    completed_status = await timetracker_status_collection.find_one({"statusName": "completed"})
    if not completed_status:
        return JSONResponse(content={"message": "Status not found"}, status_code=500)

    await timetracker_task_collection.update_one(
        {"_id": ObjectId(taskId)},
        {"$set": {"statusId": str(completed_status["_id"])}}
    )
    return JSONResponse(content={"message": "Task completed successfully"})

async def updateTask(taskId: str, task: TaskUpdate):
    update_data = task.dict(exclude_unset=True)
    if not update_data:
        return JSONResponse(content={"message": "No updates provided"}, status_code=400)

    result = await timetracker_task_collection.update_one(
        {"_id": ObjectId(taskId)},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        return JSONResponse(content={"message": "Task not found or no changes made"}, status_code=404)

    return JSONResponse(content={"message": "Task updated successfully"})
