# Rev Hardware Client (Community version)

The REV Hub Interface is a piece of software allowing for a direct connection from a REV Expansion Hub and its peripherals to a PC. 

This interface provides a method for teams to prototype with motors, servos, and sensors in a way that is faster and easier than setting up an entire robot control system. It is also a valuable troubleshooting tool that can help isolate the cause of an issue and determine if it is electrical or software related. The REV Hub Firmware can also be updated and recovered through this interface in addition to the Robot Controller Application.

This is a community continuation of the software, updating to newer underlying technologies (e.g. porting from Python 2 to Python 3), adding features, and porting to more platforms (Linux and macOS, in addition to Windows).

## Installing the software

Start by downloading the latest version of teh software from [the Releases page](https://github.com/unofficial-rev-port/REVHubInterface/releases).  An `.exe` is provided for Windows systems, an AppImage for Linux systems, and a `.DMG` for macOS.

You may also need the appropriate dirver.

- Windows: The newest versions of Windows should automatically install the required USB drivers. Alternatively, you can download the latest drivers from the [FTDI VCP website](https://www.ftdichip.com/Drivers/VCP.htm).
- Linux: The latest `libftdi.so` is provided in the download, no additional action should be necessary.
- macOS: (TODO: figure out; `brew install libftdi` doesn't seem to make the error go away)

## Connecting and Controlling an Expansion Hub

1. Connect your Expansion Hub to the computer with a USB A to USB Mini-B cable.
2. Run the REV Hub Interface Software.
3. The software will scan and connect to the Expansion Hub. The various peripheral tabs will populate with controls once connected.

## Running the development version

If you want to run the development version from this repository rather than using a pre=packaged version, you will need a few extra things:

- Python 3
- Tkinter
  - Windows: This is included in the Python 3 installer, just make sure sure it is selected to be installed at install time.
  - Linux: On Ubuntu and derivatives, this is instaled with `sudo apt install python3-tk`.  The package name will likely be similar on other distributions.
  - macOS: If using Homebrew, it can be install via `brew install python-tk`.
- On Linux, you will also need the latest `libftdi.so`.  On Ubuntu and derivitaves, this can be installed with `sudo apt install libftdi-dev`.  The package name may be similar on other distributions.
- The remaining Python dependencies (currently `pyft232` and `pyserial`, subject to future changes) can be installed via `pip3 install -r requirements.txt`
