import json
import os

from fastapi import Header, HTTPException


async def verify_auth_token(x_hub_rdv_auth_token: str = Header()):
    if x_hub_rdv_auth_token not in json.loads(os.environ.get("AUTH_TOKENS")):
        raise HTTPException(
            status_code=401, detail="X-HUB-RDV-AUTH-TOKEN header invalid"
        )
