import requests
import subprocess
import logging
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

sunoapi_base_url = os.getenv("SUNOAPI_BASE_URL", "http://localhost:3000")
proj_compose = os.getenv(
    "PROJ_COMPOSE", "/usr/local/dev/MuApi/MusicData/docker-compose.yml"
)

# Configure logging
logging.basicConfig(level=logging.INFO)


def custom_generate_audio(payload):
    url = f"{sunoapi_base_url}/api/custom_generate"
    response = requests.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    return response.json()


def extend_audio(payload):
    url = f"{sunoapi_base_url}/api/extend_audio"
    response = requests.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    return response.json()


def generate_audio_by_prompt(payload):
    url = f"{sunoapi_base_url}/api/generate"
    response = requests.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    return response.json()


def get_audio_information(audio_ids):
    url = f"{sunoapi_base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


def get_quota_information():
    url = f"{sunoapi_base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()


def start_suno_service():
    try:
        result = subprocess.run(
            [
                "docker-compose",
                "-f",
                proj_compose,
                "up",
                "-d",
                "sunoapi",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        logging.info("Start service output: %s", result.stdout)
        logging.error("Start service error: %s", result.stderr)
        return {"status": "started"}
    except subprocess.CalledProcessError as e:
        logging.error("Failed to start service: %s", e.stderr)
        return {"status": "error", "message": "Failed to start service"}


def stop_suno_service():
    try:
        # Check if the service is running
        ps_result = subprocess.run(
            [
                "docker-compose",
                "-f",
                proj_compose,
                "ps",
            ],
            capture_output=True,
            text=True,
        )
        logging.info("PS service output: %s", ps_result.stdout)
        logging.error("PS service error: %s", ps_result.stderr)

        if "sunoapi" not in ps_result.stdout:
            return {"status": "error", "message": "Suno API service is not running"}

        # Stop the specific service
        result = subprocess.run(
            [
                "docker-compose",
                "-f",
                proj_compose,
                "stop",
                "sunoapi",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        logging.info("Stop service output: %s", result.stdout)
        logging.error("Stop service error: %s", result.stderr)
        return {"status": "stopped"}
    except subprocess.CalledProcessError as e:
        logging.error("Failed to stop service: %s", e.stderr)
        return {"status": "error", "message": "Failed to stop service"}


if __name__ == "__main__":
    print(get_quota_information())
    stop_suno_service()
