import asyncio

import pytest
from fastapi import HTTPException

from api.rest_api import CodeRequest, execute_code


def test_api_stops_infinite_loops_and_returns_a_readable_error():
    response = asyncio.run(execute_code(CodeRequest(code="while(True) { }")))

    assert not response.success
    assert "Execution step limit exceeded" in response.error
    assert not hasattr(response, "traceback")


def test_api_limits_generated_output_before_printing():
    code = 'var mut text = "1234567890"\n' + "\n".join(
        "text = text + text" for _ in range(14)
    ) + "\nprint(text)"
    response = asyncio.run(execute_code(CodeRequest(code=code)))

    assert not response.success
    assert "String exceeds the 100,000-character limit" in response.error


def test_api_rejects_utf8_code_over_byte_limit():
    with pytest.raises(HTTPException) as error:
        asyncio.run(execute_code(CodeRequest(code='print("' + "é" * 50_001 + '")')))

    assert error.value.status_code == 413

