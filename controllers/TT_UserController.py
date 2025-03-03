from models.TT_RoleModel import UserSignup,UserLogin
from config.TT_Db import timetracker_user_collection
from bson import ObjectId

async def addUser(user:UserSignup):
    result = await timetracker_user_collection.insert_one(user.dict())
    return {"Message":"User added successfully"}

# async def getUser(username:str,password:str):
#     result = await timetracker_user_collection.find_one({"username":username,"password":password})
#     print("result.....",result)
#     if result is None:
#         return {"Message":"User NOT found"}
#     return {"Message":"User FOUND successfully"}

async def getUser(username: str, password: str):
    result = await timetracker_user_collection.find_one({"username": username})

    if result is None:
        return {"Message": "User NOT found"}

    return {
        "Message": "User FOUND successfully",
        "role": result.get("role", "User")  # Return role
    }

