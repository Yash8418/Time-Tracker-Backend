from models.TT_Project import Project,ProjectOut
from bson import ObjectId
from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from config.TT_Db import timetracker_projet_collection


async def addProject(project:Project):
    savedProject = await timetracker_projet_collection.insert_one(project.dict())
    return JSONResponse(content={"Message":"Project added successfully"},status_code=201)

async def getAllProjects():
    projects=await timetracker_projet_collection.find().to_list()
    return [ProjectOut(**project) for project in projects]