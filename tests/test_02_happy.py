import uuid

from hlid import HLID, hlid


def test_01():
    value = HLID()
    assert value.age < 1
    assert value.age > 0
    assert len(str(value).split("-")) == 5
    assert str(value).replace("-", "") == value.hex
    assert value.time > 0
    assert value.time < 9999999999


def test_01b():
    value = HLID(secret=uuid.uuid4().hex)
    assert value.age < 1
    assert value.age > 0
    assert len(str(value).split("-")) == 5
    assert str(value).replace("-", "") == value.hex
    assert value.time > 0


def test_02():
    value = HLID()
    result = HLID(value.hex)
    assert str(value) == str(result)


def test_03():
    assert HLID() != HLID()
    assert HLID().hex != HLID().hex


def test_04():
    secret = uuid.uuid4().hex
    value = HLID(secret=secret)
    result = HLID(value.hex, secret=secret)
    assert value.hex == result.hex


def test_05():
    user_data = "aa"
    value = HLID(user_data=user_data)
    result = HLID(value.hex)
    assert str(value) == str(result)


def test_06():
    user_data = "aa"
    secret = uuid.uuid4().hex
    value = HLID(secret=secret, user_data=user_data)
    result = HLID(str(value), secret=secret)
    assert value.hex == result.hex


def test_07():
    secret = uuid.uuid4().hex
    value = hlid(secret)
    assert value.hex == HLID(value.hex, secret=secret).hex
