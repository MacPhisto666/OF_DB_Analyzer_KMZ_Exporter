#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test per verificare che tutti i log del core engine appaiano nella GUI
"""

import sys
import os
import time
import queue
import threading

# Fix encoding per Windows
try:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

# Aggiungi src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_stdout_redirect_durante_elaborazione():
    """Simula il comportamento del thread di elaborazione"""
    print("🧪 Test stdout redirect durante elaborazione...")
    
    from estrattore_of_GUI import StdoutRedirector
    
    # Setup come nella GUI
    log_queue = queue.Queue()
    original_stdout = sys.stdout
    
    # Attiva redirect
    sys.stdout = StdoutRedirector(log_queue, original_stdout)
    
    # Simula print del core engine
    print("=" * 60)
    print("🚀 ANALIZZATORE DB OPENFIBER v2.1.1")
    print("📍 Estrazione Regione 02 - Valle d'Aosta")
    print("=" * 60)
    print("📁 File input: test.csv")
    print("📂 File output: test.xlsx")
    print("⚙️ Chunk size: 10,000 righe")
    print("🔍 Filtro STATO_UI attivo: ['302']")
    print("  • 302: Sede PAC/PAL")
    print("-" * 60)
    
    # Simula progress
    for i in range(1, 6):
        print(f"📊 Chunk {i} - Righe totali: {i*10000:,}")
        time.sleep(0.1)
    
    print("✅ Trovato INIZIO Valle d'Aosta alla riga 718,828")
    print("  📋 Record estratti: 1,000")
    print("  📋 Record estratti: 2,000")
    print("✅ Estrazione completata: 2,000 record")
    
    # Ripristina stdout
    sys.stdout = original_stdout
    
    # Conta messaggi catturati
    messages = []
    try:
        while True:
            message = log_queue.get_nowait()
            messages.append(message[1])  # Solo il testo
    except queue.Empty:
        pass
    
    print(f"\n📊 Messaggi catturati: {len(messages)}")
    for i, msg in enumerate(messages[:10]):  # Primi 10
        print(f"  {i+1:2d}. {msg}")
    
    if len(messages) > 10:
        print(f"     ... e altri {len(messages) - 10} messaggi")
    
    # Verifica messaggi chiave
    key_messages = [
        "🚀 ANALIZZATORE DB OPENFIBER v2.1.1",
        "📍 Estrazione Regione 02 - Valle d'Aosta", 
        "📁 File input: test.csv",
        "⚙️ Chunk size: 10,000 righe",
        "🔍 Filtro STATO_UI attivo: ['302']",
        "✅ Trovato INIZIO Valle d'Aosta alla riga 718,828",
        "✅ Estrazione completata: 2,000 record"
    ]
    
    missing_messages = []
    for key_msg in key_messages:
        if not any(key_msg in msg for msg in messages):
            missing_messages.append(key_msg)
    
    if missing_messages:
        print(f"\n❌ Messaggi NON catturati ({len(missing_messages)}):")
        for msg in missing_messages:
            print(f"  • {msg}")
        return False
    else:
        print(f"\n✅ Tutti i messaggi chiave catturati!")
        return True

def test_log_gui_integration():
    """Test integrazione con la GUI"""
    print("\n🧪 Test integrazione log GUI...")
    
    try:
        from estrattore_of_GUI import ModernOpenFiberGUI
        
        # Crea GUI (senza avvio)
        app = ModernOpenFiberGUI()
        
        # Simula alcuni log
        app.log_message("🔧 Test log GUI diretto", "info")
        
        # Simula print che dovrebbe essere catturato
        print("📝 Test print catturato da GUI")
        print("🚀 Messaggio importante del core engine")
        
        # Processa i log
        app.update_log_display()
        
        # Verifica che ci sono messaggi nella queue
        message_count = 0
        try:
            while True:
                app.log_queue.get_nowait()
                message_count += 1
        except queue.Empty:
            pass
        
        print(f"  📊 Messaggi nella queue GUI: {message_count}")
        
        app.app.destroy()
        
        if message_count >= 3:  # Almeno i 3 messaggi di test
            print("  ✅ GUI cattura i messaggi correttamente")
            return True
        else:
            print("  ❌ GUI non cattura abbastanza messaggi")
            return False
        
    except Exception as e:
        print(f"  ❌ Errore test GUI: {e}")
        return False

def main():
    """Test principale"""
    print("🚀 TEST LOG COMPLETO CORE ENGINE → GUI")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    if test_stdout_redirect_durante_elaborazione():
        tests_passed += 1
    
    if test_log_gui_integration():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 RISULTATI: {tests_passed}/{total_tests} test superati")
    
    if tests_passed == total_tests:
        print("🎉 REDIRECT STDOUT FUNZIONA!")
        print("✅ Tutti i print() del core engine vengono catturati")
        print("✅ I messaggi vanno sia al terminale che alla GUI")
        print("✅ La GUI può visualizzare log completi")
        print("\n💡 Ora tutti i log del core engine dovrebbero")
        print("   apparire nella finestra 'Log Elaborazione (Live)'")
    else:
        print("❌ CI SONO ANCORA PROBLEMI NEL REDIRECT")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)