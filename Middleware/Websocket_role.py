from fastapi import WebSocket, HTTPException
from Tokens.GenerateTokens import (verify_secure_token,generate_secure_token)

def websocket_current_user(allowed_roles: list):

    async def user_dependency(ws: WebSocket):

        access_token = ws.cookies.get("access_token")

        refresh_token = ws.cookies.get("refresh_token")

        payload = None


        if access_token:

            try:

                payload = verify_secure_token(access_token)

            except Exception as err:

                print(payload, "token in try")

                error_message = str(err)

               
                if error_message == "Token has expired":

                    print("Access token expired")

                else:

                    await ws.close(code=1008)

                    raise HTTPException(status_code=401,detail="Invalid access token")


        if payload is None:

            if not refresh_token:

                await ws.close(code=1008)

                raise HTTPException(status_code=401,detail="Please login again")

            try:

                refresh_payload = verify_secure_token(refresh_token)

                print(refresh_payload,"refresh data in allowed role")

                payload = refresh_payload

            except Exception:

                await ws.close(code=1008)

                raise HTTPException(status_code=401,detail="Session expired")

        email = payload.get("email")

        user_id = payload.get("id")

        user_role = payload.get("role")

        print(email, user_id, user_role, "data in allowedrole")

        if email is None or user_id is None:

            await ws.close(code=1008)

            raise HTTPException(status_code=401,detail="Authentication failed")


        if (allowed_roles and user_role not in allowed_roles):

            await ws.close(code=1008)

            raise HTTPException( status_code=403, detail="Permission denied")

        return {
            "email": email,
            "id": user_id,
            "role": user_role
        }

    return user_dependency