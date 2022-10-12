from gpusmi.core.monitor import Monitor, MemoryInfo, UtilizationRates


# https://github.com/GPUOpen-LibrariesAndSDKs/AGS_SDK
# or
# https://github.com/RadeonOpenCompute/rocm_smi_lib
# rocm-smi lib relies on UNIX filesystem


# the bindings for rocm-smi are inside
# /opt/rocm/rocm_smi/bindings/

import sys
import logging
from ctypes import c_uint64, c_uint32, byref, c_char_p, c_int64

sys.path.insert(0, "/opt/rocm/rocm_smi/bindings/")


from rsmiBindings import *


RETCODE = 0


def rsmi_ret_ok(my_ret, device=None, metric=None, silent=False):
    """ Returns true if RSMI call status is 0 (success)

    If status is not 0, error logs are written to the debug log and false is returned

    @param device: DRM device identifier
    @param my_ret: Return of RSMI call (rocm_smi_lib API)
    @param metric: Parameter of GPU currently being analyzed
    """
    global RETCODE
    global PRINT_JSON

    if my_ret != rsmi_status_t.RSMI_STATUS_SUCCESS:

        err_str = c_char_p()
        rocmsmi.rsmi_status_string(my_ret, byref(err_str))

        returnString = ''
        if device is not None:
            returnString += '%s GPU[%s]:' % (my_ret, device)
        if metric is not None:
            returnString += ' %s: ' % (metric)

        returnString += '%s\t' % (err_str.value.decode())
        if not PRINT_JSON:
            logging.debug('%s', returnString)

            if not silent:
                # if my_ret in rsmi_status_verbose_err_out:
                #    printLog(device, rsmi_status_verbose_err_out[my_ret], None)

        RETCODE = my_ret
        return False
    return True


class AMDMonitor(Monitor):

    def __init__(self) -> None:
        super().__init__()
        ret_init = rocmsmi.rsmi_init(0)

    def close(self):
        rocmsmi.rsmi_shut_down()

    def memory(self, device_id) -> MemoryInfo:
        memoryUse = c_uint64()
        memoryTot = c_uint64()
        memType = 'VRAM'

        info = MemoryInfo()

        ret = rocmsmi.rsmi_dev_memory_usage_get(device_id, memory_type_l.index(memType), byref(memoryUse))

        if rsmi_ret_ok(ret, device_id, memType):
            info.used = memoryUse.value

        ret = rocmsmi.rsmi_dev_memory_total_get(device_id, memory_type_l.index(memType), byref(memoryTot))
        if rsmi_ret_ok(ret, device_id, memType + ' total'):
            info.total = memoryTot.value

        info.free = info.total - info.used
        return info

    def utilization(self, device_id) -> UtilizationRates:
        utils = UtilizationRates()

        percent = c_uint32()
        ret = rocmsmi.rsmi_dev_busy_percent_get(device_id, byref(percent))

        if rsmi_ret_ok(ret, device_id, 'GPU Utilization '):
            utils.gpu = percent.value

        return utils

    def temperature(self, device_id) -> int:
        sensor = 'junction'

        temp = c_int64(0)
        metric = rsmi_temperature_metric_t.RSMI_TEMP_CURRENT

        ret = rocmsmi.rsmi_dev_temp_metric_get(c_uint32(device_id), temp_type_lst.index(sensor), metric, byref(temp))

        if rsmi_ret_ok(ret, device_id, sensor, True):
            return temp.value / 1000

        return 0

    def power(self, device_id) -> int:
        power = c_uint32()
        ret = rocmsmi.rsmi_dev_power_ave_get(device_id, 0, byref(power))

        if rsmi_ret_ok(ret, device_id, 'power'):
            return power.value / 1000000

        return 0
