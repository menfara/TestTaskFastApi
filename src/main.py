# Third Party Library
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from fastapi_common.db import init_db

# Application Library
from .api import router
from .conf import settings

app = FastAPI(
	title=settings.project,
	default_response_class=ORJSONResponse,
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_methods=['*'],
	allow_headers=['*'],
	allow_credentials=True
)

app.include_router(router)


@app.on_event('startup')
async def startup():
	init_db(settings.database_dsn)
