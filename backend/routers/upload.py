from fastapi import APIRouter, UploadFile, File
from storage import save_upload_file

router = APIRouter()

@router.post("/upload")
def upload_image(file: UploadFile = File(...)):
    file_path = save_upload_file(file)
    return {"filename": file.filename, "saved_path": file_path}
