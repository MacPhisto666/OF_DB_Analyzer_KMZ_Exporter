#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per creare eseguibile standalone dell'Analizzatore DB OpenFiber
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Fix encoding per Windows
try:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

def check_pyinstaller():
    """Verifica se PyInstaller è installato"""
    try:
        import PyInstaller
        print("✅ PyInstaller disponibile")
        return True
    except ImportError:
        print("❌ PyInstaller non trovato")
        print("💡 Installa con: pip install pyinstaller")
        return False

def create_spec_file():
    """Crea il file .spec personalizzato per l'applicazione"""
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Dati da includere nell'eseguibile
added_files = [
    ('data/logo_azienda.png', 'data'),
    ('data/logo_openfiber.png', 'data'),
]

# Moduli nascosti (dipendenze che PyInstaller potrebbe non rilevare)
hidden_imports = [
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
]

a = Analysis(
    ['src/estrattore_of_GUI.py'],
    pathex=[],
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
'''
    
    with open('AnalizzatoreDB_OpenFiber.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ File .spec creato: AnalizzatoreDB_OpenFiber.spec")

def build_executable():
    """Costruisce l'eseguibile usando PyInstaller"""
    
    print("🔨 Costruzione eseguibile in corso...")
    print("⏳ Questo potrebbe richiedere alcuni minuti...")
    
    try:
        # Comando PyInstaller
        cmd = [
            'pyinstaller',
            '--clean',           # Pulisce cache precedenti
            '--noconfirm',       # Non chiede conferma per sovrascrivere
            'AnalizzatoreDB_OpenFiber.spec'
        ]
        
        print(f"🚀 Eseguendo: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Eseguibile creato con successo!")
            
            # Verifica che il file esista
            exe_path = Path('dist/AnalizzatoreDB_OpenFiber.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📁 File creato: {exe_path}")
                print(f"📊 Dimensione: {size_mb:.1f} MB")
                return True
            else:
                print("❌ File eseguibile non trovato!")
                return False
        else:
            print("❌ Errore durante la costruzione:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Errore: {e}")
        return False

def create_portable_package():
    """Crea un pacchetto portatile con tutto il necessario"""
    
    print("\n📦 Creazione pacchetto portatile...")
    
    package_dir = Path("AnalizzatoreDB_OpenFiber_Portable")
    
    # Crea directory
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copia eseguibile
    exe_source = Path("dist/AnalizzatoreDB_OpenFiber.exe")
    if exe_source.exists():
        shutil.copy2(exe_source, package_dir / "AnalizzatoreDB_OpenFiber.exe")
        print("✅ Eseguibile copiato")
    
    # Crea cartelle necessarie
    (package_dir / "data").mkdir()
    (package_dir / "output").mkdir()
    
    # Copia loghi se esistono
    for logo in ["logo_azienda.png", "logo_openfiber.png"]:
        logo_path = Path(f"data/{logo}")
        if logo_path.exists():
            shutil.copy2(logo_path, package_dir / "data" / logo)
            print(f"✅ Logo copiato: {logo}")
    
    # Crea README per l'utente
    readme_content = """# Analizzatore DB OpenFiber v2.1.2 - Versione Portatile

## 🚀 Come Usare

1. **Posiziona il file CSV**: Metti il tuo file CSV OpenFiber nella cartella `data/`
2. **Avvia l'applicazione**: Doppio click su `AnalizzatoreDB_OpenFiber.exe`
3. **Seleziona il file**: Usa il pulsante "Sfoglia" per scegliere il CSV
4. **Applica filtri**: (Opzionale) Seleziona filtri STATO_UI nella sezione dedicata
5. **Elabora**: Clicca "Avvia Elaborazione"
6. **Risultati**: I file Excel (e KMZ se abilitato) saranno nella cartella `output/`

## 📁 Struttura Cartelle

- `AnalizzatoreDB_OpenFiber.exe` - Applicazione principale
- `data/` - Metti qui i file CSV e i loghi personalizzati
- `output/` - I file elaborati appariranno qui

## 🛠️ Filtri Disponibili

L'applicazione può filtrare i dati per STATO_UI:
- 🏠 FTTH Vendibili [102]
- 🏛️ PAC/PAL [302] 
- 📡 FWA Vendibili [202]
- E molti altri...

## 📋 Requisiti

- Windows 10/11
- File CSV OpenFiber (formato con separatore |)
- Spazio libero: almeno 100MB per elaborazioni

## 🆘 Problemi?

Se l'applicazione non si avvia:
1. Verifica che Windows non blocchi l'eseguibile (click destro → Proprietà → Sblocca)
2. Esegui come amministratore se necessario
3. Controlla che il file CSV sia nel formato corretto

---
Sviluppato con ❤️ per l'analisi dati OpenFiber
"""
    
    with open(package_dir / "README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README.txt creato")
    
    # Calcola dimensione totale
    total_size = sum(f.stat().st_size for f in package_dir.rglob('*') if f.is_file())
    total_size_mb = total_size / (1024 * 1024)
    
    print(f"\n🎉 Pacchetto portatile creato!")
    print(f"📁 Cartella: {package_dir}")
    print(f"📊 Dimensione totale: {total_size_mb:.1f} MB")
    print(f"\n💡 Comprimi la cartella '{package_dir}' in un ZIP")
    print("   e inviala al tuo amico!")

def main():
    """Funzione principale"""
    print("🚀 CREAZIONE ESEGUIBILE ANALIZZATORE DB OPENFIBER")
    print("=" * 60)
    
    # Verifica directory corrente
    if not Path("src/estrattore_of_GUI.py").exists():
        print("❌ Esegui questo script dalla directory principale del progetto")
        sys.exit(1)
    
    # Verifica PyInstaller
    if not check_pyinstaller():
        print("\n💡 Per installare PyInstaller:")
        print("   pip install pyinstaller")
        sys.exit(1)
    
    print(f"\n📂 Directory corrente: {os.getcwd()}")
    
    # Crea file .spec
    create_spec_file()
    
    # Costruisci eseguibile
    if build_executable():
        # Crea pacchetto portatile
        create_portable_package()
        
        print("\n" + "=" * 60)
        print("🎉 ESEGUIBILE CREATO CON SUCCESSO!")
        print("\n📦 Per condividere con il tuo amico:")
        print("1. Comprimi la cartella 'AnalizzatoreDB_OpenFiber_Portable' in un ZIP")
        print("2. Invia il file ZIP")
        print("3. Il tuo amico dovrà solo estrarre e avviare l'eseguibile!")
        
    else:
        print("\n❌ CREAZIONE FALLITA")
        print("💡 Controlla gli errori sopra e riprova")

if __name__ == "__main__":
    main()