import sys, glob, os

def hasAccess():
    if sys.platform != "linux":
        return True
    ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
    if not ports:
        return True  # nothing to test against; don't block the user
    return any(os.access(p, os.R_OK | os.W_OK) for p in ports)
