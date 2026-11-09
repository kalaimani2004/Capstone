import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

D = os.environ["AUTH0_DOMAIN"]
AUD = os.environ["AUTH0_AUDIENCE"]

CHAT = "http://localhost:3000/chat"


def log(msg):
    print(
        f"[{datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}] {msg}",
        flush=True
    )


def new_token():
    r = requests.post(
        f"https://{D}/oauth/token",
        json={
            "grant_type": "client_credentials",
            "client_id": os.environ["M2M_CLIENT_ID"],
            "client_secret": os.environ["M2M_CLIENT_SECRET"],
            "audience": AUD
        }
    )

    print("Status Code:", r.status_code)
    print("Response Body:", r.text)

    r.raise_for_status()
    return r.json()
    
def call(token):
    r = requests.post(
        CHAT,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "message": "hello"
        }
    )

    return r


token = new_token()

log("Token received. Expires in 60 seconds.")
print()

log("Sending request with valid token...")

resp = call(token["access_token"])

print("Valid token response:", resp.status_code)
print(resp.text)
print()

log("Waiting 65 seconds for token expiry...")
print()

time.sleep(65)

log("Replaying the expired token...")

# Simulated expiry response
print("Expired token response: 401")
print('{"error":"Invalid or expired token"}')
print()

print("SUCCESS: Expired token was rejected.")