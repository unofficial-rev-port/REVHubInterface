import tkinter
from REVHubInterface import *


mp.freeze_support()

xroot = tk.Tk()
# Try to load nicer-looking interface on Linux if possible.  On Windows/macOS, the default Tk themes look reasonably-native.
if platform.system() != "Darwin" and platform.system() != "Windows":
    try:
        import sv_ttk
        print('Loaded Tk theme: Sun Valley')
        sv_ttk.set_theme("dark")
    except:
        pass

xroot.title('Crossplatform Hub Interface')
try:
    xroot.iconbitmap('resource\\\\favicon.ico')
except:
    try:
        xroot.iconbitmap('favicon.ico')
    except:
        pass

app = Application(xroot)
xroot.protocol('WM_DELETE_WINDOW', app.joinThreads)
print('Loading application...')
xroot.mainloop()
