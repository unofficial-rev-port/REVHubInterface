# REV Hub Interface - Community Edition
[![Discord](https://img.shields.io/discord/1237587540014403614?style=flat&logo=discord&color=5865F2&label=Join%20our%20Discord%21)](https://discord.gg/2CJqU6YX2W)
[![PyPI - Version](https://img.shields.io/pypi/v/REVHubInterface?label=Latest%20Version%20%28PyPI%29)](https://pypi.org/project/REVHubInterface/)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/unofficial-rev-port/REVHubInterface/total?label=GitHub%20Downloads)](https://github.com/unofficial-rev-port/REVHubInterface/releases)
![Flathub Downloads](https://img.shields.io/flathub/downloads/org.unofficialrevport.REVHubInterface?label=Flathub%20Downloads)


The Community Edition of REV Hub Interface is a Community run fork of the REV hub interface, with a focus on making it the best tool it can be for First Tech Challenge teams. The Community Edition REV Hub Interface allows you to manually control an Expansion Hub from your computer, which is great for prototyping mechanisms in realistic conditions. Originally, it was simply a port of REV's release to Linux and MacOS, however, it has since grown greatly with a more modern UI, more control features, and a backend overhaul making everything more responsive and accurate.

Though the original version of the software was created by REV Robotics, this version of the software is <ins>not maintained by or affiliated with REV Robotics</ins>.  Please do <ins>**not**</ins> contact REV Robotics official support about any issues you experience with this software; instead, you may create a GitHub Issue or ask in [our Discord server](https://discord.gg/pU2fesSTqF).

This software is licensed under the BSD-3-Clause license which we inherited from REV. The full text is availiable in the LICENSE.txt file.

## Installing the software

<a href='https://flathub.org/apps/org.unofficialrevport.REVHubInterface'><img width='240' alt='Download on Flathub' src='https://flathub.org/api/badge?svg&locale=en'/></a>

Start by downloading the latest version of the software from [the Releases page](https://github.com/unofficial-rev-port/REVHubInterface/releases).  
An `.exe` is provided for Windows systems, a `.DMG` for macOS, and AUR Pkgbuild, Flatpak, and binary for Linux
You can [download from Flathub here](https://flathub.org/apps/org.unofficialrevport.REVHubInterface).
Alternately, you can download it from PyPi:

1. Install Python 3
2. Run `pip install REVHubInterface` to install
3. Finally, run `python3 -m REVHubInterface` to run the app (it should also be runnable as `revhubinterface`)

To avoid needing to run with root privileges on Linux you need to add your user to the `dialout` group:

1. Run ```sudo usermod `whoami` -a -G dialout``` (on Arch Linux, you need to use `uucp` instead of `dialout`)
2. Reboot


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
  - Linux: On Ubuntu and derivatives, this is instaled with `sudo apt install python3-tk`. On arch, it can be installed with `sudo pacman -Su tk` The package name will likely be similar on other distributions.
  - macOS: If using Homebrew, it can be install via `brew install python-tk`.
