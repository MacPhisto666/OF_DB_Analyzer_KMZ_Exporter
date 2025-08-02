# Analizzatore DB OpenFiber v2.1.1

## 📋 Descrizione
Estrattore e analizzatore avanzato per il Database Nazionale di copertura FTTH di OpenFiber. Gestisce file CSV di grandi dimensioni (1.5GB+) per estrarre, elaborare e analizzare dati specifici della Valle d'Aosta con informazioni geografiche e infrastrutturali complete. **Ora con export KMZ per Google Earth, GUI fullscreen e naming automatico!**

## ⚡ Funzionalità Implementate

### ✅ **Estrazione Dati Avanzata**
- **Filtro regionale**: Estrazione automatica regione 02 (Valle d'Aosta)
- **Lettura chunked**: Gestione ottimizzata file grandi (1.5GB+) senza saturare la memoria
- **Selezione colonne**: Output ottimizzato con 16 colonne essenziali (rimosse 9 colonne ridondanti)
- **Ordinamento automatico**: Dati ordinati per comune per facilitare analisi
- **🆕 Naming automatico**: Nome file output con timestamp YYYYMMDD automatico

### ✅ **Arricchimento Dati Geografici**
- **Comuni mappati**: 74 comuni Valle d'Aosta con codici ISTAT → nomi italiani
- **PCN integrati**: 42 PCN OpenFiber con coordinate GPS e informazioni complete
- **Join automatico**: Correlazione POP ↔ ID PCN per dati infrastrutturali
- **Geolocalizzazione**: Latitudine/longitudine per ogni PCN

### ✅ **Output Multi-Formato Professionale**
- **Excel multi-foglio**: Un foglio separato per ogni comune (≈64 fogli)
- **Export KMZ Google Earth**: Visualizzazione cartografica sedi PAC/PAL + PCN 🆕
- **Formattazione avanzata**: Bordi, allineamento centrato, auto-resize colonne
- **Nomi fogli Excel-safe**: Gestione caratteri speciali per compatibilità
- **Struttura navigabile**: Facile consultazione per analisi specifiche per comune

### ✅ **Export KMZ per Google Earth** 🆕
- **Sedi PAC/PAL**: Solo edifici con STATO_UI=302 (Pubblica Amministrazione)
- **PCN coordinati**: Ogni PCN con colore univoco abbinato alle proprie sedi
- **Icone differenziate**: Edifici governativi per sedi, telefoni per PCN
- **Struttura organizzata**: Cartella PCN + cartelle per comune
- **Coordinate accurate**: Parsing automatico formato N45.123_E7.456
- **Colori coordinati**: 20 colori rotativi per distinguere i PCN visivamente

### ✅ **GUI Moderna Professionale**
- **🆕 Interfaccia fullscreen**: Avvio automatico a schermo pieno
- **Loghi personalizzati**: Supporto logo aziendale e OpenFiber
- **Progress tracking live**: Barra di progresso e log in tempo reale con aggiornamenti fluidi 🆕
- **Export KMZ opzionale**: Checkbox per abilitare generazione KMZ 🆕
- **Filtri interattivi**: PAC/PAL [302], Residenziali [102], personalizzati
- **Anteprima dati**: Visualizzazione rapida del CSV prima dell'elaborazione
- **🆕 Naming semplificato**: Rimozione campo nome file (generazione automatica)
- **🆕 Logging ottimizzato**: Eliminazione duplicazioni e aggiornamenti live
- **Statistiche real-time**: Metriche di performance durante elaborazione

### ✅ **Performance e Monitoring**
- **Velocità ottimizzata**: ~30.000 righe/secondo (770K righe in <50 secondi)
- **Statistiche real-time**: Progress tracking durante elaborazione
- **Coverage report**: Controllo qualità PCN mappati/non mappati
- **Dettaglio per comune**: Record count e PCN utilizzati per ogni comune

## 📊 Performance Testate
- **File input**: 1.5GB CSV (770K righe totali)
- **Regione 02 estratta**: 46.323 record in ~45 secondi
- **Comuni rappresentati**: 64 comuni Valle d'Aosta
- **PCN mappati**: 42 PCN con 100% coverage
- **Output Excel**: ~3MB multi-foglio con data automatica
- **Output KMZ**: ~50KB file cartografico per Google Earth 🆕

## 🏗️ Struttura Progetto

```
AnalizzatoreDB-OF/
├── src/                              # Codice sorgente
│   ├── estrattore_of.py             # Estrattore principale con export KMZ 🆕
│   ├── estrattore_of_GUI.py         # GUI moderna fullscreen 🆕
│   ├── kmz_exporter.py              # Modulo export Google Earth 🆕
│   └── config.py                    # Configurazione e mappature
├── data/                             # File CSV e loghi (ignorati da Git)
│   ├── dbcopertura_CD_20250715.csv  # Database OpenFiber (1.5GB)
│   ├── logo_azienda.png             # Logo aziendale (50x50px)
│   └── logo_openfiber.png           # Logo OpenFiber (567x111px)
├── output/                           # File generati (ignorati da Git)
│   ├── valle_aosta_estratto_YYYYMMDD.xlsx    # Excel con data automatica 🆕
│   └── valle_aosta_estratto_YYYYMMDD_PAC_PAL.kmz  # KMZ per Google Earth 🆕
├── docs/                            # Documentazione
│   └── documentazione_tecnica.md    # Guide sviluppo dettagliate
├── .gitignore                       # Esclude data/ e output/ da Git
└── README.md                        # Questo file
```

## 🚀 Quick Start

### Prerequisiti
```bash
# Per versione console base
pip install pandas openpyxl

# Per GUI moderna + export KMZ (raccomandato)
pip install pandas openpyxl ttkbootstrap Pillow
```

### Installazione
```bash
git clone https://github.com/MacPhisto666/AnalizzatoreDB-OF
cd AnalizzatoreDB-OF
```

### Utilizzo GUI (Raccomandato) 🆕
```bash
cd src
python estrattore_of_GUI.py
```

**Caratteristiche GUI v2.1.1:**
- 🖥️ **Fullscreen**: Avvio automatico a schermo pieno
- 🎨 **Design moderno**: Interfaccia dark professionale
- 🖼️ **Loghi personalizzati**: Supporta logo aziendale + OpenFiber
- 🌍 **Export KMZ**: Checkbox per generazione file Google Earth
- 📊 **Progress live**: Barra progresso + log in tempo reale fluido 🆕
- 🔍 **Filtri interattivi**: PAC/PAL, Residenziali, personalizzati (informativi v2.1.1)
- 📋 **Anteprima dati**: Visualizza CSV prima dell'elaborazione
- ⚙️ **Configurazione semplificata**: Nome file automatico, chunk size regolabile 🆕
- 📈 **Statistiche real-time**: Velocità, record estratti, tempo
- 🔧 **Logging ottimizzato**: Niente duplicazioni, aggiornamenti live PCN/comuni 🆕

### Utilizzo Console (Classico)
```bash
cd src
python estrattore_of.py
```

## 📝 Formato Dati e Mappature

### File CSV Sorgente
- **Separatore**: Pipe (`|`)
- **Encoding**: UTF-8
- **Dimensioni**: 1.5GB+, 770K+ righe, 25 colonne originali
- **Regioni**: Tutte le regioni italiane (filtro automatico su regione 02)

### Struttura Output Excel (16 colonne)
```
COMUNE          | Nome comune italiano (es. "Aosta")
ISTAT           | Codice ISTAT comune (es. "007003") 
PARTICELLA_TOP  | Identificativo toponomastico
INDIRIZZO       | Via/indirizzo
CIVICO          | Numero civico
ID_BUILDING     | Identificativo edificio
COORDINATE_BUILDING | Coordinate GPS edificio (N45.xx_E7.xx)
STATO_UI        | Stato unità immobiliare (302=PAC/PAL, 102=residenziale, etc.)
POP             | ID PCN OpenFiber (es. "AOCUA")
NOME_PCN        | Nome PCN completo (es. "POP_AO_11_VERRES")
COMUNE_PCN      | Comune sede PCN
LAT_PCN         | Latitudine PCN (coordinate GPS)
LON_PCN         | Longitudine PCN (coordinate GPS)
TOTALE_UI       | Totale unità immobiliari
DATA_ULTIMA_MODIFICA_RECORD | Timestamp ultima modifica
DATA_ULTIMA_VARIAZIONE_STATO_BUILDING | Variazione stato edificio
```

### Struttura Output KMZ 🆕
```
Sedi PAC/PAL VdA YYYYMMDD/
├── 📡 PCN OpenFiber/          # Cartella con tutti i PCN
│   ├── POP_AO_11_VERRES      # PCN con icona telefono colorata
│   ├── POP_AO_07_DONNAS      # Ogni PCN ha colore univoco
│   └── ... (42 PCN totali)
├── 🏛️ Aosta/                 # Cartella per comune
│   ├── Sede PAC/PAL #1       # Sedi con icona edificio governativo
│   └── Sede PAC/PAL #2       # Stesso colore del PCN di riferimento
├── 🏛️ Courmayeur/
└── ... (64 comuni totali)
```

### Mappature Integrate
- **74 Comuni Valle d'Aosta**: Codice ISTAT → Denominazione italiana
- **42 PCN OpenFiber**: ID PCN → Nome, Comune sede, Coordinate GPS
- **Join automatico**: Campo POP ↔ ID PCN per arricchimento dati
- **20 Colori KMZ**: Sistema rotativo per distinguere PCN visivamente

## 🔧 Configurazione

### GUI - Loghi Personalizzati
Per utilizzare i loghi aziendali nella GUI, aggiungi questi file in `data/`:
- **`logo_azienda.png`**: Logo della tua azienda (raccomandato: 50x50px, quadrato)
- **`logo_openfiber.png`**: Logo OpenFiber (manterrà proporzioni originali)

La GUI rileva automaticamente i loghi e li integra nell'header.

### Parametri Principali (`estrattore_of.py`)
```python
file_input = "data/dbcopertura_CD_20250715.csv"    # File CSV sorgente
file_output = "output/valle_aosta_estratto.xlsx"   # Output Excel (data aggiunta automaticamente) 🆕
chunk_size = 10000                                  # Righe per chunk (ottimizzazione memoria)
export_kmz = False                                  # Abilita export KMZ Google Earth 🆕
```

### File Configurazione (`config.py`)
```python
COMUNI_VALLE_AOSTA = { ... }    # 74 comuni con codici ISTAT
PCN_VALLE_AOSTA = { ... }       # 42 PCN con coordinate e info complete
FILTRI_COMUNI_VDA = { ... }     # Filtri predefiniti per analisi
```

## 🌍 Export KMZ per Google Earth 🆕

### Cosa Include
- **Solo sedi PAC/PAL**: Filtro automatico STATO_UI=302 (Pubblica Amministrazione)
- **Tutti i PCN**: 42 punti di connessione con coordinate precise
- **Colori coordinati**: Ogni PCN e le sue sedi hanno lo stesso colore
- **Icone differenziate**: Edifici governativi per sedi, telefoni per PCN

### Struttura Organizzata
- **Cartella principale**: Nome con data automatica
- **Cartella PCN**: Tutti i 42 PCN raggruppati
- **Cartelle comuni**: Un gruppo per ogni comune (fino a 64)

### Coordinate Support
- **Parsing automatico**: Formato OpenFiber `N45.123456_E7.123456`
- **Conversione Google Earth**: Longitudine, Latitudine, Altitudine
- **Validazione**: Skip automatico coordinate non valide con log

### Utilizzo
1. **GUI**: Spunta "🌍 Genera KMZ per Google Earth"
2. **Console**: Imposta `export_kmz=True` nella funzione main
3. **Output**: File `_PAC_PAL.kmz` creato automaticamente con data
4. **Google Earth**: Apri il file KMZ per visualizzazione cartografica

## 🎨 Caratteristiche GUI Avanzate

### Filtri Dati Intelligenti 🆕
- **🏛️ PAC/PAL [302]**: Solo sedi Pubblica Amministrazione
- **🏠 Residenziale [102]**: Solo abitazioni private
- **🔍 Personalizzato**: Combinazioni custom (es: "102,302", "200,201")
- **⚠️ Nota v2.1.1**: I filtri sono attualmente informativi (funzionalità complete in v2.2)

### Export Options 🆕
- **📊 Excel**: Sempre generato con data YYYYMMDD automatica
- **🌍 KMZ**: Opzionale per Google Earth (checkbox)
- **🆕 Naming automatico**: Rimozione campo nome file per semplificare UI

### Progress Tracking Live 🆕
- **Fasi dettagliate**: Lettura CSV → Estrazione → Arricchimento → Excel → KMZ
- **Logging ottimizzato**: Eliminazione duplicazioni, aggiornamenti PCN/comuni live
- **Statistiche real-time**: Record/sec, comuni trovati, PCN utilizzati

### Controlli Avanzati
- **📊 Anteprima**: Visualizza prime 10 righe CSV prima elaborazione
- **⚙️ Chunk size**: Slider regolabile per ottimizzazione memoria
- **🗑️ Reset**: Ripristina configurazione di default
- **📋 Codici STATO_UI**: Help integrato con tutti i codici documentati

## 🐛 Troubleshooting

### GUI Non Si Avvia
```bash
# Installa dipendenze GUI
pip install ttkbootstrap Pillow

# Se persiste, usa versione console
python estrattore_of.py
```

### Loghi Non Compaiono
- Verifica che i file siano in `data/logo_azienda.png` e `data/logo_openfiber.png`
- Formati supportati: PNG, JPG, BMP
- La GUI mostrerà fallback se i loghi non sono disponibili

### KMZ Non Funziona 🆕
- **Modulo non disponibile**: Verifica import `kmz_exporter.py`
- **Icone non visibili**: Le icone sono URL Google Maps (richiedono internet)
- **Coordinate invalide**: Controlla formato `N45.123_E7.456` in COORDINATE_BUILDING
- **File vuoto**: Verifica presenza sedi PAC/PAL (STATO_UI=302)

### Errori Comuni Console
- **File non trovato**: Verificare che il CSV sia in `data/`
- **Memory error**: Ridurre `chunk_size` da 10000 a 5000 nella GUI
- **Pandas/openpyxl non installato**: `pip install pandas openpyxl`

### File Grossi e Git
Il `.gitignore` esclude automaticamente:
- `data/` - File CSV di input e loghi (troppo grossi per Git)
- `output/` - File Excel e KMZ generati (risultati locali)
- `__pycache__/` - Cache Python

## 🚧 Roadmap Sviluppo

### Versione Attuale (v2.1.1) - ✅ Completata
- [x] Estrazione regione 02 (Valle d'Aosta) ottimizzata
- [x] Selezione colonne intelligente (16/25 colonne)
- [x] Mappatura completa comuni Valle d'Aosta
- [x] Integrazione dati PCN con coordinate GPS
- [x] Output Excel multi-foglio professionale
- [x] Formattazione avanzata e auto-resize
- [x] Performance monitoring e statistiche dettagliate
- [x] GUI moderna professionale con loghi personalizzati
- [x] Progress tracking live e stdout redirect
- [x] Filtri interattivi e anteprima dati
- [x] **Export KMZ per Google Earth** 🆕
- [x] **GUI fullscreen automatica** 🆕
- [x] **🆕 Data automatica nei filename**
- [x] **🆕 Icone Google Earth ottimizzate**
- [x] **🆕 Naming automatico e UI semplificata**
- [x] **🆕 Logging ottimizzato senza duplicazioni**
- [x] **🆕 Progress live fluido per PCN e comuni**

### Prossime Versioni
- [ ] **v2.2**: Integrazione filtri GUI → Core engine (filtri funzionali)
- [ ] **v2.3**: Export KMZ con filtri personalizzati
- [ ] **v2.4**: Supporto multiple regioni in un'unica elaborazione
- [ ] **v3.0**: Export formati aggiuntivi (CSV, JSON, GeoJSON)
- [ ] **v3.1**: Analisi statistiche avanzate e dashboard
- [ ] **v3.2**: Plugin system per filtri personalizzati
- [ ] **v4.0**: Servizio web interno con API REST

## 👥 Per Sviluppatori e AI

### Continuare lo Sviluppo
1. **Leggere questa documentazione** per capire architettura e funzionalità
2. **Analizzare `src/estrattore_of.py`** per logica di estrazione e formattazione
3. **Studiare `src/estrattore_of_GUI.py`** per interfaccia moderna
4. **Consultare `src/kmz_exporter.py`** per export Google Earth 🆕
5. **Consultare `src/config.py`** per mappature e configurazioni
6. **Verificare `docs/documentazione_tecnica.md`** per dettagli implementativi
7. **Testare modifiche** su file reali prima del commit

### Architettura Software
- **Core engine**: Estrazione chunked con state machine efficiente
- **GUI moderna**: ttkbootstrap + threading + queue per responsività
- **KMZ exporter**: Modulo dedicato per Google Earth con XML/KML 🆕
- **State management**: Queue separate per log e progress tracking
- **🆕 Stdout redirect ottimizzato**: Buffer per eliminare duplicazioni
- **🆕 Logo system**: PIL/Pillow con ridimensionamento proporzionale
- **Configurazione centralizzata**: Tutte le mappature in `config.py`

### Stack Tecnologico
- **Core**: Python 3.8+, pandas 2.x, openpyxl 3.x
- **GUI**: ttkbootstrap (Bootstrap themes), PIL/Pillow (loghi)
- **KMZ**: xml.etree.ElementTree, zipfile, minidom 🆕
- **Threading**: Queue-based per UI responsiva
- **Styling**: Tema "superhero" dark moderno

## 📞 Supporto e Documentazione
- **Repository**: https://github.com/MacPhisto666/AnalizzatoreDB-OF
- **Issues**: Usare GitHub Issues per bug e richieste feature
- **Documentazione tecnica**: `docs/documentazione_tecnica.md`
- **Configurazione**: `src/config.py` con commenti dettagliati

## 🎯 Casi d'Uso Principali
- **Analisi copertura per comune**: Ogni foglio Excel = analisi specifica
- **Pianificazione infrastrutturale**: Dati PCN con coordinate GPS
- **Visualizzazione cartografica**: File KMZ per Google Earth 🆕
- **Reporting**: Statistiche automatiche per comune e PCN
- **Controllo qualità**: Verifica coverage e dati mancanti
- **Analisi geografica**: Coordinate edifici e PCN per mapping
- **Presentazioni**: GUI professionale per demo clienti
- **Sopralluoghi**: Export KMZ per navigazione GPS 🆕

## 🏆 Crediti
**💻 Powered by McPhisto with Claude 🤖**

Sviluppato con passione per l'analisi dati infrastrutturali e l'automazione intelligente.

---
*Ultima modifica: 2025-01-28 - v2.1.1 Logging ottimizzato, naming automatico e UI semplificata*