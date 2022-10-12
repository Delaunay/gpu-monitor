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


def is_amd_gpu():
    """Returns true if amdgpu is found in the list of initialized modules"""
    import subprocess

    driverInitialized = ""

    try:
        driverInitialized = str(
            subprocess.check_output(
                "cat /sys/module/amdgpu/initstate | grep live", shell=True
            )
        )
    except subprocess.CalledProcessError:
        pass

    if len(driverInitialized) > 0:
        return True

    return False
