from fastapi import APIRouter
from models.TT_ProjectModule import ProjectModule, ProjectModulePartialUpdate
from controllers.TT_ProjectModuleContoller import addProjectModule, getProjectModule, getProjectModuleByProjectId, partiallyUpadateModule

router = APIRouter()

@router.post("/addProjectModule")
async def add_project_module(project_module: ProjectModule):
    return await addProjectModule(project_module)

@router.get("/getProjectModule")
async def get_project_module():
    return await getProjectModule()

@router.get("/getProjectModule/{projectId}")
async def get_project_module_by_projectId(projectId: str):
    return await getProjectModuleByProjectId(projectId)

@router.patch("/partialUpdateProjectModule/{projectModuleId}")
async def partial_update_project(projectModuleId: str, updateData: ProjectModulePartialUpdate):
    return await partiallyUpadateModule(projectModuleId, updateData)
