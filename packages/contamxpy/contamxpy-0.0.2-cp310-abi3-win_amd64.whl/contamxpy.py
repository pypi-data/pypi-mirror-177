from __future__ import annotations

import _contamxpy

_lib = _contamxpy.lib
_ffi = _contamxpy.ffi

#print(f"_contamxpy => \n\t{dir(_contamxpy)}")

'''
    cxiGetContamState() is defined in contam-x-cosim.c
'''
def getState():
    return _lib.cxiGetContamState()

def setWindPressureMode(state, mode):
    _lib.cxiSetWindPressureMode(state, mode)

def getVersion(state):
    bufStr = _ffi.new("char[]", 64)
    _lib.cxiGetVersion(state, bufStr)
    return _ffi.string(bufStr).decode('utf-8')

def setupSimulation(state, prjPath, useCosim):
    _lib.cxiSetupSimulation(state, prjPath.encode('ascii'), useCosim)

def getSimTimeStep(state):
    timeStep = _lib.cxiGetSimulationTimeStep(state)
    return timeStep

def getSimStartDate(state):
    dayOfYear = _lib.cxiGetSimulationStartDate(state)
    return dayOfYear

def getSimEndDate(state):
    dayOfYear = _lib.cxiGetSimulationEndDate(state)
    return dayOfYear

def getSimStartTime(state):
    timeOfDaySeconds = _lib.cxiGetSimulationStartTime(state)
    return timeOfDaySeconds

def getSimEndTime(state):
    timeOfDaySeconds = _lib.cxiGetSimulationEndTime(state)
    return timeOfDaySeconds

def getCurrentDayOfYear(state):
    return _lib.cxiGetCurrentDate(state)

def getCurrentTimeInSec(state):
    return _lib.cxiGetCurrentTime(state)

def doSimStep(state, stepForward):
    _lib.cxiDoCoSimStep(state, stepForward)

def endSimulation(state):
    _lib.cxiEndSimulation(state)