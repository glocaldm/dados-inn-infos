import functions_framework
import google.auth.transport.requests
import google.oauth2.id_token
import requests
from flask import make_response, jsonify
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
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized: Missing Bearer token'}), 401
    id_token = auth_header.split(' ')[1]
    try:
        # Validate the ID Token
        request_adapter = google.auth.transport.requests.Request()
        claims = google.oauth2.id_token.verify_firebase_token(id_token, request_adapter)

        if not claims:
            return jsonify({'error': 'Unauthorized: Invalid token'}), 401
        return jsonify({
            'message': 'Hello, secure world!',
            'user': claims.get('email'),
            'uid': claims.get('user_id')
        })
    except Exception as e:
        print(e)
        return jsonify({'error': 'Unauthorized: Token verification failed'}), 401
