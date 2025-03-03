# Import FastAPI 
from fastapi import FastAPI
from routes.UserRoutes import router as user_router
from routes.TT_UserRoutes import router as tt_user_router
from fastapi.middleware.cors import CORSMiddleware

# Object of FastAPI
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(tt_user_router)