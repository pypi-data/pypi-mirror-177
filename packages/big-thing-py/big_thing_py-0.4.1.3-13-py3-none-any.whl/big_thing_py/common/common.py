from big_thing_py.common.error import *
from big_thing_py.common.soptype import *

from typing import *
from termcolor import *
from abc import *
from enum import Enum


EMPTY_JSON = '{}'
THREAD_TIME_OUT = 0.001


class TimeFormat(Enum):
    DATETIME1 = '%Y-%m-%d %H:%M:%S'
    DATETIME2 = '%Y%m%d_%H%M%S'
    DATE = '%Y-%m-%d'
    TIME = '%H:%M:%S'
    UNIXTIME = 'unixtime'


class SoPManagerMode(Enum):
    UNDEFINED = 'UNDEFINED'
    JOIN = 'JOIN'
    SPLIT = 'SPLIT'

    @classmethod
    def get(cls, name: str):
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class SoPNewStaffThingLevel(Enum):
    NEW = 0
    OLD = 1
    UPDATE = 2


class RequestMethod(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3


class SoPPrintMode(Enum):
    FULL = 0
    ABBR = 1
    SKIP = 2


class PrintTag:
    # MQTT protocol
    GOOD = '[%-30s]' % colored('✔✔✔', 'green')
    DUP = '[%-30s]' % colored('DUP✔', 'green')
    ERROR = '[%-30s]' % colored('✖✖✖', 'red')

    CONNECT = '[%-30s]' % colored('-> CONNECT', 'blue')
    DISCONNECT = '[%-30s]' % colored('-> DISCONNECT', 'blue')

    SUBSCRIBE = '[%-30s]' % colored('-> SUBSCRIBE', 'white')
    UNSUBSCRIBE = '[%-30s]' % colored('-> UNSUBSCRIBE', 'white')


class SoPPolicy(Enum):
    UNDEFINED = -1
    ALL = 0
    SINGLE = 1

    @classmethod
    def get(cls, name: str):
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED

# TODO: implement this


class SoPStaffThingInfo:
    def __init__(self, device_id: str) -> None:
        self.device_id = device_id


class SoPRFStaffThingInfo(SoPStaffThingInfo):
    def __init__(self, device_id: str, addresses: Tuple[int, int], value_name: str, value_cycle: float, alive_cycle: float) -> None:
        super().__init__(device_id)
        self.addresses = addresses
        self.value_name = value_name
        self.value_cycle = value_cycle
        self.alive_cycle = alive_cycle


class SoPHueStaffThingInfo(SoPStaffThingInfo):
    def __init__(self, device_id: str, idx: int, hue_info: dict) -> None:
        super().__init__(device_id)
        self.idx = idx
        self.hue_info = hue_info


class SoPHejhomeStaffThingInfo(SoPStaffThingInfo):
    def __init__(self, device_id: str, hejhome_info: dict) -> None:
        super().__init__(device_id)
        self.hejhome_info = hejhome_info


class StaffRegisterResult:
    def __init__(self, staff_thing_name: str, device_id: str, assigned_device_id: str) -> None:
        self.staff_thing_name = staff_thing_name
        self.device_id = device_id
        self.assigned_device_id = assigned_device_id
