from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from .services.music_service import custom_generate_audio, extend_audio, generate_audio_by_prompt, get_audio_information, get_quota_information, start_suno_service, stop_suno_service

app = FastAPI()

class GeneratePayload(BaseModel):
    prompt: str

class AudioResponse(BaseModel):
    music_url: str

@app.post("/api/custom_generate", response_model=AudioResponse)
async def custom_generate(payload: GeneratePayload):
    result = custom_generate_audio(payload.dict())
    return result

@app.post("/api/extend_audio", response_model=AudioResponse)
async def extend_audio_route(payload: GeneratePayload):
    result = extend_audio(payload.dict())
    return result

@app.post("/api/generate", response_model=AudioResponse)
async def generate_audio(payload: GeneratePayload):
    result = generate_audio_by_prompt(payload.dict())
    return result

@app.get("/api/get", response_model=List[AudioResponse])
async def get_audio(audio_ids: str):
    result = get_audio_information(audio_ids)
    return result

@app.get("/api/get_limit")
async def get_quota():
    result = get_quota_information()
    return result

@app.post("/api/start_service")
async def start_service():
    result = start_suno_service()
    if result['status'] == 'error':
        raise HTTPException(status_code=500, detail=result['message'])
    return result

@app.post("/api/stop_service")
async def stop_service():
    result = stop_suno_service()
    if result['status'] == 'error':
        raise HTTPException(status_code=500, detail=result['message'])
    return result
