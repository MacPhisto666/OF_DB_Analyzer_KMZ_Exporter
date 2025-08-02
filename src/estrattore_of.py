"""
Estrattore OpenFiber v2.1.1 - Core Engine con supporto export KMZ
Aggiornato per compatibilità con export KMZ Google Earth e nome file automatico
"""

import pandas as pd
import os
import time
from datetime import datetime

# Import configurazioni 2
from config import COMUNI_VALLE_AOSTA, PCN_VALLE_AOSTA

# Import export KMZ (opzionale)
try:
    from kmz_exporter import genera_kmz_pac_pal
    KMZ_SUPPORT = True
except ImportError:
    KMZ_SUPPORT = False
    print("ℹ️ Modulo KMZ non disponibile - export KMZ disabilitato")

# Colonne da mantenere nell'output finale
COLONNE_OUTPUT = [
    'COMUNE',  # → Verrà trasformato in nome italiano
    'PARTICELLA_TOP',
    'INDIRIZZO', 
    'CIVICO',
    'ID_BUILDING',
    'COORDINATE_BUILDING',  # Importante per KMZ
    'STATO_UI',
    'POP',  # Importante per mapping PCN
    'TOTALE_UI',
    'DATA_ULTIMA_MODIFICA_RECORD',
    'DATA_ULTIMA_VARIAZIONE_STATO_BUILDING'
]

# Nomi alternativi per il campo stato (per retrocompatibilità)
STATO_FIELD_NAMES = ['STATO_UI', 'STATO_BUILDING']

def get_stato_field_name(columns):
    """Determina quale campo stato è disponibile nel CSV"""
    for field_name in STATO_FIELD_NAMES:
        if field_name in columns:
            return field_name
    return 'STATO_UI'  # Default fallback

def process_record(row, stato_field_name='STATO_UI'):
    """
    Arricchisce un record CSV con dati da mappature esterne
    Versione aggiornata per supporto KMZ e campo STATO_BUILDING
    
    Args:
        row: Riga CSV da processare
        stato_field_name: Nome del campo stato (STATO_UI o STATO_BUILDING)
    """
    # Record base con colonne selezionate
    record_filtrato = {}
    for col in COLONNE_OUTPUT:
        if col == 'COMUNE':  # Gestito separatamente
            continue
        elif col == 'STATO_UI':
            # Usa il campo stato corretto (STATO_UI o STATO_BUILDING)
            record_filtrato[col] = row[stato_field_name] if stato_field_name in row else ''
        else:
            record_filtrato[col] = row[col] if col in row else ''
    
    # Enrichment 1: Mapping Comune (ISTAT → Nome italiano)
    codice_comune = str(row['COMUNE']).strip()
    nome_comune = COMUNI_VALLE_AOSTA.get(
        codice_comune, 
        f'Comune sconosciuto ({codice_comune})'
    )
    
    # Enrichment 2: Mapping PCN (ID → Informazioni complete)
    id_pcn = str(row['POP']).strip()
    pcn_info = PCN_VALLE_AOSTA.get(id_pcn, {})
    
    # Record finale arricchito (formato compatibile KMZ)
    record_arricchito = {
        'COMUNE': nome_comune,
        'ISTAT': codice_comune,  # Mantieni codice originale
        'PARTICELLA_TOP': record_filtrato['PARTICELLA_TOP'],
        'INDIRIZZO': record_filtrato['INDIRIZZO'],
        'CIVICO': record_filtrato['CIVICO'],
        'ID_BUILDING': record_filtrato['ID_BUILDING'],
        'COORDINATE_BUILDING': record_filtrato['COORDINATE_BUILDING'],
        'STATO_UI': record_filtrato['STATO_UI'],
        'POP': id_pcn,
        'NOME_PCN': pcn_info.get('nome', f'PCN sconosciuto ({id_pcn})'),
        'COMUNE_PCN': pcn_info.get('comune', 'Comune PCN sconosciuto'),
        'LAT_PCN': pcn_info.get('latitudine', ''),
        'LON_PCN': pcn_info.get('longitudine', ''),
        'TOTALE_UI': record_filtrato['TOTALE_UI'],
        'DATA_ULTIMA_MODIFICA_RECORD': record_filtrato['DATA_ULTIMA_MODIFICA_RECORD'],
        'DATA_ULTIMA_VARIAZIONE_STATO_BUILDING': record_filtrato['DATA_ULTIMA_VARIAZIONE_STATO_BUILDING']
    }
    
    return record_arricchito

