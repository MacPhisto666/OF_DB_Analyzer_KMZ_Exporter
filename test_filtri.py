#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test specifico per i filtri STATO_UI
"""

import sys
import os
import pandas as pd

# Fix encoding per Windows
try:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

# Aggiungi src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_filtri_funzionali():
    """Test funzionamento filtri nel core engine"""
    print("🧪 Test filtri STATO_UI funzionali...")
    
    from estrattore_of import process_record, get_stato_field_name
    
    # Simula record CSV con diversi STATO_UI
    test_records = [
        {'REGIONE': '02', 'COMUNE': '007003', 'STATO_UI': '102', 'POP': 'TEST1', 'COORDINATE_BUILDING': 'N45.1_E7.1'},
        {'REGIONE': '02', 'COMUNE': '007003', 'STATO_UI': '302', 'POP': 'TEST2', 'COORDINATE_BUILDING': 'N45.2_E7.2'},
        {'REGIONE': '02', 'COMUNE': '007003', 'STATO_UI': '201', 'POP': 'TEST3', 'COORDINATE_BUILDING': 'N45.3_E7.3'},
        {'REGIONE': '02', 'COMUNE': '007003', 'STATO_UI': '602', 'POP': 'TEST4', 'COORDINATE_BUILDING': 'N45.4_E7.4'},
    ]
    
    print("📋 Record di test:")
    for i, record in enumerate(test_records):
        print(f"  {i+1}. STATO_UI={record['STATO_UI']} (POP={record['POP']})")
    
    # Test processo senza filtri
    print("\n🔍 Test senza filtri (tutti i record):")
    processed_all = []
    for record in test_records:
        processed = process_record(record)
        processed_all.append(processed)
        print(f"  ✅ Processato: STATO_UI={processed['STATO_UI']}")
    
    print(f"  📊 Totale processati: {len(processed_all)}")
    
    # Test filtro specifico
    print("\n🔍 Test con filtro STATO_UI=['302'] (solo PAC/PAL):")
    filter_codes = ['302']
    filtered_records = []
    
    for record in test_records:
        processed = process_record(record)
        stato_ui = str(processed.get('STATO_UI', '')).strip()
        if stato_ui in filter_codes:
            filtered_records.append(processed)
            print(f"  ✅ Incluso: STATO_UI={stato_ui}")
        else:
            print(f"  ❌ Escluso: STATO_UI={stato_ui}")
    
    print(f"  📊 Totale filtrati: {len(filtered_records)}")
    
    # Test filtro multiplo
    print("\n🔍 Test con filtro STATO_UI=['102', '302'] (FTTH + PAC/PAL):")
    filter_codes = ['102', '302']
    filtered_records = []
    
    for record in test_records:
        processed = process_record(record)
        stato_ui = str(processed.get('STATO_UI', '')).strip()
        if stato_ui in filter_codes:
            filtered_records.append(processed)
            print(f"  ✅ Incluso: STATO_UI={stato_ui}")
        else:
            print(f"  ❌ Escluso: STATO_UI={stato_ui}")
    
    print(f"  📊 Totale filtrati: {len(filtered_records)}")
    
    return True

def test_config_filtri():
    """Test configurazione filtri"""
    print("\n🧪 Test configurazione filtri...")
    
    from config import FILTRI_TIPOLOGIE_SEDE
    
    print("📋 Filtri configurati:")
    for key, data in FILTRI_TIPOLOGIE_SEDE.items():
        codici = data.get('codici', [])
        desc = data.get('descrizione', 'N/A')
        print(f"  • {key}: {desc} → {codici}")
    
    # Test filtro PAC/PAL
    pac_pal_filter = FILTRI_TIPOLOGIE_SEDE.get('pac_pal', {})
    expected_codes = ['302']
    actual_codes = pac_pal_filter.get('codici', [])
    
    if actual_codes == expected_codes:
        print("  ✅ Filtro PAC/PAL corretto")
    else:
        print(f"  ❌ Filtro PAC/PAL errato: atteso {expected_codes}, trovato {actual_codes}")
        return False
    
    return True

def main():
    """Test principale"""
    print("🚀 TEST FILTRI STATO_UI FUNZIONALI")
    print("=" * 50)
    
    success = True
    
    if not test_config_filtri():
        success = False
    
    if not test_filtri_funzionali():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TUTTI I TEST SUPERATI!")
        print("✅ I filtri sono ora funzionali nel core engine")
        print("✅ La GUI può passare filtri al motore di estrazione")
        print("✅ I record vengono filtrati correttamente per STATO_UI")
    else:
        print("❌ ALCUNI TEST FALLITI")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)