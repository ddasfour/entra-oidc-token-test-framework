# Entra ID OIDC Token Test Framework

Automated pytest framework for validating Microsoft Entra ID
OIDC authentication endpoints using a live app registration.

## What it tests

- OIDC discovery endpoint structure and required fields
- Token acquisition using client credentials flow (MSAL)
- Token response validation — structure, type, and expiry
- Error handling for invalid client credentials
- Redirect URI validation — registered vs unregistered URIs
- Response time thresholds across all endpoints

## Key finding

Entra ID uses deferred redirect URI validation — it presents
the sign-in page first and only rejects an unregistered
redirect URI after authentication. This is important behaviour
to understand when building SSO integrations at scale.

## Project structure

tests/test_discovery.py        — OIDC discovery endpoint tests
tests/test_token_endpoint.py   — Token acquisition and validation
tests/test_redirect_uri.py     — Redirect URI behaviour tests
utils/auth_helpers.py          — Reusable MSAL helper functions

## Setup

```bash
git clone https://github.com/ddasfour/entra-oidc-token-test-framework.git
cd entra-oidc-token-test-framework
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and add your Entra ID credentials:

Never commit your `.env` file. It is protected by `.gitignore`.

## Run all tests

```bash
pytest
```

## Prerequisites

- Microsoft Entra ID app registration with client credentials
- Redirect URI `https://jwt.ms` registered on the app
- ID tokens and Access tokens enabled under Authentication
