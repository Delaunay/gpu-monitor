from gpusmi.core.monitor import Monitor, MemoryInfo, UtilizationRates


class AMDMonitor(Monitor):
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
