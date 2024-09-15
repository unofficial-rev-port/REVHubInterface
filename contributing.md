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

1. Install PyInstaller (`pip install pyinstaller` or it may be present in a distro repository)
2. Run `pyinstaller REVHubInterface.spec`
3. The binary should be available in the `dist` folder

### Flatpak
Install Flatpak and flatpak-builder  
TODO: finish this with Flathub directions

</details>