def sanitize_sheet_name(name):
    """
    Converte nomi comuni in nomi fogli Excel validi
    """
    # Excel limits: 31 chars, no special chars
    name = str(name)[:31]
    invalid_chars = ['/', '\\', '?', '*', '[', ']', ':']
    for char in invalid_chars:
        name = name.replace(char, '-' if char in ['/', '\\', ':'] else '')
    return name

def apply_professional_formatting(worksheet):
    """
    Applica formattazione professionale al foglio Excel
    """
    from openpyxl.styles import Border, Side, Alignment
    
    # Definizione stili
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    center_alignment = Alignment(horizontal='center', vertical='center')
    
    # Applica bordi e allineamento a tutte le celle con dati
    for row in worksheet.iter_rows():
        for cell in row:
            if cell.value is not None:
                cell.border = thin_border
                cell.alignment = center_alignment
    
    # Auto-resize colonne intelligente
    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        
        for cell in column:
            try:
                cell_length = len(str(cell.value))
                if cell_length > max_length:
                    max_length = cell_length
            except:
                pass
        
        # Imposta larghezza con vincoli min/max
        adjusted_width = min(max(max_length + 2, 10), 50)
        worksheet.column_dimensions[column_letter].width = adjusted_width

def generate_multisheet_excel(df_valle_aosta, file_output):
    """
    Genera file Excel multi-foglio con formattazione professionale
    Versione ottimizzata per grandi dataset
    """
    print(f"📊 Generazione Excel multi-foglio: {len(df_valle_aosta)} record")
    
    # Ordinamento per comune
    df_valle_aosta = df_valle_aosta.sort_values('COMUNE')
    
    # Raggruppamento per comune
    comuni_groups = df_valle_aosta.groupby('COMUNE')
    print(f"🏘️ Trovati {len(comuni_groups)} comuni")
    
    # Generazione Excel con writer
    with pd.ExcelWriter(file_output, engine='openpyxl') as writer:
        comuni_processati = 0
        
        for comune_nome, gruppo_data in comuni_groups:
            # Nome foglio Excel-safe
            nome_foglio = sanitize_sheet_name(comune_nome)
            
            # Scrivi dati nel foglio
            gruppo_data.to_excel(writer, sheet_name=nome_foglio, index=False)
            
            # Applica formattazione professionale
            worksheet = writer.sheets[nome_foglio]
            apply_professional_formatting(worksheet)
            
            comuni_processati += 1
            
            # Progress ogni 10 comuni
            if comuni_processati % 10 == 0:
                print(f"  📄 Processati {comuni_processati}/{len(comuni_groups)} fogli")
        
        print(f"✅ Excel generato: {comuni_processati} fogli")

