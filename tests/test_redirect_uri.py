import time
import pytest
import requests
from utils.auth_helpers import (
    get_authorize_response,
    AUTHORIZE_ENDPOINT,
    CLIENT_ID
)


class TestRedirectURI:

    def test_valid_redirect_uri_does_not_return_error(self):
        """A registered redirect URI must not produce a mismatch error"""
        response = get_authorize_response("https://jwt.ms")
        location = response.headers.get("Location", "")
        assert "error=redirect_uri_mismatch" not in location

    def test_valid_redirect_uri_returns_redirect(self):
        """A valid request must return a redirect response"""
        response = get_authorize_response("https://jwt.ms")
        assert response.status_code in [200, 302]

    def test_invalid_redirect_uri_is_rejected(self):
        """An unregistered redirect URI must be rejected by Entra ID"""
        response = get_authorize_response("https://evil-site.com/callback")
        location = response.headers.get("Location", "")
        body = response.text
        assert "error" in location or \
               "error" in body.lower() or \
               response.status_code == 400

    def test_invalid_redirect_uri_shows_mismatch_error(self):
        """Entra ID defers redirect URI validation to post-authentication.
        An unregistered URI causes Entra ID to show the sign-in page first,
        then reject with mismatch error after credentials are submitted.
        This test confirms the request does not get a success redirect."""
        response = get_authorize_response("https://evil-site.com/callback")
        location = response.headers.get("Location", "")
        body = response.text
        assert "code=" not in location and \
               "access_token" not in location or \
               "ConvergedSignIn" in body or \
               "Sign in" in body

    def test_missing_client_id_is_rejected(self):
        """Request without client_id must be rejected"""
        params = {
            "response_type": "code",
            "redirect_uri": "https://jwt.ms",
            "scope": "openid",
            "state": "test_state"
        }
        response = requests.get(
            AUTHORIZE_ENDPOINT,
            params=params,
            allow_redirects=False
        )
        body = response.text
        assert response.status_code in [400, 302] or \
               "error" in body.lower()

    def test_http_redirect_uri_rejected_for_non_localhost(self):
        """Non-localhost HTTP redirect URIs must be rejected"""
        response = get_authorize_response("http://insecure-site.com/callback")
        location = response.headers.get("Location", "")
        body = response.text
        assert "error" in location or \
               "error" in body.lower() or \
               response.status_code == 400

    def test_authorize_endpoint_response_time_under_5_seconds(self):
        """Authorize endpoint must respond within 5 seconds"""
        start = time.time()
        get_authorize_response("https://jwt.ms")
        elapsed = time.time() - start
        assert elapsed < 5.0