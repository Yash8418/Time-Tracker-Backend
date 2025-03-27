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
    print(projects)
    return [ProjectOut(**project) for project in projects]

# async def getAllProjectsByUserId(userId:str):
#     projects=await timetracker_projet_collection.find({"_id":userId}).to_list()
#     return [ProjectOut(**project) for project in projects]
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

async def getAllProjectsByUserId(userId: str):
    try:
        # Ensure userId is stored as a string, not as ObjectId
        projects = await timetracker_projet_collection.find({"userId": userId}).to_list(None)

        # Convert MongoDB results into Pydantic models
        return [ProjectOut(**project) for project in projects]

    except Exception as e:
        print(f"Error fetching projects: {e}")
        return []
