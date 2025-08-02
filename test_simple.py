#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test semplificato per verificare import e funzioni base"""

import sys
import os

# Fix encoding per Windows
try:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

# Aggiungi src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic():
    print("Test import base...")
    
    try:
        from config import FILTRI_TIPOLOGIE_SEDE, STATI_UI
        print(f"✅ Config OK - {len(FILTRI_TIPOLOGIE_SEDE)} filtri, {len(STATI_UI)} stati")
    except ImportError as e:
        print(f"❌ Config error: {e}")
        return False
    
    try:
        from estrattore_of import get_stato_field_name, STATO_FIELD_NAMES
        print(f"✅ Estrattore OK - {STATO_FIELD_NAMES}")
    except ImportError as e:
        print(f"❌ Estrattore error: {e}")
        return False
    
    # Test funzione stato
    import pandas as pd
    df = pd.DataFrame({'STATO_UI': ['102'], 'OTHER': ['test']})
    result = get_stato_field_name(df.columns)
    print(f"✅ Test campo stato: {result}")
    
    return True

if __name__ == "__main__":
    success = test_basic()
    print(f"Test {'SUPERATO' if success else 'FALLITO'}")