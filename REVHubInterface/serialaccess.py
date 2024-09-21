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

def getAccess():
    # Get all groups that exist on the system
    all_groups = grp.getgrall()

    # Check if 'dialout' or 'uucp' is in any of the available group names, and set it as the group to use if so
    group_to_use = 'unknown'
    for group in all_groups:
        if 'dialout' in group.gr_name.lower():
            group_to_use = 'dialout'
            break
        if 'uucp' in group.gr_name.lower():
            group_to_use = 'uucp'
            break

    if group_to_use == 'unknown':
        raise Exception("Neither dialout or uucp seem to exist.")

    if os.path.exists("/usr/bin/flatpak-spawn"):
        command_result = os.system("/usr/bin/flatpak-spawn --host pkexec usermod $USER -a -G dialout")
    else:
        command_result = os.system("pkexec usermod $USER -a -G dialout")

    if command_result != 0:
        raise Exception("Unexpected command exit code: " + str(command_result))
