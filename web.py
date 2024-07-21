from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
import base64
from io import BytesIO
from typing import Optional
from validator import *
import time
from database import *
from randomgen import *

app = FastAPI()
templating = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templating.TemplateResponse("index.html", {
        "request": request})

class FileUpload(BaseModel):
    file_data: str

@app.post("/upload")
async def upload_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    file1_bytes = await file1.read()
    file2_bytes = await file2.read()

    # Convert to base64
    file1_base64 = base64.b64encode(file1_bytes).decode('utf-8')
    file2_base64 = base64.b64encode(file2_bytes).decode('utf-8')

    if is_base64_image(file1_base64) == False:
        return "im1error"
    elif is_base64_image(file2_base64) == False:
        return "im2error"
    else:
        succ_id = upsuccess_verif_genid()
        filever_add(succ_id)
        return "success_"+str(succ_id)

# This is just a placeholder to show how you might handle the base64 encoding
# on the client side and convert it back to files on the server side.
@app.get("/up-success/{filever_id}")
async def upsuccess(request: Request, filever_id: int):    
    is_ok = filever_verif(filever_id)
    if is_ok == True:
        return templating.TemplateResponse("process.html", {"request": request, "ver_id": filever_id})
    else:
        return templating.TemplateResponse("nopermit.html", {"request": request})


@app.post("/status-update/{ver_id}")
async def upload_files(ver_id: int):
    
    return 
