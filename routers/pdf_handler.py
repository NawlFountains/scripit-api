from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse
from pdf_splitter import split_pdf 

router = APIRouter()

@router.post('/split')
async def split_pdf_endpoint(file: UploadFile , start_page: int, end_page: int):
    file_bytes = await file.read()
    output = split_pdf(file_bytes,start_page,end_page)
    return StreamingResponse(
            content = output,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=output.pdf"}
            )
