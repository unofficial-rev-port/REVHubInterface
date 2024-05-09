# REV Hub Interface (Community Edition)

The REV Hub Interface is a piece of software allowing for a direct connection from a REV Expansion Hub and its peripherals to a PC. 

This interface provides a method for teams to prototype with motors, servos, and sensors in a way that is faster and easier than setting up an entire robot control system. It is also a valuable troubleshooting tool that can help isolate the cause of an issue and determine if it is electrical or software related. The REV Hub Firmware can also be updated and recovered through this interface in addition to the Robot Controller Application.

This is a community continuation of the software, updating to newer underlying technologies (e.g. porting from Python 2 to Python 3), adding features, and porting to more platforms (Linux and macOS, in addition to Windows). Though initially created by REV, this version of the software is **not maintained by or affiliated with REV.**  Do **not** contact REV support about any issues you experience with this software, instead you may create a GitHub Issue or ask in https://discord.gg/pU2fesSTqF. 

This software is licensed under the BSD-3-Clause license. The full text is availiable in the LICENSE.txt file.

## Installing the software

Start by downloading the latest version of the software from [the Releases page](https://github.com/unofficial-rev-port/REVHubInterface/releases).  An `.exe` is provided for Windows systems, a Flatpak for Linux systems (soon to be published on Flathub), and a `.DMG` for macOS.
Alternately, you can download it from PyPi:

1. Install Python 3
2. Run `pip install REVHubInterface` to install
3. Finally, run `python3 -m REVHubInterface` to run the app (it should also be runnable as `revhubinterface`)

To avoid needing to run with root privileges on Ubuntu based platforms (and possibly other distributions) you need to add your user to the `dialout` group:

1. Run ```sudo usermod `whoami` -a -G dialout```
2. Reboot

Firmware updates may require installing a driver.

> [!WARNING]
> Firmware update functionality has been ommited from the initial release.

<details>
  <summary>Driver installation</summary>

- Windows: The newest versions of Windows should automatically install the required USB drivers. Alternatively, you can download the latest drivers from the [FTDI VCP website](https://www.ftdichip.com/Drivers/VCP.htm).
- Linux: The latest `libftdi` is provided in the Flatpak.  If installing via PyPI instead, you will need to install `libftdi` yourself.  On Ubuntu and derivitaves, this can be installed with `sudo apt install libftdi1`.  The package name may be similar on other distributions.
- macOS: (TODO: figure out; `brew install libftdi` doesn't seem to make the error go away. UPDATE: https://github.com/lsgunth/pyft232/pull/22 is merged but not yet published, in the mean time we should manually apply the change in our releases that have the library bundled.  Also, should we bundle `libftdi1.dylib` and its dependencies, or request users install it via Homebrew themselves?

</details>

## Connecting and Controlling an Expansion Hub

1. Connect your Expansion Hub to the computer with a USB A to USB Mini-B cable.
2. Run the REV Hub Interface Software.
3. Press Connect.  The software will scan and connect to the Expansion Hub. The various peripheral tabs will populate with controls once connected.

## Running the development version

Early binaries are availiable from the Actions tab, or from the pre-releases section of https://pypi.org/project/REVHubInterface/#history.

If you want to compile yourself rather than using a pre-packaged version, you will need to install a few additional dependencies:

- Python 3
- Tkinter
  - Windows: This is included in the Python 3 installer, just make sure sure it is selected to be installed at install time.
  - Linux: On Ubuntu and derivatives, this is instaled with `sudo apt install python3-tk`.  The package name will likely be similar on other distributions.
  - macOS: If using Homebrew, it can be install via `brew install python-tk`.
- On Linux, you will need to install `libftdi`.  On Ubuntu and derivitaves, this can be installed with `sudo apt install libftdi1`.  The package name may be similar on other distributions.
- The remaining Python dependencies (currently `pyft232` and `pyserial`, subject to future changes) can be installed via `pip3 install -r requirements.txt`
- Finally, run `python3 REVHubInterface` while in the base folder of the repo.
- Alternately, you can install onto your system from source using `pip install .` from the base folder of the repo, then using `python3 -m REVHubInterface` from anywhere.

## Compiling and publishing binaries
<details>
  <summary>Directions for developers</summary>

### PyPi
PyPi builds *should* be automated by simply updating the trigger-actions branch, however, if you want to do it manually:

1. Install build (`pip install build`) and twine (`pip install twine`)
2. Create a Github release with a tag with the proper version number (if you want a dev release just skip this step; see https://packaging.python.org/en/latest/specifications/version-specifiers/ for proper version numbering)
3. Run `python3 -m build `
4. Run `twine upload dist/*`

You may want to setup an API key for easier login, see https://packaging.python.org/en/latest/specifications/pypirc/#using-a-pypi-token

### Pyinstaller
Pyinstaller builds should be automated by pushing to the trigger-actions branch and binaries should be available in the actions tab.  However, if you'd prefer to build from source:

1. Install PyInstaller (`pip install pyinstaller`)
2. Run `pyinstaller REVHubInterface.spec`
3. The binary should be available in the `dist` folder

### Flatpak
Install Flatpak and flatpak-builder  
TODO: finish this with Flathub directions

</details>

