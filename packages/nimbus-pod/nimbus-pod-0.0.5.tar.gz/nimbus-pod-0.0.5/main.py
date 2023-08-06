#!/usr/bin/env python3

from fastapi import FastAPI
from setuptools import setup, find_packages  

setup(name = 'nimbus_pod', packages = find_packages())

# from .dependencies import get_query_token, get_token_header
# from .internal import admin
from .routers import system, services, diagnostics
from .utils import log

app = FastAPI()  # dependencies=[Depends(get_query_token)])

# Public 
app.include_router(system.router)
app.include_router(services.router)
app.include_router(diagnostics.router)

# Internal
# app.include_router(admin.router)

log.create_log_file()

@app.get('/')
async def root():
    return {
        "message": "Nimbus says hi"
    }

log.record_app_event('Nimbus-Pod App running')
