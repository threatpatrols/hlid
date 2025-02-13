import hashlib
import hmac
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

__version__ = "0.1.3"


class HLID:
    """
    A human-readable twist on ULID/UUID values; A unique human-time-lexicographically sortable
    identifier using the same form as a UUID4 which makes it possible to use with existing UUID4
    systems such as database storage and validators.

        20241105-1108-5200-00ff-8fa646f09a7e
        ^        ^    ^ ^  ^ ^  ^
        |        |    | |  | |  |- 12x hex: nonce-value -or- hmac-value
        |        |    | |  | |- 2x hex: one byte of user-data; 2x hex chars
        |        |    | |+ |- 4x digits: -10^4 seconds; tenth of millisecond
        |        |    |- 2x digits: seconds
        |        |- 4x digits: hours and minutes
        |- 8x digits: year and month and day

    HLID example value:     20241105-0153-0041-0874-67961ce919d7
    UUID4 comparison value: 1c21583a-9b17-11ef-99e9-d34117a8d86d

    :return: str
    """

    _value: str
    _is_signed: bool = False

    def __init__(self, value: Optional[str] = None, secret: Optional[str] = None, user_data: str = "00") -> None:
        if not user_data or len(user_data) != 2 or user_data != user_data.lower():
            raise ValueError("HLID user-data invalid, must be 2x lowercase hex chars only.")

        try:
            _ = int(user_data, 16)  # test to make sure user-data is hex
        except:
            raise ValueError("HLID user-data invalid, must be hex chars only.")

        if value:
            if value != value.lower():
                raise ValueError("HLID invalid, be lowercase hex chars only.")
            if len(value) == 32:
                value = f"{value[0:8]}-{value[8:12]}-{value[12:16]}-{value[16:20]}-{value[20:32]}"  # transmorph
            self._value = value
        else:
            ts = datetime.now(timezone.utc)
            ts_subseconds = ts.strftime("%f")[0:4]
            hlid_ts = f"{ts.strftime(f'%Y%m%d-%H%M-%S')}{ts_subseconds[:2]}-{ts_subseconds[2:]}{user_data}"
            hlid_ts_suffix = self.__trunc_sha256_hmac_else_nonce(value=hlid_ts, secret=secret)
            self._value = f"{hlid_ts}-{hlid_ts_suffix}"

        if secret:
            if len(secret) < 16:
                raise ValueError("HLID secret too short; must be 16 chars or longer.")

            self._is_signed = True

            hlid_ts = "-".join(self._value.split("-")[0:-1])
            hlid_sign = self._value.split("-")[-1]
            if hlid_sign != self.__trunc_sha256_hmac_else_nonce(value=hlid_ts, secret=secret):
                raise ValueError("HLID fails HMAC check.")

        try:
            _ = self.age  # test to make sure the _value is a valid HLID
        except:
            raise ValueError("HLID invalid value.")

    def __call__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        if self._is_signed:
            return f"HLID({self._value})s"
        return f"HLID({self._value})"

    def __str__(self) -> str:
        return self._value

    @property
    def hex(self) -> str:
        """
        Return the HLID as a string with the "-" removed
        :return: str
        """
        return str(self._value).replace("-", "")

    @property
    def age(self) -> float:
        """
        Return the age in seconds of the HLID value
        :return: float
        """
        return (datetime.now(timezone.utc) - self.datetime).total_seconds()

    @property
    def time(self) -> float:
        """
        Return the time-since-epoch time value of the HLID value
        :return: float
        """
        return self.datetime.timestamp()

    @property
    def datetime(self) -> datetime:
        """
        Return the datetime that the HLID value represents
        :return: datetime
        """
        return datetime(
            year=int(self._value[0:4]),
            month=int(self._value[4:6]),
            day=int(self._value[6:8]),
            hour=int(self._value[9:11]),
            minute=int(self._value[11:13]),
            second=int(self._value[14:16]),
            microsecond=int(self._value[16:21].replace("-", "")) * 100,
            tzinfo=timezone.utc,
        )

    def __trunc_sha256_hmac_else_nonce(self, value: str, secret: Optional[str] = None) -> str:
        if not secret:
            return str(uuid4()).split("-")[-1]  # = 12 random hex chars

        # = first 12 sha256-hmac hex chars
        return hmac.new(secret.encode(), msg=value.encode(), digestmod=hashlib.sha256).hexdigest()[0:12]


def hlid(secret: Optional[str] = None) -> HLID:
    return HLID(secret=secret)
