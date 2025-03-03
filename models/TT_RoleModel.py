from pydantic import BaseModel,validator,Field
from typing import Optional,Dict,Any
from bson import ObjectId

class UserSignup(BaseModel):
    username:str
    password:str
    role:str
    

class UserLogin(BaseModel):
    username:str
    password:str



