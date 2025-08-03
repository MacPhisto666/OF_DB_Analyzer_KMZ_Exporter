# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Dati da includere nell'eseguibile
added_files = [
    ('data/logo_azienda.png', 'data'),
    ('data/logo_openfiber.png', 'data'),
]

# Moduli nascosti (dipendenze che PyInstaller potrebbe non rilevare)
hidden_imports = [
    # Moduli locali del progetto
    'estrattore_of',
    'config',
    'kmz_exporter',
    # Dipendenze esterne
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'ttkbootstrap',
    'ttkbootstrap.constants',
    'pandas',
    'openpyxl',
    'queue',
    'threading',
    'datetime',
    'xml.etree.ElementTree',
    'zipfile',
    'secrets',  # Necessario per numpy/pandas
    'numpy.random',
    'numpy.random.bit_generator',
]

a = Analysis(
    ['src/estrattore_of_GUI.py'],
    pathex=['src'],  # Aggiungi src al path per trovare i moduli locali
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',  # Esclude matplotlib se non usato
        'scipy',       # Esclude scipy se non usato
        'numpy.testing',
        'pytest',
        'unittest',
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
