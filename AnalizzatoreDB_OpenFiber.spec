# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Dati da includere nell'eseguibile
added_files = [
    ('data/logo_azienda.png', 'data'),
    ('data/logo_openfiber.png', 'data'),
]

# Moduli nascosti (dipendenze che PyInstaller potrebbe non rilevare)
hidden_imports = [
    'estrattore_of',  # Modulo locale principale
    'config',         # Modulo locale configurazione
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'ttkbootstrap',
    'ttkbootstrap.constants',
    'pandas',
    'pandas._libs',
    'pandas._libs.tslib',
    'pandas._libs.tslibs',
    'pandas._libs.tslibs.base',
    'numpy',
    'numpy.random',
    'numpy.random.bit_generator',
    'numpy.random._pickle',
    'openpyxl',
    'openpyxl.styles',
    'openpyxl.workbook',
    'openpyxl.worksheet',
    'queue',
    'threading',
    'datetime',
    'xml.etree.ElementTree',
    'zipfile',
    'secrets',  # Modulo mancante per numpy.random
    'hashlib',
    'hmac',
    'base64',
    'io',
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
]

a = Analysis(
    ['src/estrattore_of_GUI.py'],
    pathex=['src'],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # Esclude matplotlib se non usato
        'scipy',       # Esclude scipy se non usato
        'pytest',
        'unittest',
        'test',
        'tests',
    ],
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
    name='AnalizzatoreDB_OpenFiber',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Mostra console per debug - cambia a False per nasconderla
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='data/logo_openfiber.png',  # Icona dell'eseguibile (opzionale)
)
