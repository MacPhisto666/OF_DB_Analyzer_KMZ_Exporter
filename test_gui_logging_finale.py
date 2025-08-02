#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test finale per verificare logging GUI
"""

import sys
import os
import time

# Fix encoding per Windows
try:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

# Aggiungi src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_gui_structure():
    """Test struttura base GUI senza avvio"""
    print("🧪 Test struttura GUI...")
    
    try:
        import tkinter as tk
        import ttkbootstrap as ttk_modern
        from estrattore_of_GUI import ModernOpenFiberGUI
        
        print("  ✅ Import GUI riuscito")
        
        # Crea GUI ma non avvia mainloop
        app = ModernOpenFiberGUI()
        
        # Verifica attributi essenziali
        essential_attrs = [
            'log_queue', 'progress_queue', 'log_text', 
            'original_stdout', 'processing'
        ]
        
        missing_attrs = []
        for attr in essential_attrs:
            if not hasattr(app, attr):
                missing_attrs.append(attr)
        
        if missing_attrs:
            print(f"  ❌ Attributi mancanti: {missing_attrs}")
            return False
        
        print("  ✅ Tutti gli attributi essenziali presenti")
        
        # Test log_message
        app.log_message("Test messaggio GUI", "info")
        print("  ✅ log_message funziona")
        
        # Test update_log_display
        app.update_log_display()
        print("  ✅ update_log_display funziona")
        
        # Chiudi GUI
        app.app.destroy()
        print("  ✅ GUI chiusa correttamente")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Errore: {e}")
        return False

def test_field_defaults():
    """Test valori di default dei campi"""
    print("\n🧪 Test valori default...")
    
    try:
        from estrattore_of_GUI import ModernOpenFiberGUI
        
        app = ModernOpenFiberGUI()
        
        # Test campo CSV input vuoto
        input_value = app.input_file_var.get()
        if input_value == "":
            print("  ✅ Campo CSV input vuoto")
        else:
            print(f"  ❌ Campo CSV input non vuoto: '{input_value}'")
            return False
        
        # Test campo output vuoto
        output_value = app.output_dir_var.get()
        if output_value == "":
            print("  ✅ Campo output vuoto")
        else:
            print(f"  ❌ Campo output non vuoto: '{output_value}'")
            return False
        
        app.app.destroy()
        return True
        
    except Exception as e:
        print(f"  ❌ Errore: {e}")
        return False

def test_redirector_fix():
    """Test StdoutRedirector con parametri corretti"""
    print("\n🧪 Test StdoutRedirector corretto...")
    
    try:
        import queue
        from estrattore_of_GUI import StdoutRedirector
        
        log_queue = queue.Queue()
        original_stdout = sys.stdout
        
        # Test creazione con parametri corretti
        redirector = StdoutRedirector(log_queue, original_stdout)
        print("  ✅ StdoutRedirector creato correttamente")
        
        # Test write
        redirector.write("Test messaggio\n")
        redirector.flush()
        
        # Verifica queue
        try:
            message = log_queue.get_nowait()
            print(f"  ✅ Messaggio nella queue: {message[1]}")
        except queue.Empty:
            print("  ❌ Nessun messaggio nella queue")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Errore: {e}")
        return False

def main():
    """Test principale"""
    print("🚀 TEST CORREZIONI GUI FINALI")
    print("=" * 45)
    
    tests_passed = 0
    total_tests = 3
    
    if test_gui_structure():
        tests_passed += 1
    
    if test_field_defaults():
        tests_passed += 1
    
    if test_redirector_fix():
        tests_passed += 1
    
    print("\n" + "=" * 45)
    print(f"📊 RISULTATI: {tests_passed}/{total_tests} test superati")
    
    if tests_passed == total_tests:
        print("🎉 TUTTE LE CORREZIONI FUNZIONANO!")
        print("✅ TypeError StdoutRedirector risolto")
        print("✅ Campi input/output vuoti per default")
        print("✅ Struttura GUI corretta")
        print("✅ Sistema logging predisposto")
        print("\n💡 La GUI dovrebbe ora:")
        print("   • Non avere errori nel thread")
        print("   • Mostrare i log nella finestra")
        print("   • Terminare correttamente l'elaborazione")
        print("   • Avere campi vuoti all'avvio")
    else:
        print("❌ ALCUNE CORREZIONI HANNO PROBLEMI")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)