def estrai_regione_02(file_input="data/dbcopertura_CD_20250715.csv", 
                     file_output="output/valle_aosta_estratto.xlsx", 
                     chunk_size=10000,
                     export_kmz=False,
                     filter_state_codes=None):
    """
    Estrae dati regione 02 (Valle d'Aosta) con supporto export KMZ opzionale e filtri STATO_UI
    VERSIONE AGGIORNATA v2.1.1 con nome file automatico e filtri funzionali
    
    Args:
        file_input: Path file CSV di input
        file_output: Path file Excel di output (verrà aggiunta data automaticamente)
        chunk_size: Dimensione chunk per ottimizzazione memoria
        export_kmz: Se True, genera anche file KMZ per Google Earth
        filter_state_codes: Lista di codici STATO_UI da filtrare (es. ['102', '302'])
                           Se None, estrae tutti i record
    
    Returns:
        bool: True se successo, False se errore
    """
    print("=" * 60)
    print("🚀 ANALIZZATORE DB OPENFIBER v2.1.1")
    print("📍 Estrazione Regione 02 - Valle d'Aosta")
    print("=" * 60)
    
    start_time = time.time()
    
    # === AGGIUNTA DATA AUTOMATICA AL FILENAME ===
    output_dir = os.path.dirname(file_output)
    output_name = os.path.basename(file_output)
    name_without_ext = os.path.splitext(output_name)[0]
    
    # Genera nome con data automatica
    data_oggi = datetime.now().strftime("%Y%m%d")
    new_filename = f"{name_without_ext}_{data_oggi}.xlsx"
    file_output_final = os.path.join(output_dir, new_filename)
    
    # === VALIDAZIONE INPUT ===
    if not os.path.exists(file_input):
        print(f"❌ ERRORE: File {file_input} non trovato!")
        return False
    
    # Creazione directory output
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 File input: {file_input}")
    print(f"📂 File output: {file_output_final}")
    print(f"⚙️ Chunk size: {chunk_size:,} righe")
    
    # Informazioni sui filtri
    if filter_state_codes:
        print(f"🔍 Filtro STATO_UI attivo: {filter_state_codes}")
        from config import STATI_UI
        for code in filter_state_codes:
            desc = STATI_UI.get(code, 'Sconosciuto')
            print(f"  • {code}: {desc}")
    else:
        print("📋 Nessun filtro - tutti i record saranno estratti")
    
    if export_kmz:
        if KMZ_SUPPORT:
            print("🌍 Export KMZ: Abilitato")
        else:
            print("⚠️ Export KMZ: Richiesto ma modulo non disponibile")
            export_kmz = False
    
    print("-" * 60)
    
    # === CHUNKED READING ===
    try:
        chunk_iterator = pd.read_csv(
            file_input,
            sep='|',
            chunksize=chunk_size,
            dtype=str,
            low_memory=False
        )
        
        # Leggi il primo chunk per determinare il nome del campo stato
        first_chunk = next(iter(pd.read_csv(
            file_input,
            sep='|',
            chunksize=1,
            dtype=str,
            low_memory=False
        )))
        
        stato_field_name = get_stato_field_name(first_chunk.columns)
        print(f"📋 Campo stato rilevato: {stato_field_name}")
        
        # Ricrea l'iteratore (il primo è stato consumato)
        chunk_iterator = pd.read_csv(
            file_input,
            sep='|',
            chunksize=chunk_size,
            dtype=str,
            low_memory=False
        )
        
    except Exception as e:
        print(f"❌ Errore lettura CSV: {e}")
        return False
    
    # === STATE MACHINE EXTRACTION ===
    valle_aosta_data = []
    found_start = False
    found_end = False
    total_rows_processed = 0
    start_row = 0
    end_row = 0
    
    print("🔍 Ricerca dati Valle d'Aosta...")
    
    for chunk_num, chunk in enumerate(chunk_iterator):
        # Progress tracking
        if chunk_num % 10 == 0:
            print(f"📊 Chunk {chunk_num + 1:,} - Righe totali: {total_rows_processed:,}")
        
        for idx, row in chunk.iterrows():
            total_rows_processed += 1
            regione = str(row['REGIONE']).strip()
            
            # State machine logic
            if not found_start and regione == '02':
                found_start = True
                start_row = total_rows_processed
                print(f"✅ Trovato INIZIO Valle d'Aosta alla riga {start_row:,}")
            
            if found_start:
                if regione == '02':
                    # Processa e arricchisce record con campo stato corretto
                    record_arricchito = process_record(row, stato_field_name)
                    
                    # Applica filtro STATO_UI se specificato
                    if filter_state_codes is None:
                        # Nessun filtro - aggiungi tutti i record
                        valle_aosta_data.append(record_arricchito)
                    else:
                        # Controlla se il record soddisfa il filtro
                        stato_ui = str(record_arricchito.get('STATO_UI', '')).strip()
                        if stato_ui in filter_state_codes:
                            valle_aosta_data.append(record_arricchito)
                        # Record filtrato - non viene aggiunto
                    
                    # Progress estrazione
                    if len(valle_aosta_data) % 1000 == 0:
                        print(f"  📋 Record estratti: {len(valle_aosta_data):,}")
                else:
                    found_end = True
                    end_row = total_rows_processed
                    print(f"🏁 Trovata FINE Valle d'Aosta alla riga {end_row:,}")
                    break
        
        if found_end:
            break
    
    # === RISULTATI ESTRAZIONE ===
    if not valle_aosta_data:
        print("❌ Nessun dato Valle d'Aosta trovato!")
        return False
    
    print(f"✅ Estrazione completata: {len(valle_aosta_data):,} record")
    print(f"📊 Range righe: {start_row:,} - {end_row:,}")
    
    # === CONVERSIONE DATAFRAME ===
    df_valle_aosta = pd.DataFrame(valle_aosta_data)
    print(f"📋 DataFrame creato: {len(df_valle_aosta)} righe x {len(df_valle_aosta.columns)} colonne")
    
    # === GENERAZIONE EXCEL ===
    print("\n📊 Generazione file Excel multi-foglio...")
    try:
        generate_multisheet_excel(df_valle_aosta, file_output_final)
        excel_size = os.path.getsize(file_output_final) / (1024 * 1024)  # MB
        print(f"💾 Excel salvato: {file_output_final} ({excel_size:.1f} MB)")
    except Exception as e:
        print(f"❌ Errore generazione Excel: {e}")
        return False
    
    # === EXPORT KMZ (OPZIONALE) ===
    kmz_success = True
    
    if export_kmz and KMZ_SUPPORT:
        print("\n🌍 Generazione file KMZ per Google Earth...")
        try:
            # Nome file KMZ basato sul file Excel finale
            base_name = os.path.splitext(file_output_final)[0]
            kmz_file = f"{base_name}_PAC_PAL.kmz"
            
            # Genera KMZ
            kmz_success = genera_kmz_pac_pal(df_valle_aosta, kmz_file)
            
            if kmz_success:
                kmz_size = os.path.getsize(kmz_file) / 1024  # KB
                print(f"💾 KMZ salvato: {kmz_file} ({kmz_size:.1f} KB)")
            else:
                print("❌ Errore generazione KMZ")
                
        except Exception as e:
            print(f"❌ Errore export KMZ: {e}")
            kmz_success = False
    
    # === STATISTICHE FINALI ===
    elapsed_time = time.time() - start_time
    comuni_unici = df_valle_aosta['COMUNE'].nunique()
    pcn_unici = df_valle_aosta['POP'].nunique()
    
    print("\n" + "=" * 60)
    print("📈 STATISTICHE FINALI")
    print("=" * 60)
    print(f"⏱️  Tempo elaborazione: {elapsed_time:.1f} secondi")
    print(f"📋 Record estratti: {len(valle_aosta_data):,}")
    print(f"🏘️  Comuni trovati: {comuni_unici}")
    print(f"📡 PCN utilizzati: {pcn_unici}")
    print(f"⚡ Velocità: {len(valle_aosta_data)/elapsed_time:,.0f} record/secondo")
    print(f"📊 File Excel: {file_output_final}")
    
    if export_kmz and kmz_success:
        base_name = os.path.splitext(file_output_final)[0]
        kmz_file = f"{base_name}_PAC_PAL.kmz"
        print(f"🌍 File KMZ: {kmz_file}")
    elif export_kmz:
        print("⚠️  KMZ: Errore durante generazione")
    
    print("✅ Elaborazione completata con successo!")
    print("=" * 60)
    
    return True

def main():
    """Funzione principale per esecuzione standalone"""
    # Configurazione default
    file_input = "data/dbcopertura_CD_20250715.csv"
    file_output = "output/valle_aosta_estratto.xlsx"  # Data aggiunta automaticamente
    chunk_size = 10000
    
    # Esecuzione con export KMZ abilitato per test
    result = estrai_regione_02(
        file_input=file_input,
        file_output=file_output, 
        chunk_size=chunk_size,
        export_kmz=True  # Abilitato per test KMZ
    )
    
    if result:
        print("\n🎉 Estrazione completata con successo!")
    else:
        print("\n❌ Estrazione fallita!")

if __name__ == "__main__":
    main()