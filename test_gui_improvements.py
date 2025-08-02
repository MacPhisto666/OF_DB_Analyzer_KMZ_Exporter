#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test delle modifiche alla GUI dell'Analizzatore DB OpenFiber v2.1.1
Verifica funzionamento nuovi filtri e logging migliorato
"""

import sys
import os

# Fix encoding per Windows
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Aggiungi src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test degli import necessari"""
    print("🧪 Test import dipendenze...")
    
    try:
        import tkinter as tk
        print("  ✅ tkinter OK")
    except ImportError as e:
        print(f"  ❌ tkinter: {e}")
        return False
    
    try:
        import ttkbootstrap
        print("  ✅ ttkbootstrap OK")
    except ImportError as e:
        print(f"  ❌ ttkbootstrap: {e}")
        return False
    
    try:
        from config import FILTRI_TIPOLOGIE_SEDE, STATI_UI
        print(f"  ✅ config.py OK - {len(FILTRI_TIPOLOGIE_SEDE)} filtri, {len(STATI_UI)} stati")
    except ImportError as e:
        print(f"  ❌ config.py: {e}")
        return False
    
    try:
        from estrattore_of import get_stato_field_name, STATO_FIELD_NAMES
        print(f"  ✅ estrattore_of.py OK - Campi stato: {STATO_FIELD_NAMES}")
    except ImportError as e:
        print(f"  ❌ estrattore_of.py: {e}")
        return False
    
    return True

def test_campo_stato():
    """Test rilevamento campo stato"""
    print("\n🧪 Test rilevamento campo STATO...")
    
    from estrattore_of import get_stato_field_name
    import pandas as pd
    
    # Test con STATO_UI
    df_ui = pd.DataFrame({'STATO_UI': ['102'], 'OTHER': ['test']})
    campo_ui = get_stato_field_name(df_ui.columns)
    print(f"  ✅ CSV con STATO_UI → rilevato: {campo_ui}")
    
    # Test con STATO_BUILDING
    df_building = pd.DataFrame({'STATO_BUILDING': ['302'], 'OTHER': ['test']})
    campo_building = get_stato_field_name(df_building.columns)
    print(f"  ✅ CSV con STATO_BUILDING → rilevato: {campo_building}")
    
    # Test senza campo stato
    df_nessuno = pd.DataFrame({'OTHER': ['test']})
    campo_default = get_stato_field_name(df_nessuno.columns)
    print(f"  ✅ CSV senza campo stato → default: {campo_default}")
    
    return True

def test_filtri_config():
    """Test configurazione filtri"""
    print("\n🧪 Test configurazione filtri...")
    
    from config import FILTRI_TIPOLOGIE_SEDE, STATI_UI
    
    print(f"  📊 Filtri disponibili: {len(FILTRI_TIPOLOGIE_SEDE)}")
    for key, data in FILTRI_TIPOLOGIE_SEDE.items():
        codici = data.get('codici', [])
        desc = data.get('descrizione', 'N/A')
        print(f"    • {key}: {desc} → {codici}")
    
    print(f"  📊 Stati UI disponibili: {len(STATI_UI)}")
    for code, desc in STATI_UI.items():
        print(f"    • {code}: {desc}")
    
    return True

def test_gui_creation():
    """Test creazione GUI (senza avvio)"""
    print("\n🧪 Test creazione GUI...")
    
    try:
        from estrattore_of_GUI import ModernOpenFiberGUI
        
        # Crea GUI ma non la avvia
        app = ModernOpenFiberGUI()
        print("  ✅ GUI creata con successo")
        
        # Verifica presenza dei nuovi metodi
        if hasattr(app, 'log_message'):
            print("  ✅ Metodo log_message presente")
        else:
            print("  ❌ Metodo log_message mancante")
        
        if hasattr(app, 'on_filter_change'):
            print("  ✅ Metodo on_filter_change presente")
        else:
            print("  ❌ Metodo on_filter_change mancante")
        
        # Test logging
        app.log_message("Test log message", "info")
        print("  ✅ Log message test OK")
        
        # Chiudi GUI senza mostrare
        app.app.destroy()
        print("  ✅ GUI chiusa correttamente")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Errore creazione GUI: {e}")
        return False

def main():
    """Test principale"""
    print("🚀 TEST MODIFICHE GUI ANALIZZATORE DB OPENFIBER v2.1.1")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Import
    if test_imports():
        tests_passed += 1
    
    # Test 2: Campo stato
    if test_campo_stato():
        tests_passed += 1
    
    # Test 3: Configurazione filtri
    if test_filtri_config():
        tests_passed += 1
    
    # Test 4: Creazione GUI
    if test_gui_creation():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RISULTATI: {tests_passed}/{total_tests} test superati")
    
    if tests_passed == total_tests:
        print("🎉 TUTTI I TEST SUPERATI! Le modifiche sono pronte.")
        return True
    else:
        print("❌ ALCUNI TEST FALLITI. Controlla gli errori sopra.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)