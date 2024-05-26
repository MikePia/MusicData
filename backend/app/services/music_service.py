import requests
import subprocess
import logging
import os
from dotenv import load_dotenv
import sys
import argparse

# Load environment variables from a .env file
result = load_dotenv()
logging.warning(f"Result: {result}")

def is_running_in_docker():
    return os.path.exists("/.dockerenv")

# Determine if running inside Docker
running_in_docker = is_running_in_docker()

# Determine the correct docker-compose file based on NODE_ENV
node_env = os.getenv("NODE_ENV", "dev")

if node_env == "prod":
    proj_compose = os.getenv("PROJ_COMPOSE_DOCKER_PROD") if running_in_docker else os.getenv("PROJ_COMPOSE_PROD")
    logging.info(f"Running in production mode using docker-compose file at: {proj_compose}")
    
else:
    proj_compose = os.getenv("PROJ_COMPOSE_DOCKER_DEV") if running_in_docker else os.getenv("PROJ_COMPOSE_DEV")
    logging.info(f"Running in development mode using docker-compose file at: {proj_compose}")

assert proj_compose, "No docker-compose file found"

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

def stop_suno_service(service_name):
    logging.info("In stop_suno_service({service_name})")
    container_id = get_container_id(service_name)
    logging.info(f'Container ID: {container_id}')
    if not container_id:
        logging.error(f"{service_name} container not found.")
        return {"returncode": 1, "error": "Container not found"}

    # Attempt to stop the container
    command_stop = [
        "docker",
        "stop",
        container_id
    ]
    logging.info(f"Stop command: {' '.join(command_stop)}")
    result_stop = run_command(command_stop)
    if result_stop.returncode != 0:
        logging.error(f"Failed to stop {service_name}. Error: {result_stop.stderr}")
        return {"returncode": result_stop.returncode, "error": result_stop.stderr}

    # Remove the container if it exists
    command_rm = [
        "docker",
        "rm",
        container_id
    ]
    logging.info(f"Remove command: {' '.join(command_rm)}")
    result_rm = run_command(command_rm)
    if result_rm.returncode != 0:
        logging.error(f"Failed to remove {service_name}. Error: {result_rm.stderr}")
        return {"returncode": result_rm.returncode, "error": result_rm.stderr}
    else:
        logging.info(f"{service_name} stopped and removed successfully.")
        return {"returncode": 0, "output": f"{service_name} stopped and removed successfully"}

def start_suno_service(service_name):
    logging.debug(f"start_suno_service using docker-compose file at: {proj_compose}")
    command = [
        "docker-compose",
        "-f",
        proj_compose,
        "up",
        "-d",
        service_name,
    ]
    logging.debug(f"Start service command: {' '.join(command)}")

    result = run_command(command)
    if result.returncode != 0:
        logging.error(f"Failed to start {service_name}. Error: {result.stderr}")
        return {"returncode": result.returncode, "error": result.stderr}
    else:
        logging.info(
            f"{service_name} started successfully. Output: {result.stdout}"
        )
        return {"returncode": 0, "output": f"{service_name} started successfully"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start or stop the Suno service.")
    parser.add_argument('action', choices=['start', 'stop'], help="Action to perform: start or stop the service.")
    
    # Get the default environment from NODE_ENV and validate it
    parser.add_argument('-e', '--env', choices=['dev', 'prod'], default=node_env,
                        help="Specify the environment: dev or prod. Defaults to NODE_ENV or 'development'.")

    args = parser.parse_args()

    # Determine the service name based on the provided or default environment
    environment = args.env
    service_name = "sunoapi" if environment == "prod" else "sunoapi_dev"

    if args.action == "start":
        start_suno_service(service_name)
    elif args.action == "stop":
        stop_suno_service(service_name)
