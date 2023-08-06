import time
import cpuinfo
from pynvml import *
import psutil

def tracker_start():
  return time.time();


def tracker_end():
  return time.time();
  

def tracker(tracker_end,tracker_start):
    print ()
    calc=tracker_end-tracker_start
    cpupower= psutil.cpu_percent(calc)
    cpuname =cpuinfo.get_cpu_info()['brand_raw']
    print ('CPU Name :' + cpuname)
    print ('CPU Usage Percent :' + str(cpupower))
    print()
    

    nvmlInit()
    deviceCount = nvmlDeviceGetCount()
    mW_to_W= 1e3
    for i in range(deviceCount):
       handle = nvmlDeviceGetHandleByIndex(i)
       measure = nvmlDeviceGetPowerUsage(handle)// mW_to_W
       print("GPU Name",":", nvmlDeviceGetName(handle))
       print('GPU Power:' + str(measure)+"W")
       print()

    print ('Time Taken :' + str(calc))