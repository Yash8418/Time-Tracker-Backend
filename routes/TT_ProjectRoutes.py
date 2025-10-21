from fastapi import APIRouter, HTTPException, Body
from models.TT_Project import Project, ProjectOut, ProjectPartialUpdate
from controllers.TT_ProjectController import addProject, getAllProjects, getAllProjectsByUserId, getAllProjectsByDeveloperId, partialUpdateProject
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

# Router definition
router = APIRouter()

# MongoDB Client Initialization (ensure db and modules are defined correctly in your code)
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["admin"]  # Use the correct database

@router.post("/addProject/")
async def add_project(project: Project):
    return await addProject(project)

@router.get("/getAllProjects/")
async def get_all_projects():
    return await getAllProjects()

@router.get("/getProjectModule/{project_id}")
async def get_modules_by_project(project_id: str):
    try:
        # Check if the project_id is a valid ObjectId
        if not ObjectId.is_valid(project_id):
            raise HTTPException(status_code=400, detail="Invalid project ID format")

        # Convert the project_id string to ObjectId
        # project_obj_id = ObjectId(project_id)

        # Query the modules collection by projectId
        # modules = await db.modules.find({"projectId": project_obj_id}).to_list(length=100)
        modules = await db.modules.find({"projectId": project_id}).to_list(length=100)

        if not modules:
            # Instead of throwing an error here, we can just return an empty array or a custom message
            return {"message": "No modules found for this project", "modules": []}

        return modules
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get("/getAllProjectsByUserId/{userId}")
async def get_all_projects_by_userId(userId: str):
    return await getAllProjectsByUserId(userId)

@router.get("/getAllProjectsByDeveloperId/{developerId}")
async def get_all_projects_by_developerId(developerId: str):
    return await getAllProjectsByDeveloperId(developerId)

@router.patch("/partialUpdateProject/{projectId}")
async def partial_update_project(projectId: str, updateData: ProjectPartialUpdate = Body(...)):
    try:
        # Check if the projectId is a valid ObjectId
        if not ObjectId.is_valid(projectId):
            raise HTTPException(status_code=400, detail="Invalid project ID format")

        # Proceed with the partial update operation
        return await partialUpdateProject(projectId, updateData)

    except Exception as e:
        # Handle any errors during the partial update process
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
