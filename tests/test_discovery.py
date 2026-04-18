import time
import pytest
from utils.auth_helpers import get_discovery_document


class TestOIDCDiscovery:

    def test_discovery_endpoint_returns_200(self):
        """Discovery endpoint must be reachable and return 200"""
        response = get_discovery_document()
        assert response.status_code == 200

    def test_discovery_response_is_json(self):
        """Response must be valid JSON"""
        response = get_discovery_document()
        data = response.json()
        assert isinstance(data, dict)

    def test_discovery_contains_required_oidc_fields(self):
        """OIDC spec requires these fields to be present"""
        response = get_discovery_document()
        data = response.json()
        required_fields = [
            "issuer",
            "authorization_endpoint",
            "token_endpoint",
            "jwks_uri",
            "response_types_supported",
            "subject_types_supported",
            "id_token_signing_alg_values_supported"
        ]
        for field in required_fields:
            assert field in data, f"Missing required OIDC field: {field}"

    def test_issuer_matches_expected_tenant(self):
        """Issuer must reference the correct Entra ID tenant"""
        response = get_discovery_document()
        data = response.json()
        assert "login.microsoftonline.com" in data["issuer"]

    def test_token_endpoint_uses_https(self):
        """Token endpoint must use HTTPS — security requirement"""
        response = get_discovery_document()
        data = response.json()
        assert data["token_endpoint"].startswith("https://")

    def test_authorization_endpoint_uses_https(self):
        """Authorization endpoint must use HTTPS"""
        response = get_discovery_document()
        data = response.json()
        assert data["authorization_endpoint"].startswith("https://")

    def test_jwks_uri_uses_https(self):
        """JWKS URI must use HTTPS to protect signing keys"""
        response = get_discovery_document()
        data = response.json()
        assert data["jwks_uri"].startswith("https://")

    def test_supported_response_types_includes_code(self):
        """Authorization code flow must be supported"""
        response = get_discovery_document()
        data = response.json()
        assert "code" in data["response_types_supported"]

    def test_id_token_signing_uses_rs256(self):
        """Entra ID must sign ID tokens with RS256"""
        response = get_discovery_document()
        data = response.json()
        assert "RS256" in data["id_token_signing_alg_values_supported"]

    def test_discovery_response_time_under_3_seconds(self):
        """Discovery endpoint must respond within 3 seconds"""
        start = time.time()
        get_discovery_document()
        elapsed = time.time() - start
        assert elapsed < 3.0