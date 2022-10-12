from gpusmi.core.monitor import Monitor, MemoryInfo, UtilizationRates


# https://github.com/GPUOpen-LibrariesAndSDKs/AGS_SDK
# or
# https://github.com/RadeonOpenCompute/rocm_smi_lib
# rocm-smi lib relies on UNIX filesystem


# agsInitialize
# agsDeInitialize

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
