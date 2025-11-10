"""
Core utilities
"""
from typing import Any, Dict
import orjson


def json_response(data: Any) -> bytes:
    """Fast JSON response using orjson"""
    return orjson.dumps(data)


def validate_input(data: Dict, required_fields: list) -> tuple[bool, str]:
    """Validate input data"""
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, ""
