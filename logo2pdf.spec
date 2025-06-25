# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('files','files')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    #excludes=['tkinter','PyQt6','PySide6','PySide2', 'matplotlib','xlrd', 'xlwt', 'xlsxwriter', 'openpyxl', 'pyxlsb','scipy','test'],   
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='logo2pdf',
    icon='.\\files\\images\\icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)



a.binaries = a.binaries - TOC([
    ('tcl85.dll', None, None),
    ('tk85.dll', None, None),
    ('_tkinter', None, None)
])

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='logo2pdf',
)