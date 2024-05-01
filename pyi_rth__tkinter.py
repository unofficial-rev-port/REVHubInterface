# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Aug 23 2022, 17:18:36) 
# [GCC 11.2.0]
# Embedded file name: site-packages\PyInstaller\loader\rthooks\pyi_rth__tkinter.py
import os, sys
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

tcldir = os.path.join(sys._MEIPASS, 'tcl')
tkdir = os.path.join(sys._MEIPASS, 'tk')
if not os.path.isdir(tcldir):
    raise FileNotFoundError('Tcl data directory "%s" not found.' % tcldir)
if not os.path.isdir(tkdir):
    raise FileNotFoundError('Tk data directory "%s" not found.' % tkdir)
os.environ['TCL_LIBRARY'] = tcldir
os.environ['TK_LIBRARY'] = tkdir

# okay decompiling pyi_rth__tkinter.pyc
