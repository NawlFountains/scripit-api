from fastapi import FastAPI
from routers import pdf_handler, letterboxd_handler

app = FastAPI(title='Scripting API')

app.include_router(pdf_handler.router, prefix='/pdf_handler', tags=['pdf_handler'])
app.include_router(letterboxd_handler.router, prefix='/letterboxd_handler', tags=['letterboxd_handler'])
