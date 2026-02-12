from app.utils.iam_utils.auth import auth_utils

def test_hash_and_verify_password():
    """Verify hash_password produces verifiable hash and wrong password fails."""
    password = "s3cret-pass"
    hashed = auth_utils.hash_password(password)

    assert hashed != password
    assert auth_utils.verify_password(password, hashed) is True
    assert auth_utils.verify_password("wrong-pass", hashed) is False
