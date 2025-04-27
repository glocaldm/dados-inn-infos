import functions_framework
import requests
from flask import make_response
from google.cloud import secretmanager

# Set variables
ALLOWED_ORIGIN = "https://glocaldm.github.io"
external_url = "https://ical.booking.com/v1/export?t=219b9892-bf77-4998-b804-30590502eaf6"
project_id = 'autogpt-searcher-1682924050005'  # Fill in your project
secret_id = 'DEEP_SEEK_API_KEY'
version_id = 'latest'
# Create Secret Version Reference
name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"


@functions_framework.http
def fetch_and_store_data(request):
    origin = request.headers.get('Origin', '')
    cors_headers = {
        'Access-Control-Allow-Origin': ALLOWED_ORIGIN if origin == ALLOWED_ORIGIN else '',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'Vary': 'Origin'
    }

    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return ('', 204, cors_headers)

    # Handle GET or POST request
    if request.method in ['POST']:
        request_json = request.json()

        client = secretmanager.SecretManagerServiceClient()
        response = client.access_secret_version(request={"name": name})

        API_KEY = response.payload.data.decode("UTF-8")

        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

        data = {
            "model": "deepseek-reasoner",  # Use 'deepseek-reasoner' for R1 model or 'deepseek-chat' for V3 model
            "messages": [
                {"role": "system", "content": "You are a professional assistant"},
                {"role": "user", "content": "Who are you?"}
            ],
            "stream": False  # Disable streaming
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            make_response(response.json()['choices'])
            response.headers['Content-Type'] = 'application/json'
        else:
            print("Request failed, error code:", response.status_code)

    return make_response(("Method Not Allowed", 405, cors_headers))
