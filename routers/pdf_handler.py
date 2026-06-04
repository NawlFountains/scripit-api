from fastapi import APIRouter, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse 
from pdf_splitter import split_pdf 
import os

router = APIRouter()

@router.post('/split')
async def split_pdf_endpoint(file: UploadFile, start_page: int, end_page: int, background_tasks: BackgroundTasks):
    file_bytes = await file.read()
    tmp_path = split_pdf(file_bytes, start_page, end_page)
    background_tasks.add_task(os.remove, tmp_path)
    return FileResponse(
        tmp_path,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=output.pdf"}
    )
