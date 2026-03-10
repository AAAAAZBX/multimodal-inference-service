import os
from typing import Literal

ServiceMode = Literal["vlm", "t2i"]

def get_service_mode() -> ServiceMode:
    mode = os.getenv("SERVICE_MODE", "vlm").lower()
    if mode not in {"vlm", "t2i"}:
        raise ValueError(
            "Invalid SERVICE_MODE. Expected 'vlm' or 't2i'."
        )
    return mode
