import grp
import getpass
import sys

def hasAccess():
    if sys.platform == "linux":
        try:
            user = getpass.getuser()  # Alternative to os.getlogin()
            groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
            if 'dialout' in groups or 'uucp' in groups: return True
            return False
        except KeyError:
            return False
    else: return True
