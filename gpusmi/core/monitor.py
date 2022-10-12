
from dataclasses import dataclass


@dataclass
class MemoryInfo:
    free: float = 0
    total: float = 0
    used: float = 0


@dataclass
class UtilizationRates:
    gpu: int
    memory: int


class Monitor:
    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        raise NotImplementedError()

    def memory(self, device_id) -> MemoryInfo:
        raise NotImplementedError()

    def utilization(self, device_id) -> UtilizationRates:
        raise NotImplementedError()

    def temperature(self, device_id) -> int:
        raise NotImplementedError()

    def power(self, device_id) -> int:
        raise NotImplementedError()

