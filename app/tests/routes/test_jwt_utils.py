import importlib

import pytest

from app.config import env_config
from app.utils.iam_utils.auth import jwt_utils


def test_create_and_decode_token(clear_env, set_env_vars):
    importlib.reload(env_config)
    importlib.reload(jwt_utils)

    token = jwt_utils.JWT_utils.create_access_token("user-123", ["role-1"], expires_minutes=5)
    payload = jwt_utils.JWT_utils.decode_access_token(token)

    assert payload["sub"] == "user-123"
    assert payload["role_ids"] == ["role-1"]


def test_expired_token_raises(clear_env, set_env_vars):
    importlib.reload(env_config)
    importlib.reload(jwt_utils)

    token = jwt_utils.JWT_utils.create_access_token("user-123", ["role-1"], expires_minutes=-1)
    with pytest.raises(jwt_utils.JWTError, match="Token expired"):
        jwt_utils.JWT_utils.decode_access_token(token)
