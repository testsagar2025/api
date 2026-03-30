
from fastapi import FastAPI
from .crypto import encrypt_payload

app = FastAPI(title="DeltaStudy Mirror API")

@app.get("/")
def read_root():
    return {"status": "online", "message": "AES-256-GCM Encrypted Endpoint"}

@app.get("/api/pw/batches")
async def get_batches():
    mock_data = {
        "success": True, 
        "data": [
            {"id": "101", "name": "Physics Wallah Batch"},
            {"id": "102", "name": "Delta Study Batch"}
        ]
    }
    return {"data": encrypt_payload(mock_data)}

@app.get("/api/pw/subjects/{batch_id}")
async def get_subjects(batch_id: str):
    mock_data = {
        "success": True,
        "batch_id": batch_id,
        "subjects": [{"id": "s1", "name": "Organic Chemistry"}]
    }
    return {"data": encrypt_payload(mock_data)}