import tkinter

from REVHubInterface.REVHubInterface import *

try:
    from ttkthemes import ThemedTk

    print('loaded theme')
except ModuleNotFoundError:  # could be ImportError?
    pass

mp.freeze_support()
# Try to load nicer-looking interface on Linux if possible.
# On Windows/macOS, the default TK themes look reasonably-native.
try:
    xroot = ThemedTk(theme="arc")
except NameError:
    xroot = tkinter.Tk()

xroot.title('Crossplatform Hub Interface')
try:
    xroot.iconbitmap('resource\\\\favicon.ico')
except TclError:
    try:
        xroot.iconbitmap('favicon.ico')
    except TclError:
        print("Icon not found")
        pass
app = Application(xroot)
xroot.protocol('WM_DELETE_WINDOW', app.joinThreads)
print('Loading application...')
xroot.mainloop()
