"""
Test completo integrazione export KMZ
Verifica funzionamento modulo KMZ con dati realistici
"""

import pandas as pd
import os
import sys
from datetime import datetime

# Aggiungi src al path se necessario
sys.path.insert(0, 'src')

try:
    from kmz_exporter import KMZExporter, genera_kmz_pac_pal
    from config import PCN_VALLE_AOSTA, COMUNI_VALLE_AOSTA
    print("✅ Import moduli completati")
except ImportError as e:
    print(f"❌ Errore import: {e}")
    sys.exit(1)

def create_test_data():
    """Crea dataset di test realistico"""
    test_data = []
    
    # Dati di test per diverse sedi PAC/PAL
    sedi_test = [
        {
            'COMUNE': 'Aosta',
            'ISTAT': '007003',
            'INDIRIZZO': 'Piazza Chanoux',
            'CIVICO': '1',
            'ID_BUILDING': 'AO_MUNICIPIO_001',
            'COORDINATE_BUILDING': 'N45.737649_E7.320166',
            'STATO_UI': '302',  # PAC/PAL
            'POP': 'AOCUA',
            'NOME_PCN': 'POP_AO_11_VERRES'
        },
        {
            'COMUNE': 'Aosta',
            'ISTAT': '007003',
            'INDIRIZZO': 'Via Festaz',
            'CIVICO': '15',
            'ID_BUILDING': 'AO_SCUOLA_002',
            'COORDINATE_BUILDING': 'N45.734521_E7.325789',
            'STATO_UI': '302',  # PAC/PAL
            'POP': 'AOCUA',
            'NOME_PCN': 'POP_AO_11_VERRES'
        },
        {
            'COMUNE': 'Verrès',
            'ISTAT': '007073',
            'INDIRIZZO': 'Via Roma',
            'CIVICO': '10',
            'ID_BUILDING': 'VR_MUNICIPIO_001',
            'COORDINATE_BUILDING': 'N45.661442_E7.691030',
            'STATO_UI': '302',  # PAC/PAL
            'POP': 'AOAGA',
            'NOME_PCN': 'POP_AO_07_DONNAS'
        },
        {
            'COMUNE': 'Courmayeur',
            'ISTAT': '007022',
            'INDIRIZZO': 'Piazza Abbé Henry',
            'CIVICO': '2',
            'ID_BUILDING': 'CM_MUNICIPIO_001',
            'COORDINATE_BUILDING': 'N45.796638_E6.968169',
            'STATO_UI': '302',  # PAC/PAL
            'POP': 'AOBOA',
            'NOME_PCN': 'POP_AO_13_LA_THUILE'
        },
        {
            'COMUNE': 'Saint-Vincent',
            'ISTAT': '007065',
            'INDIRIZZO': 'Via Roma',
            'CIVICO': '62',
            'ID_BUILDING': 'SV_OSPEDALE_001',
            'COORDINATE_BUILDING': 'N45.748899_E7.647321',
            'STATO_UI': '302',  # PAC/PAL
            'POP': 'AOCGA',
            'NOME_PCN': 'POP_AO_49_SAINT_DENIS'
        },
        # Aggiungi alcuni dati non PAC/PAL per test
        {
            'COMUNE': 'Aosta',
            'ISTAT': '007003',
            'INDIRIZZO': 'Via Testbed',
            'CIVICO': '100',
            'ID_BUILDING': 'AO_RESID_001',
            'COORDINATE_BUILDING': 'N45.740000_E7.330000',
            'STATO_UI': '102',  # Residenziale - non dovrebbe apparire in KMZ
            'POP': 'AOCUA',
            'NOME_PCN': 'POP_AO_11_VERRES'
        }
    ]
    
    return pd.DataFrame(sedi_test)

def test_coordinate_parsing():
    """Test parsing coordinate"""
    print("\n🧪 Test parsing coordinate...")
    
    exporter = KMZExporter()
    
    test_coords = [
        ('N45.737649_E7.320166', (7.320166, 45.737649, 0)),
        ('N45.661442_E7.691030', (7.691030, 45.661442, 0)),
        ('S12.345_W67.890', (-67.890, -12.345, 0)),
        ('INVALID_COORD', None),
        ('', None),
        (None, None)
    ]
    
    for input_coord, expected in test_coords:
        result = exporter.parse_coordinates(input_coord)
        print(f"  '{input_coord}' → {result}")
        
        if expected is None:
            assert result is None, f"Expected None, got {result}"
        else:
            assert result == expected, f"Expected {expected}, got {result}"
    
    print("✅ Test coordinate parsing OK")

