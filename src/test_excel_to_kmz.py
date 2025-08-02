"""
Test Excel → KMZ - VERSIONE PULITA RIGENERATA
Converte il file Excel reale in KMZ per Google Earth
"""

import pandas as pd
import os
import sys
from datetime import datetime

# Aggiungi src al path se necessario
if os.path.exists('src'):
    sys.path.insert(0, 'src')

try:
    from kmz_exporter import genera_kmz_pac_pal
    print("✅ Modulo KMZ importato")
except ImportError as e:
    print(f"❌ Errore import KMZ: {e}")
    sys.exit(1)

def trova_excel():
    """Trova il file Excel nelle posizioni più probabili"""
    posizioni = [
        "output/valle_aosta_estratto.xlsx",         # Root progetto
        "../output/valle_aosta_estratto.xlsx",      # Da src/
        "./valle_aosta_estratto.xlsx",              # Directory corrente
        "valle_aosta_estratto.xlsx"                 # Senza path
    ]
    
    print("🔍 Ricerca file Excel...")
    for path in posizioni:
        if os.path.exists(path):
            print(f"✅ Trovato: {os.path.abspath(path)}")
            return path
        
    print("❌ File Excel non trovato!")
    print("📂 Directory corrente:", os.getcwd())
    return None

def analizza_stato_ui(df):
    """Analizza STATO_UI e trova il metodo migliore per filtrare PAC/PAL"""
    print("\n🔍 ANALISI STATO_UI")
    print("=" * 40)
    
    print(f"📊 Record totali: {len(df):,}")
    print(f"📋 Tipo STATO_UI: {df['STATO_UI'].dtype}")
    
    # Mostra distribuzione
    stati = df['STATO_UI'].value_counts().head(10)
    print(f"\n📈 Distribuzione STATO_UI:")
    for stato, count in stati.items():
        print(f"  {stato}: {count:,} record")
    
    # Test filtri per 302
    metodi = {
        "== 302 (int)": df['STATO_UI'] == 302,
        "== '302' (str)": df['STATO_UI'] == '302',
        "astype(str) == '302'": df['STATO_UI'].astype(str) == '302'
    }
    
    print(f"\n🧪 Test filtri per PAC/PAL (302):")
    migliore = None
    max_risultati = 0
    
    for nome, filtro in metodi.items():
        try:
            count = filtro.sum()
            print(f"  {nome}: {count:,} record")
            
            if count > max_risultati:
                max_risultati = count
                migliore = filtro
        except Exception as e:
            print(f"  {nome}: ❌ Errore - {e}")
    
    print(f"\n✅ Record PAC/PAL trovati: {max_risultati:,}")
    return migliore

def main():
    """Funzione principale"""
    print("🧪 TEST EXCEL → KMZ REALE")
    print("=" * 50)
    
    # 1. Trova Excel
    excel_file = trova_excel()
    if not excel_file:
        print("💡 Assicurati di aver generato l'Excel con la GUI")
        return False
    
    # 2. Leggi Excel
    print(f"\n📖 Lettura Excel: {excel_file}")
    try:
        fogli = pd.read_excel(excel_file, sheet_name=None)
        print(f"📋 Fogli trovati: {len(fogli)}")
        
        # Unisci tutti i fogli
        tutti_dati = []
        for nome, dati in fogli.items():
            tutti_dati.append(dati)
        
        df_completo = pd.concat(tutti_dati, ignore_index=True)
        print(f"✅ Record totali: {len(df_completo):,}")
        
    except Exception as e:
        print(f"❌ Errore lettura Excel: {e}")
        return False
    
    # 3. Verifica colonne
    colonne_necessarie = ['STATO_UI', 'COMUNE', 'ID_BUILDING', 'COORDINATE_BUILDING', 'POP']
    mancanti = [col for col in colonne_necessarie if col not in df_completo.columns]
    
    if mancanti:
        print(f"❌ Colonne mancanti: {mancanti}")
        return False
    
    print("✅ Colonne necessarie presenti")
    
    # 4. Analizza e filtra PAC/PAL
    filtro_pac_pal = analizza_stato_ui(df_completo)
    if filtro_pac_pal is None:
        print("❌ Impossibile trovare PAC/PAL")
        return False
    
    df_pac_pal = df_completo[filtro_pac_pal].copy()
    print(f"\n🏛️ Sedi PAC/PAL filtrate: {len(df_pac_pal):,}")
    
    if len(df_pac_pal) == 0:
        print("❌ Nessuna sede PAC/PAL dopo filtro!")
        return False
    
    # Mostra distribuzione per comune
    comuni = df_pac_pal['COMUNE'].value_counts().head(10)
    print(f"\n📊 Top 10 comuni con più sedi PAC/PAL:")
    for comune, count in comuni.items():
        print(f"  🏛️ {comune}: {count} sedi")
    
    # 5. Genera KMZ
    print(f"\n🌍 GENERAZIONE KMZ")
    print("=" * 30)
    
    # Determina directory output
    if excel_file.startswith("output/"):
        dir_output = "output"
    else:
        dir_output = os.path.dirname(excel_file) or "."
    
    os.makedirs(dir_output, exist_ok=True)
    
    # Nome file con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_kmz = os.path.join(dir_output, f"valle_aosta_PAC_PAL_{timestamp}.kmz")
    
    print(f"📦 File KMZ: {file_kmz}")
    print(f"🗂️ Path assoluto: {os.path.abspath(file_kmz)}")
    
    # Genera KMZ (passa DataFrame già filtrato)
    try:
        print(f"🏛️ Sedi da processare: {len(df_pac_pal):,}")
        
        successo = genera_kmz_pac_pal(df_pac_pal, file_kmz)
        
        if successo and os.path.exists(file_kmz):
            dimensione = os.path.getsize(file_kmz) / 1024
            
            print(f"\n🎉 KMZ GENERATO CON SUCCESSO!")
            print(f"📦 File: {os.path.basename(file_kmz)}")
            print(f"📏 Dimensione: {dimensione:.1f} KB")
            print(f"🏛️ Sedi incluse: {len(df_pac_pal):,}")
            print(f"🗂️ Posizione: {file_kmz}")
            print(f"\n🌍 APRI IL FILE IN GOOGLE EARTH!")
            
            # Verifica contenuto directory
            print(f"\n📁 File nella directory output:")
            try:
                files = [f for f in os.listdir(dir_output) if f.endswith(('.kmz', '.xlsx'))]
                for file in sorted(files):
                    size = os.path.getsize(os.path.join(dir_output, file)) / 1024
                    print(f"  📄 {file} ({size:.1f} KB)")
            except:
                pass
            
            return True
        else:
            print(f"\n❌ KMZ non generato correttamente")
            return False
            
    except Exception as e:
        print(f"\n❌ Errore generazione KMZ: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        successo = main()
        
        print("\n" + "=" * 50)
        if successo:
            print("🎉 SUCCESSO! KMZ generato correttamente!")
        else:
            print("❌ FALLITO! Controlla gli errori sopra")
            
    except KeyboardInterrupt:
        print("\n⏹️ Interrotto dall'utente")
    except Exception as e:
        print(f"\n💥 Errore imprevisto: {e}")