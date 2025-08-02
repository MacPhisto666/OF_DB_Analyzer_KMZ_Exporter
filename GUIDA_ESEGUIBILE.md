# 🚀 Guida Creazione Eseguibile Standalone

## 📋 Prerequisiti

1. **Installa PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Verifica dipendenze installate**:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Metodo 1: Script Automatico (Raccomandato)

### 1. Esegui lo script di build:
```bash
python build_executable.py
```

Questo script:
- ✅ Verifica che PyInstaller sia installato
- ✅ Crea un file .spec ottimizzato
- ✅ Costruisce l'eseguibile
- ✅ Crea un pacchetto portatile completo

### 2. Risultato:
- 📁 `dist/AnalizzatoreDB_OpenFiber.exe` - Eseguibile standalone
- 📦 `AnalizzatoreDB_OpenFiber_Portable/` - Cartella pronta da condividere

---

## 🛠️ Metodo 2: Comando Manuale

Se preferisci il controllo manuale:

### 1. Comando base (più semplice):
```bash
pyinstaller --onefile --windowed --name "AnalizzatoreDB_OpenFiber" src/estrattore_of_GUI.py
```

### 2. Comando avanzato (con ottimizzazioni):
```bash
pyinstaller --onefile --windowed ^
  --name "AnalizzatoreDB_OpenFiber" ^
  --add-data "data/logo_azienda.png;data" ^
  --add-data "data/logo_openfiber.png;data" ^
  --hidden-import "PIL" ^
  --hidden-import "ttkbootstrap" ^
  --exclude-module "matplotlib" ^
  --exclude-module "scipy" ^
  src/estrattore_of_GUI.py
```

---

## 📊 Opzioni PyInstaller Utili

| Opzione | Significato |
|---------|-------------|
| `--onefile` | Crea un singolo file .exe |
| `--windowed` | Nasconde la console (solo GUI) |
| `--console` | Mostra la console (utile per debug) |
| `--add-data` | Include file aggiuntivi |
| `--hidden-import` | Forza inclusione moduli |
| `--exclude-module` | Esclude moduli non necessari |
| `--icon` | Imposta icona dell'eseguibile |
| `--name` | Nome del file finale |

---

## 📦 Cosa Includere nel Pacchetto

### File Essenziali per l'Amico:
```
AnalizzatoreDB_OpenFiber_Portable/
├── AnalizzatoreDB_OpenFiber.exe    # Eseguibile principale
├── data/                           # Cartella per CSV e loghi
│   ├── logo_azienda.png           # Logo personalizzato (opzionale)
│   └── logo_openfiber.png         # Logo OpenFiber (opzionale)
├── output/                         # Cartella per risultati
└── README.txt                     # Istruzioni per l'uso
```

### Istruzioni per l'Amico:
1. **Estrai il ZIP** ricevuto
2. **Posiziona il file CSV** nella cartella `data/`
3. **Avvia** `AnalizzatoreDB_OpenFiber.exe`
4. **Seleziona il file** con "Sfoglia"
5. **Applica filtri** (opzionale)
6. **Avvia elaborazione**
7. **Trova i risultati** nella cartella `output/`

---

## 🐛 Risoluzione Problemi

### Errore "ModuleNotFoundError":
```bash
# Aggiungi import nascosti
pyinstaller --hidden-import nome_modulo
```

### Eseguibile troppo grande:
```bash
# Escludi moduli non necessari
pyinstaller --exclude-module matplotlib --exclude-module scipy
```

### Console che si chiude subito:
```bash
# Usa --console per vedere errori
pyinstaller --console src/estrattore_of_GUI.py
```

### File non trovati:
```bash
# Aggiungi file con --add-data
pyinstaller --add-data "source;destination"
```

---

## ⚡ Ottimizzazioni Dimensione

Per ridurre la dimensione dell'eseguibile:

1. **Escludi moduli non necessari**:
   ```bash
   --exclude-module matplotlib
   --exclude-module scipy
   --exclude-module pytest
   --exclude-module unittest
   ```

2. **Usa UPX** (compressore):
   ```bash
   --upx-dir path/to/upx
   ```

3. **Versione "directory"** invece di onefile:
   ```bash
   pyinstaller --windowed src/estrattore_of_GUI.py
   # Crea una cartella con più file, ma più veloce all'avvio
   ```

---

## 🎯 Risultato Finale

Al termine avrai:
- 📁 **Un eseguibile standalone** (≈30-80MB)
- 🚀 **Avvio veloce** senza installazioni Python
- 🎨 **Interfaccia completa** con tutti i filtri
- 📊 **Log in tempo reale** nella GUI
- 🌍 **Export KMZ** per Google Earth
- 📋 **Tutti i 10 filtri STATO_UI** funzionali

Il tuo amico potrà usare l'applicazione **senza installare Python** o dipendenze! 🎉

---

## 📝 Note Importanti

- ⏳ **Prima compilazione**: Può richiedere 2-5 minuti
- 💾 **Spazio necessario**: ≈500MB durante la compilazione
- 🔒 **Antivirus**: Potrebbe segnalare falsi positivi
- 🪟 **Windows Defender**: Potrebbe chiedere conferma al primo avvio

---

**Versione Testata**: Windows 10/11, Python 3.8+  
**Dimensione finale**: ≈40-80MB (dipende dalle dipendenze)