def test_pcn_colors():
    """Test assegnazione colori PCN"""
    print("\n🎨 Test assegnazione colori PCN...")
    
    exporter = KMZExporter()
    
    print(f"📊 PCN totali in config: {len(PCN_VALLE_AOSTA)}")
    print(f"🎨 Colori disponibili: {len(exporter.pcn_colors)}")
    print(f"🎯 Colori assegnati: {len(exporter.pcn_color_map)}")
    
    # Verifica che tutti i PCN abbiano un colore
    for pcn_id in PCN_VALLE_AOSTA.keys():
        assert pcn_id in exporter.pcn_color_map, f"PCN {pcn_id} senza colore"
    
    # Mostra alcuni esempi
    esempi = list(exporter.pcn_color_map.items())[:5]
    for pcn_id, color in esempi:
        print(f"  {pcn_id}: {color}")
    
    print("✅ Test colori PCN OK")

def test_kmz_generation():
    """Test generazione KMZ completa"""
    print("\n🌍 Test generazione KMZ...")
    
    # Crea dati di test
    df_test = create_test_data()
    print(f"📊 Dataset test: {len(df_test)} record")
    print(f"🏛️ Sedi PAC/PAL: {len(df_test[df_test['STATO_UI'] == '302'])}")
    
    # File output
    output_file = "test_pac_pal.kmz"
    
    try:
        # Genera KMZ
        success = genera_kmz_pac_pal(df_test, output_file)
        
        if success and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"✅ KMZ generato: {output_file} ({file_size} bytes)")
            
            # Cleanup
            os.remove(output_file)
            print("🗑️ File test rimosso")
            
            return True
        else:
            print("❌ KMZ non generato correttamente")
            return False
            
    except Exception as e:
        print(f"❌ Errore test KMZ: {e}")
        return False

def test_data_filtering():
    """Test filtro dati PAC/PAL"""
    print("\n🔍 Test filtro dati...")
    
    df_test = create_test_data()
    
    # Verifica dati originali
    print(f"📊 Record totali: {len(df_test)}")
    print(f"🏛️ Sedi PAC/PAL (302): {len(df_test[df_test['STATO_UI'] == '302'])}")
    print(f"🏠 Sedi residenziali (102): {len(df_test[df_test['STATO_UI'] == '102'])}")
    
    # Filtro solo PAC/PAL
    df_pac_pal = df_test[df_test['STATO_UI'] == '302']
    
    # Verifica filtro
    assert len(df_pac_pal) == 5, f"Expected 5 PAC/PAL, got {len(df_pac_pal)}"
    assert all(df_pac_pal['STATO_UI'] == '302'), "Filtro PAC/PAL non corretto"
    
    print("✅ Test filtro dati OK")

def test_pcn_uniqueness():
    """Test unicità PCN in KMZ"""
    print("\n📡 Test unicità PCN...")
    
    df_test = create_test_data()
    df_pac_pal = df_test[df_test['STATO_UI'] == '302']
    
    # PCN univoci nei dati
    pcn_unici = df_pac_pal['POP'].unique()
    print(f"📊 PCN unici nei dati: {len(pcn_unici)}")
    for pcn in pcn_unici:
        count = len(df_pac_pal[df_pac_pal['POP'] == pcn])
        pcn_name = PCN_VALLE_AOSTA.get(pcn, {}).get('nome', 'Sconosciuto')
        print(f"  {pcn} ({pcn_name}): {count} sedi")
    
    print("✅ Test unicità PCN OK")

def run_all_tests():
    """Esegue tutti i test"""
    print("🧪 AVVIO TEST SUITE KMZ")
    print("=" * 50)
    
    tests = [
        test_coordinate_parsing,
        test_pcn_colors,
        test_data_filtering,
        test_pcn_uniqueness,
        test_kmz_generation
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__} FALLITO: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 RISULTATI TEST: {passed} ✅ | {failed} ❌")
    
    if failed == 0:
        print("🎉 Tutti i test sono passati!")
        return True
    else:
        print("⚠️ Alcuni test sono falliti")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
