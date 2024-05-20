import requests
import subprocess

base_url = "http://localhost:3000"
suno_docker = "/usr/local/dev/MuApi/sunoapi/suno-api/docker-compose.yml"


def custom_generate_audio(payload):
    url = f"{base_url}/api/custom_generate"
    response = requests.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    return response.json()


def extend_audio(payload):
    url = f"{base_url}/api/extend_audio"
    response = requests.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    return response.json()


def generate_audio_by_prompt(payload):
    url = f"{base_url}/api/generate"
    response = requests.post(
        url, json=payload, headers={"Content-Type": "application/json"}
    )
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = requests.get(url)
    return response.json()


def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = requests.get(url)
    return response.json()


def start_suno_service():
    subprocess.run(["docker-compose", "-f", "sunoapi/docker-compose.yml", "up", "-d"])

def stop_suno_service():
    subprocess.run(["docker-compose", "-f", "sunoapi/docker-compose.yml", "down"])


if __name__ == "__main__":
    print(get_quota_information())