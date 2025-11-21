from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import uuid, os
from db import init_db, add_job, get_job, update_job_status
from worker_api import notify_kaggle_worker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.on_event("startup")
def startup():
    init_db()

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())
    video_path = f"{UPLOAD_FOLDER}/{job_id}_{file.filename}"

    with open(video_path, "wb") as f:
        f.write(await file.read())

    add_job(job_id, "queued", video_path)
    notify_kaggle_worker(job_id)

    return {"job_id": job_id, "status": "queued"}

@app.get("/status/{job_id}")
def check_status(job_id: str):
    return get_job(job_id)

@app.post("/update-job")
def worker_update(
    job_id: str = Form(...),
    status: str = Form(...),
    result_url: str = Form(None)
):
    update_job_status(job_id, status, result_url)
    return {"ok": True}
