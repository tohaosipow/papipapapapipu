from fastapi import APIRouter

from api.api_v1.endpoints import users, settings, calls, time_table
from api.api_v1.endpoints import community

api_router = APIRouter()

api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(community.router, prefix='/community', tags=['community'])
api_router.include_router(settings.router, prefix='/settings', tags=['settings'])
api_router.include_router(calls.router, prefix='/calls', tags=['calls'])
api_router.include_router(time_table.router, prefix='/time_table', tags=['time_table'])
