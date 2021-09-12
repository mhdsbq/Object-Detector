import os
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import aiofiles 
from load_detector_model import load_detector_model
from object_detector import object_detector

from fastapi.encoders import jsonable_encoder

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="")

detector = load_detector_model()

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.post('/detect')
async def predict(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    result = object_detector(detector, file_location)

    os.remove(file_location)

    return jsonable_encoder(result)