from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from .services.music_service import (
    custom_generate_audio,
    extend_audio,
    generate_audio_by_prompt,
    get_audio_information,
    get_quota_information,
    start_suno_service,
    stop_suno_service,
)
import logging
import os

app = FastAPI()

# Set up CORS middleware
origins = [
    "http://localhost:3000",
    # "http://localhost:3001",
    "http://localhost:3002",  # React frontend in development
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.DEBUG)


class GeneratePayload(BaseModel):
    prompt: str


class AudioResponse(BaseModel):
    music_url: str


@app.post("/api/custom_generate", response_model=AudioResponse)
async def custom_generate(payload: GeneratePayload):
    logging.debug("Custom generate endpoint hit")
    result = custom_generate_audio(payload.dict())
    return result


@app.post("/api/extend_audio", response_model=AudioResponse)
async def extend_audio_route(payload: GeneratePayload):
    logging.debug("Extend audio endpoint hit")
    result = extend_audio(payload.dict())
    return result


@app.post("/api/generate", response_model=AudioResponse)
async def generate_audio(payload: GeneratePayload):
    logging.debug("Generate audio endpoint hit")
    result = generate_audio_by_prompt(payload.dict())
    return result


@app.get("/api/get", response_model=List[AudioResponse])
async def get_audio(audio_ids: str):
    logging.debug("Get audio endpoint hit")
    result = get_audio_information(audio_ids)
    return result


@app.get("/api/get_limit")
async def get_quota():
    logging.debug("Get quota endpoint hit")
    result = get_quota_information()
    return result


def get_service_name():
    node_env = os.getenv("NODE_ENV", "development")
    return "sunoapi" if node_env == "production" else "sunoapi_dev"


@app.post("/api/start_service")
async def start_service():
    logging.debug("Start service endpoint hit")
    service_name = get_service_name()
    logging.debug(f"Service name: {service_name}, calling start_suno_service")
    result = start_suno_service(service_name)
    logging.debug(f"Called start_suno_service, result: {result}")
    if result["returncode"] != 0:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@app.post("/api/stop_service")
async def stop_service():
    logging.info("Stop service endpoint hit, calling get_service_name()")
    service_name = get_service_name()
    logging.info(f"Service name: {service_name}, calling stop_suno_service")
    result = stop_suno_service(service_name)
    logging.info(f"Result from stop_suno_service: {result}")
    if result["returncode"] != 0:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
