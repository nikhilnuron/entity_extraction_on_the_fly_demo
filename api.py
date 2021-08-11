from fastapi import FastAPI
import uvicorn
from fastapi import APIRouter, Form, status, HTTPException, UploadFile, File, Depends
from io import BytesIO
from fastapi.responses import ORJSONResponse

from demo_rain import caller_wrapper

app = FastAPI()

@app.get('/')
def helloworld():
    return "hello world"

@app.post('/extract_entities', response_class=ORJSONResponse)
async def extract_entities(file: UploadFile=File(...), file2: UploadFile=File(...)):
    """
    in file 1 upload  rain_demo.csv file in the folder structure of this repo
    in file 2 upload requirements.txt file
    """
    if file.filename.split(".")[-1] not in ["csv"]:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Only csv file allowed")
    file = await file.read()
    file = BytesIO(file)
    file2 = await file2.read()
    file2 = file2.decode('ascii')
    return caller_wrapper(file, file2)


if __name__=='__main__':
    uvicorn.run(app, host='127.0.0.1', port=5432)