from models.TT_Project import Project,ProjectOut
from bson import ObjectId
from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from config.TT_Db import timetracker_projet_collection, timetracker_user_collection
from motor.motor_asyncio import AsyncIOMotorCollection
import json
async def addProject(project:Project):
    savedProject = await timetracker_projet_collection.insert_one(project.dict())
    return JSONResponse(content={"Message":"Project added successfully"},status_code=201)

# async def getAllProjects():
#     projects=await timetracker_projet_collection.find().to_list()
#     # print(projects)
#     # assignedDevelopers:str
#     # userId:str
#     for project in projects:
#         if "userId" in project:
#             user_data = await timetracker_user_collection.find_one({"_id": ObjectId(project["userId"])})
#             if user_data:
#                 user_data["_id"] = str(user_data["_id"])
#                 project["user_id"] = user_data
#             else:
#                 project["user_id"] = None

#         # Fix assignedDevelopers field (Convert string to array if needed)
#         if "assignedDevelopers" in project:
#             if isinstance(project["assignedDevelopers"], str):  
#                 try:
#                     project["assignedDevelopers"] = json.loads(project["assignedDevelopers"])  # Convert string to list
#                 except json.JSONDecodeError:
#                     project["assignedDevelopers"] = []
#         if "assignedDevelopers" in project and isinstance(project["assignedDevelopers"], list):
#             project["assignedDevelopers"] = [ObjectId(dev_id) for dev_id in project["assignedDevelopers"]]
            
#             developers_data = await timetracker_user_collection.find({"_id": {"$in": project["assignedDevelopers"]}}).to_list(None)
#             print(developers_data)
#             for dev in developers_data:
#                 dev["_id"] = str(dev["_id"])

#             project["developers"] = developers_data
#         else:
#             project["developers"] = []



#     return [ProjectOut(**project) for project in projects]

async def getAllProjects():
    projects = await timetracker_projet_collection.find().to_list(None)

    for project in projects:
        if "userId" in project:
            user_data = await timetracker_user_collection.find_one({"_id": ObjectId(project["userId"])})
            if user_data:
                user_data["_id"] = str(user_data["_id"])
                project["user_id"] = user_data
            else:
                project["user_id"] = None

        if "assignedDevelopers" in project and isinstance(project["assignedDevelopers"], list):
            developer_list = []
            for dev_id in project["assignedDevelopers"]:
                dev_data = await timetracker_user_collection.find_one({"_id": ObjectId(dev_id)})
                if dev_data:
                    dev_data["_id"] = str(dev_data["_id"])
                    developer_list.append(dev_data)
            project["dev_id"] = developer_list


    return [ProjectOut(**project) for project in projects]
async def getAllProjectsByUserId(userId: str):
    try:
        projects = await timetracker_projet_collection.find({
            "$or": [
                {"userId": userId},  # 🔹 Projects created by this user
                {"assignedDevelopers": {"$elemMatch": {"id": userId}}}  # 🔹 Projects assigned to this user
            ]
        }).to_list(None)

        # Convert MongoDB results into Pydantic models
        return [ProjectOut(**project) for project in projects]

    except Exception as e:
        print(f"Error fetching projects: {e}")
        return []
    
async def getAllProjectsByDeveloperId(developerId:str):
    try:
        projects = await timetracker_projet_collection.find({
            "assignedDevelopers": {"$elemMatch": {"id": developerId}}
        }).to_list(None)

        # Convert MongoDB results into Pydantic models
        return [ProjectOut(**project) for project in projects]
    except Exception as e:
        print(f"Error fetching projects: {e}")
        return []