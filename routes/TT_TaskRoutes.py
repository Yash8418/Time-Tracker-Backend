from fastapi import APIRouter
from models.TT_TaskModel import Task,TaskOut
from controllers.TT_TaskController import addTask,getTask, getAllTasksByDeveloperId

router=APIRouter()
@router.post("/addTask")
async def add_task(task:Task):
    return await addTask(task)
@router.get("/getTask")
async def get_task():
    return await getTask()
@router.get("/getAllTasksByDeveloperId/{developerId}")
async def get_all_tasks_by_developerId(developerId: str):
    return await getAllTasksByDeveloperId(developerId)
