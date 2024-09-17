import grp
import os, sys

def hasAccess():
    if sys.platform == "linux":
        try:
            groups = [g.gr_name for g in grp.getgrall() if os.getlogin() in g.gr_mem]
            if 'dialout' in groups or 'uucp' in groups: return True
            return False
        except KeyError:
            return False
    else: return True
