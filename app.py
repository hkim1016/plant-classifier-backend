from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus
from PIL import Image
from pytorch import analyze_plant, analyze_plant_live_view

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def health():
    print('HEALTH CHECK')
    return {
        'Status': 'OK'
    }

@app.post('/plant_analysis')
async def plant_analysis(file: UploadFile = File(...)):
    print('ANALYZING PLANT')
    print('filename: ', file.filename)
    return analyze_plant(file.file)

@app.post('/plant_analysis_live')
async def plant_analysis_live(file: UploadFile = File(...)):
    print('ANALYZING PLANT')
    print('filename: ', file.filename)
    return analyze_plant_live_view(file.file)