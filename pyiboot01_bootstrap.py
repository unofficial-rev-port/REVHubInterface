# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Aug 23 2022, 17:18:36) 
# [GCC 11.2.0]
# Embedded file name: site-packages\PyInstaller\loader\pyiboot01_bootstrap.py
import sys, pyimod03_importers
pyimod03_importers.install()
import os
if not hasattr(sys, 'frozen'):
    sys.frozen = True
sys.prefix = sys._MEIPASS
sys.exec_prefix = sys.prefix
sys.base_prefix = sys.prefix
sys.base_exec_prefix = sys.exec_prefix
VIRTENV = 'VIRTUAL_ENV'
if VIRTENV in os.environ:
    os.environ[VIRTENV] = ''
    del os.environ[VIRTENV]
python_path = []
for pth in sys.path:
    if not os.path.isabs(pth):
        pth = os.path.abspath(pth)
    python_path.append(pth)
    sys.path = python_path

class NullWriter:
    softspace = 0
    encoding = 'UTF-8'

    def write(*args):
        pass

    def flush(*args):
        pass

    def isatty(self):
        return False


if sys.stdout is None or sys.stdout.fileno() < 0:
    sys.stdout = NullWriter()
if sys.stderr is None or sys.stderr.fileno() < 0:
    sys.stderr = NullWriter()
try:
    import encodings
except ImportError:
    pass

if sys.warnoptions:
    import warnings
try:
    import ctypes, os
    from ctypes import LibraryLoader, DEFAULT_MODE

    def _frozen_name(name):
        if name:
            frozen_name = os.path.join(sys._MEIPASS, os.path.basename(name))
            if os.path.exists(frozen_name):
                name = frozen_name
        return name


    class PyInstallerImportError(OSError):

        def __init__(self, name):
            self.msg = 'Failed to load dynlib/dll %r. Most probably this dynlib/dll was not found when the application was frozen.' % name
            self.args = (self.msg,)


    class PyInstallerCDLL(ctypes.CDLL):

        def __init__(self, name, *args, **kwargs):
            name = _frozen_name(name)
            try:
                super(PyInstallerCDLL, self).__init__(name, *args, **kwargs)
            except Exception as base_error:
                raise PyInstallerImportError(name)


    ctypes.CDLL = PyInstallerCDLL
    ctypes.cdll = LibraryLoader(PyInstallerCDLL)

    class PyInstallerPyDLL(ctypes.PyDLL):

        def __init__(self, name, *args, **kwargs):
            name = _frozen_name(name)
            try:
                super(PyInstallerPyDLL, self).__init__(name, *args, **kwargs)
            except Exception as base_error:
                raise PyInstallerImportError(name)


    ctypes.PyDLL = PyInstallerPyDLL
    ctypes.pydll = LibraryLoader(PyInstallerPyDLL)
    if sys.platform.startswith('win'):

        class PyInstallerWinDLL(ctypes.WinDLL):

            def __init__(self, name, *args, **kwargs):
                name = _frozen_name(name)
                try:
                    super(PyInstallerWinDLL, self).__init__(name, *args, **kwargs)
                except Exception as base_error:
                    raise PyInstallerImportError(name)


        ctypes.WinDLL = PyInstallerWinDLL
        ctypes.windll = LibraryLoader(PyInstallerWinDLL)

        class PyInstallerOleDLL(ctypes.OleDLL):

            def __init__(self, name, *args, **kwargs):
                name = _frozen_name(name)
                try:
                    super(PyInstallerOleDLL, self).__init__(name, *args, **kwargs)
                except Exception as base_error:
                    raise PyInstallerImportError(name)


        ctypes.OleDLL = PyInstallerOleDLL
        ctypes.oledll = LibraryLoader(PyInstallerOleDLL)
except ImportError:
    pass

if sys.platform.startswith('darwin'):
    try:
        from ctypes.macholib import dyld
        dyld.DEFAULT_LIBRARY_FALLBACK.insert(0, sys._MEIPASS)
    except ImportError:
        pass

d = 'eggs'
d = os.path.join(sys._MEIPASS, d)
if os.path.isdir(d):
    for fn in os.listdir(d):
        sys.path.append(os.path.join(d, fn))

# okay decompiling pyiboot01_bootstrap.pyc
