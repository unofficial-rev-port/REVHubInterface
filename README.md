# REV Hub Interface — Community Edition
[![Discord](https://img.shields.io/discord/1237587540014403614?style=flat&logo=discord&color=5865F2&label=Join%20our%20Discord%21)](https://discord.gg/2CJqU6YX2W)
[![PyPI - Version](https://img.shields.io/pypi/v/REVHubInterface?label=Latest%20Version%20%28PyPI%29)](https://pypi.org/project/REVHubInterface/)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/unofficial-rev-port/REVHubInterface/total?label=GitHub%20Downloads)](https://github.com/unofficial-rev-port/REVHubInterface/releases)
![Flathub Downloads](https://img.shields.io/flathub/downloads/org.unofficialrevport.REVHubInterface?label=Flathub%20Downloads)


This is the Community Edition of REV Hub Interface.
REV Hub Interface allows you to manually control an Expansion Hub from your computer with zero code.
Originally created by REV, we have now ported it to Linux and macOS.
We have also added a more modern UI, more control features,
and overhauled the backend to make everything more responsive.

Though the original version of the software was created by REV Robotics,
this version is <ins>not maintained by or affiliated with REV Robotics</ins>.
Please do <ins>**not**</ins> contact REV Robotics official support about any issues you experience with this software;
instead, you may create a GitHub Issue or ask in [our Discord server](https://discord.gg/pU2fesSTqF).

This software is licensed under the BSD-3-Clause license, as is the official REV version that it is based on.
The full text is available in the LICENSE.txt file.

## Installing the software

<a href='https://flathub.org/apps/org.unofficialrevport.REVHubInterface'><img width='240' alt='Download on Flathub' src='https://flathub.org/api/badge?svg&locale=en'/></a>

Start by downloading the latest version of the software from [the Releases page](https://github.com/unofficial-rev-port/REVHubInterface/releases).  
An `.exe` is provided for Windows, a `.DMG` for macOS, and AUR Pkgbuild, Flatpak, and binary for Linux
You can [download from Flathub here](https://flathub.org/apps/org.unofficialrevport.REVHubInterface).
Alternately, you can download it from PyPi:

1. Install Python 3
2. Run `pip install REVHubInterface` to install
3. Finally, run `python3 -m REVHubInterface` to run the app (it should also be runnable as `revhubinterface`)

To avoid needing to run REV Hub Interface with root privileges on Linux, add your user to the `dialout` group:

1. Run ```sudo usermod `whoami` -a -G dialout``` (on Arch Linux, you need to use `uucp` instead of `dialout`)
2. Reboot


## Connecting and Controlling an Expansion Hub

1. Connect your Expansion Hub to the computer with a USB A to USB Mini-B cable.
2. Run the REV Hub Interface Software.
3. Press Connect.  The software will scan and connect to the Expansion Hub. The various peripheral tabs will be populated with controls once connected.

## Running the development version

Early binaries are available from the Actions tab,
or from the pre-releases section of https://pypi.org/project/REVHubInterface/#history.

To compile yourself, first install a few additional dependencies:

- Python 3
- Tkinter
  - Windows: This is included in the Python 3 installer. Make sure the checkbox to install it is selected.
  - Linux: On Ubuntu and derivatives, this is installed with `sudo apt install python3-tk`. On Arc and derivatives, it can be installed with `sudo pacman -Su tk`. The package name should be similar on other distributions.
  - macOS: If using Homebrew, it can be installed via `brew install python-tk`.

