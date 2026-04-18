import time
import pytest
from utils.auth_helpers import get_access_token, get_token_with_bad_secret


class TestTokenEndpoint:

    def test_valid_credentials_return_access_token(self):
        """Valid client credentials must return an access token"""
        result = get_access_token()
        assert "access_token" in result, \
            f"No access token returned. Error: {result.get('error_description')}"

    def test_token_response_contains_token_type(self):
        """Token response must contain token_type field"""
        result = get_access_token()
        assert "token_type" in result

    def test_token_type_is_bearer(self):
        """Token type must be Bearer — OAuth 2.0 standard"""
        result = get_access_token()
        assert result["token_type"].lower() == "bearer"

    def test_token_response_contains_expires_in(self):
        """Token response must contain expiry information"""
        result = get_access_token()
        assert "expires_in" in result

    def test_token_expiry_is_positive_integer(self):
        """Token expiry must be a positive number"""
        result = get_access_token()
        assert isinstance(result["expires_in"], int)
        assert result["expires_in"] > 0

    def test_access_token_is_non_empty_string(self):
        """Access token must be a non-empty string"""
        result = get_access_token()
        assert isinstance(result["access_token"], str)
        assert len(result["access_token"]) > 0

    def test_access_token_is_jwt_format(self):
        """Access token must be in JWT format — three dot-separated parts"""
        result = get_access_token()
        token = result["access_token"]
        parts = token.split(".")
        assert len(parts) == 3, "Token is not in valid JWT format"

    def test_no_error_in_valid_token_response(self):
        """Valid credentials must not return an error field"""
        result = get_access_token()
        assert "error" not in result

    def test_invalid_secret_returns_error(self):
        """Invalid credentials must be rejected"""
        result = get_token_with_bad_secret()
        assert "error" in result

    def test_invalid_secret_does_not_return_token(self):
        """Invalid credentials must never return an access token"""
        result = get_token_with_bad_secret()
        assert "access_token" not in result

    def test_invalid_secret_returns_invalid_client_error(self):
        """Error code must indicate authentication failure"""
        result = get_token_with_bad_secret()
        assert result.get("error") == "invalid_client"

    def test_token_acquisition_under_3_seconds(self):
        """Token endpoint must respond within 3 seconds"""
        start = time.time()
        get_access_token()
        elapsed = time.time() - start
        assert elapsed < 3.0