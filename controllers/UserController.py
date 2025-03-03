from config.database import user_collection
from models.RoleModel import User,UserOut
from bson import ObjectId


async def getAllUser():
    users=await user_collection.find().to_list(length=None)
    return [UserOut(**user) for user in users]

async def addUser(user:User):
    result = await user_collection.insert_one(user.dict())
    return {"Message":"User added successfully"}

async def delUser(userId:str):
    result = await user_collection.delete_one({"_id":ObjectId(userId)})
    return {"Message":"User deleterd successfully"}

async def getUser(userId:str):
    result = await user_collection.find_one({"_id":ObjectId(userId)})
    return UserOut(**result)