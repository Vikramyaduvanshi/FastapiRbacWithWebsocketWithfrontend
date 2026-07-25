from datetime import datetime, timedelta, timezone
import json
import jwt
from cryptography.fernet import Fernet


JWT_SECRET = "c21efdc8881f7f9cc2b9cb6c833d1fa83143586742b8c467be07866c8df48080"
AES_SECRET = "TM5P-ztVxqQ6XFU9UgrUBY9ltM8Cf5pVskEyKjsMVlE="

fernet = Fernet(AES_SECRET.encode())


def generate_secure_token(user, time_value: int, isrefresh: bool = False) -> str:
  
    original_payload = {
        "id": str(user.id) if hasattr(user, "id") else str(user.get("_id")),
        "email": user.email if hasattr(user, "email") else user.get("email"),
        "role": user.role if hasattr(user, "role") else user.get("role"),
    }


    json_string = json.dumps(original_payload)
    encrypted_payload = fernet.encrypt(json_string.encode("utf-8")).decode("utf-8")


    if isrefresh:
        expire_time = datetime.now(timezone.utc) + timedelta(days=time_value)
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=time_value)    

    jwt_payload = {
        "data": encrypted_payload,
        "exp": expire_time
    }

    token = jwt.encode(jwt_payload, JWT_SECRET, algorithm="HS256")
    return token


def verify_secure_token(token: str) -> dict:
    try:
    
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        encrypted_data = decoded.get("data")

        decrypted_bytes = fernet.decrypt(encrypted_data.encode("utf-8"))
        original_data = json.loads(decrypted_bytes.decode("utf-8"))

        return original_data

    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except Exception:
        raise Exception("Invalid Token or Decryption Failed")

