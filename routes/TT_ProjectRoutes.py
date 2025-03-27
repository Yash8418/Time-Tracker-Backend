from fastapi import APIRouter
from models.TT_Project import Project,ProjectOut
from controllers.TT_ProjectController import addProject,getAllProjects, getAllProjectsByUserId

router = APIRouter()
@router.post("/addProject/")
async def add_project(project:Project):
    return await addProject(project)

@router.get("/getAllProjects/")
async def get_all_projects():
    return await getAllProjects()

@router.get("/getAllProjectsByUserId/{userId}")
async def get_all_projects_by_user_id(userId:str):
    return await getAllProjectsByUserId(userId)

