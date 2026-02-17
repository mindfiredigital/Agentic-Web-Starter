import importlib

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.config import env_config
from app.utils.iam_utils import auth_deps, jwt_utils


def test_missing_credentials_raises(clear_env, set_env_vars):
    """Verify HTTP 401 when no credentials are provided."""
    importlib.reload(env_config)
    importlib.reload(jwt_utils)
    importlib.reload(auth_deps)

    with pytest.raises(HTTPException, match="Not authenticated"):
        auth_deps.get_current_user_payload(credentials=None)


def test_invalid_token_raises(clear_env, set_env_vars):
    """Verify HTTP 401 when token is invalid."""
    importlib.reload(env_config)
    importlib.reload(jwt_utils)
    importlib.reload(auth_deps)

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="invalid-token",
    )
    with pytest.raises(HTTPException, match="Invalid token"):
        auth_deps.get_current_user_payload(credentials=credentials)


def test_valid_token_returns_payload(clear_env, set_env_vars):
    """Verify valid token returns correct TokenPayload with sub and role_ids."""
    importlib.reload(env_config)
    importlib.reload(jwt_utils)
    importlib.reload(auth_deps)

    token = jwt_utils.JWT_utils.create_access_token("user-1", ["role-1"], expires_minutes=5)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    payload = auth_deps.get_current_user_payload(credentials=credentials)

    assert payload.sub == "user-1"
    assert payload.role_ids == ["role-1"]
