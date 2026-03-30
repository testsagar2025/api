from fastapi import FastAPI, Request, Query
from Crypto.Cipher import AES
import json
import secrets
from typing import Optional

app = FastAPI()

# Configuration
KEY = b"maggikhalo".ljust(32, b'\0')

def encrypt_payload(data: dict) -> dict:
    """Helper to encrypt dictionary into the DeltaStudy hex format."""
    json_bytes = json.dumps(data).encode('utf-8')
    nonce = secrets.token_bytes(12)
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(json_bytes)
    # Format: IV:Ciphertext+Tag
    encrypted_hex = f"{nonce.hex()}:{(ciphertext + tag).hex()}"
    return {"data": encrypted_hex}

@app.get("/")
def health_check():
    return {"status": "online", "version": "1.0.0"}

# 1. GET BATCHES
@app.get("/api/pw/batches")
def get_batches():
    payload = {
        "success": True,
        "data": [
            {
                "batchId": "65df241600f257001881fbbd",
                "batchName": "Physics Wallah Alpha",
                "batchImage": "https://static.pw.live/5eb393ee95fab7468a79d189/64634676-963b-4895-950c-e160e1694f4c.png"
            }
        ]
    }
    return encrypt_payload(payload)

# 2. POST BATCH DETAILS (Required for Subjects)
@app.post("/api/pw/batchdetails")
async def get_batch_details(request: Request):
    # Your client sends {"searchParams": {"BatchId": "..."}}
    body = await request.json()
    batch_id = body.get("searchParams", {}).get("BatchId", "unknown")
    
    payload = {
        "success": True,
        "data": {
            "batchId": batch_id,
            "subjects": [
                {"id": "physics-593096", "subjectName": "Physics", "subjectImage": ""},
                {"id": "chemistry-102938", "subjectName": "Chemistry", "subjectImage": ""}
            ]
        }
    }
    return encrypt_payload(payload)

# 3. GET TOPICS
@app.get("/api/pw/topics")
def get_topics(BatchId: str, SubjectId: str):
    payload = {
        "success": True,
        "data": [
            {"id": "topic-1", "name": "Electrostatics", "slug": "electricity-872753"},
            {"id": "topic-2", "name": "Current Electricity", "slug": "current-12345"}
        ]
    }
    return encrypt_payload(payload)

# 4. GET VIDEOS
@app.get("/api/pw/datacontent")
def get_videos(batchId: str, subjectSlug: str, topicSlug: str, contentType: str = "videos"):
    payload = {
        "success": True,
        "data": [
            {
                "id": "vid-001",
                "name": "Lecture 01: Introduction",
                "childId": "6871f4dc7e1cab1b3bfddb7d",
                "url": "https://example.com/stream.mpd"
            }
        ]
    }
    return encrypt_payload(payload)
