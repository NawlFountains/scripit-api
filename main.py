from fastapi import FastAPI
from routers import pdf_handler, letterboxd_handler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Scripting API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://scripit.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_handler.router, prefix='/pdf_handler', tags=['pdf_handler'])
app.include_router(letterboxd_handler.router, prefix='/letterboxd_handler', tags=['letterboxd_handler'])
