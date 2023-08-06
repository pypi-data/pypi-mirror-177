# Python Bindings for ContamX 

**NOTE: This package is not yet fully functional.**

This is the initial implementation of a Python wrapper for `contamx-lib` which is a dynamic link library with an API to run ContamX.  

Currently, this Python package only includes the basic components required to generate the wrapper, and the Python wrapper only implements the methods required to run a simulation from beginning to end. The demonstration imports `contamxpy`, obtains a `state`, gets properties of the simulation necessary to run from beginning to end, then steps through all the time steps.  

# Usage

Typically, one would work within a Python virtual environment which can be created and activated using the following commands.  
```
$ python -m venv .venv
$ .venv\Scripts\activate  (on Windows)
```   
Install `contamxpy` from PyPI.  
```
$(.venv) python -m pip install contamxpy
```   
## Example Test Module: *test_cxcffi.py*  
```python
import contamxpy as cxLib
import os, sys
from optparse import OptionParser

#================================================================= main() =====
def main():
    #----- Manage option parser
    parser = OptionParser(usage="%prog [options] arg1\n\targ1=PRJ filename\n")
    parser.set_defaults(verbose=0)
    parser.add_option("-v", "--verbose", action="store", dest="verbose", type="int", default=0,
                        help="Define verbose output level: 0=Min, 1=Medium, 2=Maximum.")
    (options, args) = parser.parse_args()

    #----- Process command line options -v
    verbose = options.verbose

    if len(args) != 1:
        parser.error("Need one argument:\n  arg1 = PRJ file.")
        return
    else:
        prj_name  = args[0]

    if ( not os.path.exists(prj_name) ):
        print("ERROR: PRJ file not found.")
        return

    msg_cmd = "Running test_cxcffi.py: arg1 = " + args[0] + " " + str(options)
    print(msg_cmd, "\n")

    if verbose > 1:
        print(f"cxLib attributes =>\n{chr(10).join(map(str, dir(cxLib)))}\n")

    #----- Initialize contamx-lib State
    cxState: object = cxLib.getState()
    cxLib.setWindPressureMode(cxState, 0)

    #----- Query State for Version info
    verStr = cxLib.getVersion(cxState)
    if verbose >= 0:
        print(f"getVersion() returned {verStr}.")

    #----- Setup Simulation for PRJ
    cxLib.setupSimulation(cxState, prj_name, 1)

    dayStart = cxLib.getSimStartDate(cxState)
    dayEnd   = cxLib.getSimEndDate(cxState)
    secStart = cxLib.getSimStartTime(cxState)
    secEnd   = cxLib.getSimEndTime(cxState)
    tStep    = cxLib.getSimTimeStep(cxState)

    simBegin = (dayStart - 1) * 86400 + secStart
    simEnd = (dayEnd - 1) * 86400 + secEnd
 
    #----- Calculate the simulation duration in seconds and total time steps
    if (simBegin < simEnd):
        simDuration = simEnd - simBegin
    else:
        simDuration = 365 * 86400 - simEnd + simBegin
    numTimeSteps = int(simDuration / tStep)
 
    #----- Get the current date/time after initial steady state simulation
    currentDate = cxLib.getCurrentDayOfYear(cxState)
    currentTime = cxLib.getCurrentTimeInSec(cxState)
    if verbose > 0:
        print(f"Sim days = {dayStart}:{dayEnd}")
        print(f"Sim times = {secStart}:{secEnd}")
        print(f"Sim time step = {tStep}")
        print(f"Number of steps = {numTimeSteps}")

    #----- Run Simulation
    for i in range(numTimeSteps):
        currentDate = cxLib.getCurrentDayOfYear(cxState)
        currentTime = cxLib.getCurrentTimeInSec(cxState)
        if verbose > 1:
            print(f"{i}\t{currentDate},{currentTime}")
        cxLib.doSimStep(cxState, 1)

    cxLib.endSimulation(cxState)

# --- End main() ---#

if __name__ == "__main__":
    main()
```

# Developer Notes

These bindings were developed using the **C Foreign Function Interface (CFFI)**. CFFI utilizes C header files that define the API to contamx-lib, i.e., contamx-lib.lib. It builds a dynamic Python module that incorporates the static library.  

**NOTE** The static build must include the following dependencies: `WSock32.lib`, `WS2_32.lib`, and `user32.lib`.  

## Steps to Develop Python Bindings

### 1. Create directory for *contamxpy*  
- Either clone the repo OR
- python -m pip install contamxpy (e.g., into a virtual environment)  
```
contamxpy\  
|
| setup.py
| setup.cfg
| MANIFEST.in 
| LICENSE.txt
| README.md
| contamxpy_build.py
| contamxpy.py
| contamx-lib.lib
| contamx-lib.dll
|
├── include\
|   └── common-api.h
|       commonState.h
|       contam-x-cosim.h
|       contam-x-state.h
|       element-api.h
|       flags.h
|       library-api.h
|       project-api.h
|       string-len-max.h
|       types.h
|
└── demo_files\
    └── test_cxcffi.py
        testOneZoneWthCtm.prj
        testOneZoneWthCtm.wth
        testOneZoneWthCtm.ctm
```
### 2. Create virtual environment
   `python -m venv .venv`  
   
### 3. Activate virtual environment
   + Windows => `.venv\Scripts\activate.bat`
   + Linux => `.venv/bin/activate`
   
