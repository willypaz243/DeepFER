from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.env import ENV


class SecurityService:
    def verify_password(self, plain_password: str, hash_password: str):
        plain_pass_bytes = plain_password.encode("utf-8")
        hash_pass_bytes = hash_password.encode("utf-8")
        return bcrypt.checkpw(plain_pass_bytes, hash_pass_bytes)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, ENV.SECRET_KEY, algorithm=ENV.ALGORITHM)  # type: ignore
        return encoded_jwt

    def decode_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, ENV.SECRET_KEY, algorithms=[ENV.ALGORITHM])  # type: ignore
            user_ci = int(payload.get("sub"))
            if not user_ci:
                raise ValueError("Token is missing 'user_ci' claim.")
            return user_ci
        except jwt.PyJWTError:
            raise ValueError("Invalid token")
