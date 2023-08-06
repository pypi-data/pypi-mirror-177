import contamxpy as cxLib
import os, sys
from optparse import OptionParser

#===================================================================================== main() =====
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
