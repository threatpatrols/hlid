import time
import uuid

import pytest

from hlid import HLID


def test_01():
    secret = uuid.uuid4().hex
    value1 = HLID(secret=secret)
    time.sleep(0.01)
    value2 = HLID(secret=secret)
    assert value1.hex != value2.hex


def test_02():
    user_data = "AA"
    with pytest.raises(ValueError) as e_info:
        _ = HLID(user_data=user_data)
    assert "must be 2x lowercase hex chars only" in str(e_info.value)


def test_02b():
    user_data = "xx"
    with pytest.raises(ValueError) as e_info:
        _ = HLID(user_data=user_data)
    assert "must be hex chars only" in str(e_info.value)


def test_03():
    secret = uuid.uuid4().hex[0:8]  # too short
    with pytest.raises(ValueError) as e_info:
        _ = HLID(secret=secret)
    assert "HLID secret too short" in str(e_info.value)


def test_04():
    secret = uuid.uuid4().hex
    value = HLID(secret=secret)
    with pytest.raises(ValueError) as e_info:
        _ = HLID(value.hex, secret=uuid.uuid4().hex)
    assert "HLID fails HMAC check" in str(e_info.value)


def test_05():
    value = uuid.uuid4().hex
    with pytest.raises(ValueError) as e_info:
        _ = HLID(value)
    assert "HLID invalid value" in str(e_info.value)


def test_06():
    value = uuid.uuid4().hex + "-" + uuid.uuid4().hex
    with pytest.raises(ValueError) as e_info:
        _ = HLID(value)
    assert "HLID invalid value" in str(e_info.value)


def test_07():
    value = str(HLID()).upper()
    with pytest.raises(ValueError) as e_info:
        _ = HLID(value)
    assert "lowercase hex chars only" in str(e_info.value)
