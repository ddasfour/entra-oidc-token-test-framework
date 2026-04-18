import os
import time
import requests
from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
DISCOVERY_URL = f"{AUTHORITY}/v2.0/.well-known/openid-configuration"
AUTHORIZE_ENDPOINT = f"{AUTHORITY}/oauth2/v2.0/authorize"
TOKEN_ENDPOINT = f"{AUTHORITY}/oauth2/v2.0/token"


def get_discovery_document():
    """Fetch the OIDC discovery document from Entra ID"""
    response = requests.get(DISCOVERY_URL)
    return response


def get_access_token():
    """Acquire an access token using client credentials flow"""
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    return result


def get_token_with_bad_secret():
    """Attempt token acquisition with an invalid client secret"""
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential="invalid_secret_intentionally_wrong"
    )
    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )
    return result


def get_authorize_response(redirect_uri, extra_params=None):
    """Call the authorize endpoint with given redirect URI"""
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid",
        "response_mode": "query",
        "state": "test_state_123"
    }
    if extra_params:
        params.update(extra_params)
    response = requests.get(
        AUTHORIZE_ENDPOINT,
        params=params,
        allow_redirects=False
    )
    return response