from fastapi  import FastAPI, File, UploadFile
import shutil
from pathlib import Path
import os,sys
import time

app = FastAPI()
DATA_DIR = Path("./sample_docs")
DATA_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file:UploadFile = File(...)):
    file_path = DATA_DIR/file.filename
    
    ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx", ".xlsx"}
    if file_path.suffix not in ALLOWED_EXTENSIONS:
        return {"error": "File type not allowed"}
    else:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file,buffer)
        return {"status": "uploaded successfully", "filename": file.filename}


