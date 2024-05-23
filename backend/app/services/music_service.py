import requests
import subprocess
import logging
import os
from dotenv import load_dotenv
import sys

# Load environment variables from a .env file
load_dotenv()

def is_running_in_docker():
    path = "/.dockerenv"
    return os.path.exists(path)

running_in_docker = is_running_in_docker()

if running_in_docker:
    print("Running inside Docker")
    proj_compose = os.getenv(
        "PROJ_COMPOSE", "/usr/src/app/docker-compose.yml"
    )
else:
    print("Running outside Docker")
    proj_compose = os.getenv(
        "PROJ_COMPOSE", "/usr/local/dev/MuApi/MusicData/docker-compose.yml"
    )

logging.basicConfig(level=logging.DEBUG)
logging.debug(f"Using docker-compose file at: {proj_compose}")

sunoapi_base_url = os.getenv("SUNOAPI_BASE_URL", "http://localhost:3000")

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

def run_command(command):
    logging.debug(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    logging.debug(f"Command output: {result.stdout}")
    logging.debug(f"Command error: {result.stderr}")
    logging.debug(f"Command return code: {result.returncode}")
    return result

def get_container_id(service_name):
    command = [
        "docker",
        "ps",
        "-a",
        "--filter", f"name={service_name}",
        "--format", "{{.ID}}"
    ]
    result = run_command(command)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        logging.error(f"Failed to get container ID for {service_name}. Error: {result.stderr}")
        return None

def stop_suno_service():
    container_id = get_container_id("musicdata_sunoapi")
    if not container_id:
        logging.error("Suno API service container not found.")
        return {"returncode": 1, "error": "Container not found"}

    # Attempt to stop the container
    command_stop = [
        "docker",
        "stop",
        container_id
    ]
    result_stop = run_command(command_stop)
    if result_stop.returncode != 0:
        logging.error(f"Failed to stop Suno API service. Error: {result_stop.stderr}")
        return {"returncode": result_stop.returncode, "error": result_stop.stderr}

    # Remove the container if it exists
    command_rm = [
        "docker",
        "rm",
        container_id
    ]
    result_rm = run_command(command_rm)
    if result_rm.returncode != 0:
        logging.error(f"Failed to remove Suno API service. Error: {result_rm.stderr}")
        return {"returncode": result_rm.returncode, "error": result_rm.stderr}
    else:
        logging.info("Suno API service stopped and removed successfully.")
        return {"returncode": 0, "output": "Suno API service stopped and removed successfully"}

def start_suno_service():
    logging.debug(f"start_suno_service using docker-compose file at: {proj_compose}")
    command = [
        "docker-compose",
        "-f",
        proj_compose,
        "up",
        "-d",
        "sunoapi",
    ]
    logging.debug(f"Start service command: {' '.join(command)}")

    result = run_command(command)
    if result.returncode != 0:
        logging.error(f"Failed to start Suno API service. Error: {result.stderr}")
        return {"returncode": result.returncode, "error": result.stderr}
    else:
        logging.info(
            f"Suno API service started successfully. Output: {result.stdout}"
        )
        return {"returncode": 0, "output": "Suno API service started successfully"}


if __name__ == "__main__":
    # Add commandline arg to run start or stop
    if len(sys.argv) < 2:
        print("Usage: python music_service.py start|stop")
        sys.exit(1)
    elif sys.argv[1] == "start":
        start_suno_service()
    elif sys.argv[1] == "stop":
        stop_suno_service()
