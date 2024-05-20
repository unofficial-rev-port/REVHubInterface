# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import collect_data_files
from setuptools_scm import get_version, _cli
_cli.main(["ls"])

datas = []
datas += collect_data_files('sv_ttk')
binaries = []
hiddenimports = []
tmp_ret = collect_all('REVHubInterface')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


block_cipher = None


a = Analysis(
    ['REVHubInterface/__main__.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='REVHubInterface',
    icon='org.unofficialrevport.REVHubInterface.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

app = BUNDLE(
    exe,
    name='REVHubInterface.app',
    icon='org.unofficialrevport.REVHubInterface.icns',
    bundle_identifier=None,
    version=get_version(),
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleIdentifier': 'org.unofficialrevport.REVHubInterface',
        'CFBundleDisplayName': 'REV Hub Interface - Community Edition',
        'NSHumanReadableCopyright': 'Copyright © REV Robotics LLC and the Unoffical REV Port community.\nThis software is released under the BSD 3-Clause license.',
    },
)
