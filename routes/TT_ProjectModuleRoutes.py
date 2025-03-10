from fastapi import APIRouter
from models.TT_ProjectModule import ProjectModule,ProjectModuleOut
from controllers.TT_ProjectModuleContoller import addProjectModule,getProjectModule

router=APIRouter()
@router.post("/addProjectModule")
async def add_project_module(project_module:ProjectModule):
    return await addProjectModule(project_module)
@router.get("/getProjectModule")
async def get_project_module():
    return await getProjectModule()