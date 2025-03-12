
from fastapi import APIRouter
from models.TT_TaskModel import Task,TaskOut
from controllers.TT_TaskController import addTask,getTask

router=APIRouter()
@router.post("/addTask")
async def add_task(task:Task):
    return await addTask(task)
@router.get("/getTask")
async def get_task():
    return await getTask()
