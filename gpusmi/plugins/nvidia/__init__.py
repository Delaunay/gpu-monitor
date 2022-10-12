from gpusmi.core.monitor import Monitor, MemoryInfo, UtilizationRates

IMPORT_ERROR = None

try:
    from pynvml import *
except ImportError as err:
    IMPORT_ERROR = err


class NVMonitor(Monitor):
    def __init__(self) -> None:
        super().__init__()

        if IMPORT_ERROR is not None:
            raise IMPORT_ERROR

        self.noop = False

        try:
            nvmlInit()
        except NVML_ERROR_DRIVER_NOT_LOADED:
            self.noop = True

        self.device_count = self._call(nvmlDeviceGetCount, default=0)

    def _call(self, function, *args, default=None):
        if self.noop:
            return default

        return function(*args)

    def _device(self, index):
        return self._call(nvmlDeviceGetHandleByIndex, index)


    def close(self):
        self._call(nvmlShutdown)

    def memory(self, device_id) -> MemoryInfo:
        memory = self._call(nvmlDeviceGetMemoryInfo, self._device(device_id), default=MemoryInfo())
        value = MemoryInfo()
        value.free = memory.free
        value.used = memory.used
        value.total = memory.total
        return value

    def utilization(self, device_id) -> UtilizationRates:
        """Percent of time over the past sample period during which one or more kernels was executing on the GPU.

        Notes
        -----
        This does NOT show how well the GPU is utilized, a single kernel using a single cuda core for 100% of the sample time
        will make this value show an gpu utilization rate of 100%!

        """
        utils = self._call(nvmlDeviceGetUtilizationRates, self._device(device_id), default=UtilizationRates())
        value = UtilizationRates()
        value.gpu = utils.gpy
        value.memory = utils.memory
        return value

    def temperature(self, device_id) -> int:
        """in degrees C"""
        return self._call(nvmlDeviceGetTemperature, self._device(device_id), NVML_TEMPERATURE_GPU, default=0)

    def power(self, device_id) -> int:
        """Power in milliwatts"""
        return self._call(nvmlDeviceGetPowerUsage, self._device(device_id), default=0)
