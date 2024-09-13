from fastapi import FastAPI, Request, File, UploadFile, Query, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from utils.item_process import *
from utils.util import *
import pandas as pd
from htc import predict
import random
import shutil
import sys
import os
import re

# const
FILES_PATH = "datadir/files"
STATIC_PATH = "src/static"
TEMPLATE_PATH = "src/templates"
UPLOAD_PATH = './datadir/uploads'

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
app.mount("/files", StaticFiles(directory=FILES_PATH), name="files")
templates = Jinja2Templates(directory=TEMPLATE_PATH)

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_PATH, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    return JSONResponse(content={"message": "File successfully uploaded", "filename": file.filename}, status_code=200)


# @TODO: renew
@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    def get_file_type(file_path):
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.csv':
            return 'csv'
        elif file_extension.lower() in ['.xls', '.xlsx']:
            return 'xlsx'
        else:
            return None

    file_path = os.path.join(UPLOAD_PATH, file.filename)
    file_type = get_file_type(file_path)
    if file_type == "csv":
        df = pd.read_csv(file_path, encoding='gbk')
    else:
        df = pd.read_excel(file_path, encoding='utf-8')
    html_table = df.to_html(index=False, classes="table table-striped table-hover")
    return HTMLResponse(content=html_table)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/get-files", response_model=List[List[str]])
async def get_files(folder: str = Query(..., description="The folder to list files from")):
    try:
        folder_list = json.loads(folder)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid folder format")

    folder_path = os.path.join(FILES_PATH, *folder_list)

    # 判断文件夹是否存在
    if not os.path.isdir(folder_path):
        raise HTTPException(status_code=404, detail="Folder not found")

    # 获取所有文件夹中的文件
    files = get_all_files_in_directory(folder_path)
    return files


class FileMoveRequest(BaseModel):
    file_name: str
    output_text: str

@app.post("/move-file")
async def move_file(request: FileMoveRequest):
    def convert_to_slash_format_regex(s):
        s = re.sub(r'-+', '/', s).strip('/')
        return s

    file_name = request.file_name
    output_text = request.output_text
    file_path = convert_to_slash_format_regex(output_text)

    if not file_name or not output_text:
        raise HTTPException(status_code=400, detail="File name and output text are required.")

    source_path = os.path.join(UPLOAD_PATH, file_name)
    dest_folder = os.path.join(FILES_PATH, file_path)

    try:
        # 获取目标路径
        dest_path = os.path.join(dest_folder, os.path.basename(source_path))

        # 如果文件已存在，先删除它
        if os.path.exists(dest_path):
            os.remove(dest_path)

        shutil.move(source_path, dest_folder)
        return {"message": "文件移动成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error moving file: {str(e)}")


@app.post("/dir-level")
async def dir_level(request: Request):
    return get_directory_structure(FILES_PATH)


@app.post("/process")
async def process(request: Request):
    data_json = await request.json()
    input_file = data_json['input_file']

    # 目录树
    predict_label_name = predict.run(input_file)
    cls = predict_label_name

    # 信息项
    origin_items, modify_items = run(input_file)
    origin_result = ""
    modify_result = ""

    for idx, item in enumerate(origin_items):
        origin_result += f"{idx + 1}. {item}\n"

    for idx, item in enumerate(modify_items):
        modify_result += f"{idx + 1}. {item}\n"

    return {
        "class": cls,
        "origin": origin_result,
        "modify": modify_result
    }
