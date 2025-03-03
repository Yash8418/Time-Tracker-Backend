from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL="mongodb://localhost:27017"
TIMETRACKER_DATABASE_NAME="TimeTracker"

client=AsyncIOMotorClient(MONGO_URL)

timetracker_db=client[TIMETRACKER_DATABASE_NAME]
timetracker_user_collection=timetracker_db["users"]