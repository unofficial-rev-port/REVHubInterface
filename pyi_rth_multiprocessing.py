# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Aug 23 2022, 17:18:36) 
# [GCC 11.2.0]
# Embedded file name: site-packages\PyInstaller\loader\rthooks\pyi_rth_multiprocessing.py
import sys
if sys.version_info >= (3, 4):
    import os, re, multiprocessing, multiprocessing.spawn as spawn
    from subprocess import _args_from_interpreter_flags
    multiprocessing.process.ORIGINAL_DIR = None

    def _freeze_support():
        if len(sys.argv) >= 2 and set(sys.argv[1:-2]) == set(_args_from_interpreter_flags()) and sys.argv[-2] == '-c' and (sys.argv[-1].startswith('from multiprocessing.semaphore_tracker import main') or sys.argv[-1].startswith('from multiprocessing.forkserver import main')):
            exec sys.argv[-1]
            sys.exit()
        if spawn.is_forking(sys.argv):
            kwds = {}
            for arg in sys.argv[2:]:
                name, value = arg.split('=')
                if value == 'None':
                    kwds[name] = None
                else:
                    kwds[name] = int(value)

            spawn.spawn_main(**kwds)
            sys.exit()
        return


    multiprocessing.freeze_support = spawn.freeze_support = _freeze_support
try:
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking

class _Popen(forking.Popen):

    def __init__(self, *args, **kw):
        if hasattr(sys, 'frozen'):
            os.putenv('_MEIPASS2', sys._MEIPASS)
        try:
            super(_Popen, self).__init__(*args, **kw)
        finally:
            if hasattr(sys, 'frozen'):
                if hasattr(os, 'unsetenv'):
                    os.unsetenv('_MEIPASS2')
                else:
                    os.putenv('_MEIPASS2', '')


forking.Popen = _Popen

# okay decompiling pyi_rth_multiprocessing.pyc
