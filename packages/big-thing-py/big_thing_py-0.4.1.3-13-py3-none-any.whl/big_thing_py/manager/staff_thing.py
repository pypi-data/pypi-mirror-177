from big_thing_py.core.thing import *
from big_thing_py.utils import *
from big_thing_py.common import *


class SoPStaffThing(SoPThing):
    def __init__(self, name: str, service_list: List[SoPService], alive_cycle: float, is_super: bool = False, is_parallel: bool = True,
                 device_id: str = None):
        super().__init__(name, service_list, alive_cycle, is_super, is_parallel)
        self._device_id = device_id

    # TODO: Check this method works correct
    def __eq__(self, o: object) -> bool:
        return super().__eq__(o) and (o._device_id == self._device_id)

    def get_device_id(self) -> str:
        return self._device_id

    def set_device_id(self, id: str) -> None:
        self._device_id = id

    def set_function_publish_queue(self, publish_queue: Queue):
        for function in self._function_list:
            function.set_publish_queue(publish_queue)
