from fastapi import FastAPI
from routers import pdf_handler

app = FastAPI(title='PDF handler API')

app.include_router(pdf_handler.router, prefix='/pdf_handler', tags=['pdf_handler'])