### 4. Install *cffi* and *wheel* packages  
   `$ python -m pip install cffi, wheel`

### 5. Generate *contamxpy* 

Run the build module.
```
contamxpy_build.py
```   
This should generate *_contamxpy.c*, etc.
```
contamxpy\  
|
├── Release\
|   └── *.exp/.lib/.obj
|
└── _contamxpy.c
    _contamxpy.cp310-win_amd64.pyd
```

Most importantly it will generate a .pyd file, e.g., 
`_contamxpy-0.0.1-abi3-cp310-win_amd64.pyd`. This is a dynamic python module 
which will be imported into a driver program.  

### 6. Install the development version locally
```
$(.venv) pip install .
```
### 7. Generate Files for Distribution
Built distribution, i.e., wheel file:
```
$(.venv) python -m setup bdist_wheel
```
Source distribution, i.e., compressed archive (.gz, .zip):
```
$(.venv) python -m setup sdist
$(.venv) python -m setup sdist --format=zip
```

## Development Files  

### build_cxcffi.py

The file shown below is a minimum implementation for using `cxiLib`. 
It must be modified to incorporate the full functionality of the 
API associated with `contamx-lib.dll`.  

```python
from __future__ import annotations

# Using the "out-of-line", "API mode"
from cffi import FFI

CDEF = '''\
    // see types.h
    typedef int32_t IX;
    typedef double  R8;

    void* cxiGetContamState();
    void cxiSetupSimulation(void* contamXState, char* projectPath, IX useCosim);
    void cxiSetWindPressureMode(void* contamXState, IX useWP);

    IX cxiGetSimulationStartDate(void* contamXState);
    IX cxiGetSimulationStartTime(void* contamXState);
    IX cxiGetSimulationEndDate(void* contamXState);
    IX cxiGetSimulationEndTime(void* contamXState);
    IX cxiGetSimulationTimeStep(void* contamXState);
    IX cxiGetCurrentDate(void* contamXState);
    IX cxiGetCurrentTime(void* contamXState);
    void cxiDoCoSimStep(void* contamXState, IX stepForward);
    void cxiEndSimulation(void* contamXState);

    IX cxiGetVersion(void* contamXState, char* strVersion);
    IX cxiGetNumCtms(void* contamXState);
    IX cxiGetCtmName(void* contamXState, IX ctmNumber, char* strName);
    IX cxiGetNumZones(void* contamXState);
    IX cxiGetZoneMF(void* contamXState, IX zoneNumber, IX ctmNumber, R8* pMassFraction);
'''

SRC = '''\
    #include "include//contam-x-cosim.h"
'''

ffibuilder = FFI()
ffibuilder.cdef(CDEF)
ffibuilder.set_source(
    "_contamxpy", SRC,
    include_dirs=['.','include'],  # C header files for contam-x-lib
    libraries=['contamx-lib'],     # Library to link with (.lib, .dll)
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
```
### contamxpy
This is the wrapper module to be imported for use by driver programs as demonstrated in *test_cxcffi.py* above.
```python
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
```

### setup.py  

This file is only required if you want to install the *contamxpy* 
package within a virtual environment using pip. However, once the 
*.pyd* file is generated, it can be utilized by a python module 
along with the *contamx-lib.dll*.  

```python
from __future__ import annotations

import platform
import sys

from setuptools import setup

if platform.python_implementation() == 'CPython':
    try:
        import wheel.bdist_wheel
    except ImportError:
        cmdclass = {}
    else:
        class bdist_wheel(wheel.bdist_wheel.bdist_wheel):
            def finalize_options(self) -> None:
                self.py_limited_api = f'cp3{sys.version_info[1]}'
                super().finalize_options()

        cmdclass = {'bdist_wheel': bdist_wheel}
else:
    cmdclass = {}

setup(
    cffi_modules=['contamxpy_build.py:ffibuilder'], cmdclass=cmdclass,
    data_files=[(
        'lib\\site-packages\\', ["contamx-lib.dll"])]
    )
```

### setup.cfg

```ini
[metadata]
name = contamxpy
version = 0.0.1
description = ContamX Python wrapper
long_description = file: README.md
long_description_content_type = text/markdown
url = https://www.nist.gov/el/energy-and-environment-division-73200/nist-multizone-modeling
author = W. Stuart Dols, Brian Polidoro
author_email = william.dols@nist.gov
license = Public Domain
license_files = LICENSE.txt
classifiers =
    License :: Public Domain :: BSD License
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Programming Language :: Python :: Implementation :: CPython
    Programming Language :: Python :: Implementation :: PyPy

[options]
py_modules = contamxpy
install_requires = cffi>=1
python_requires = >=3.7
setup_requires = cffi>=1
```

### MANIFEST.in
The manifest file is used to add files to the source builds.  

```
include include\*.h
include contamx-lib.*
include demo_files\*.*
```

# REFERENCES
1. https://www.youtube.com/watch?v=X5irxO5VCHw
2. https://github.com/asottile/ukkonen
3. https://cffi.readthedocs.io/en/latest/index.html
4. https://docs.python.org/3.10/distutils/index.html
5. https://setuptools.pypa.io/en/latest/setuptools.html
6. https://packaging.python.org/en/latest/tutorials/packaging-projects/

# TODO  
- Implement full API.  
- Test on Linux  
