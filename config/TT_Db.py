from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL="mongodb://localhost:27017"
TIMETRACKER_DATABASE_NAME="TimeTracker"

client=AsyncIOMotorClient(MONGO_URL)

timetracker_db=client[TIMETRACKER_DATABASE_NAME]
timetracker_user_collection=timetracker_db["users"]
timetracker_projet_collection=timetracker_db["projects"]
timetracker_projet_team_collection=timetracker_db["project_team"]