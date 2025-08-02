#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test specifico per il sistema di logging GUI
"""

import sys
import os
import time
import threading

# Fix encoding per Windows
try:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except:
    pass

# Aggiungi src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_logging_components():
    """Test componenti del sistema di logging"""
    print("🧪 Test componenti logging...")
    
    import queue
    from datetime import datetime
    
    # Test queue
    log_queue = queue.Queue()
    
    # Test manuale
    timestamp = datetime.now().strftime("%H:%M:%S")
    test_message = "Test messaggio logging"
    log_queue.put((timestamp, test_message, "info"))
    
    # Verifica
    try:
        retrieved = log_queue.get_nowait()
        print(f"  ✅ Queue funziona: {retrieved}")
    except queue.Empty:
        print("  ❌ Queue vuota - errore")
        return False
    
    # Test StdoutRedirector
    from estrattore_of_GUI import StdoutRedirector
    
    original_stdout = sys.stdout
    redirector = StdoutRedirector(log_queue, original_stdout)
    
    # Test write
    redirector.write("Test write diretto\n")
    redirector.flush()
    
    # Verifica messaggi nella queue
    messages_count = 0
    try:
        while True:
            message = log_queue.get_nowait()
            messages_count += 1
            print(f"  📝 Messaggio {messages_count}: {message[1]}")
    except queue.Empty:
        pass
    
    if messages_count > 0:
        print(f"  ✅ StdoutRedirector funziona: {messages_count} messaggi")
    else:
        print("  ❌ StdoutRedirector non funziona")
        return False
    
    return True

def test_print_capture():
    """Test cattura print()"""
    print("\n🧪 Test cattura print()...")
    
    import queue
    from estrattore_of_GUI import StdoutRedirector
    
    log_queue = queue.Queue()
    original_stdout = sys.stdout
    
    # Attiva redirect
    sys.stdout = StdoutRedirector(log_queue, original_stdout)
    
    # Test print
    print("Questo è un test print() che dovrebbe essere catturato")
    print("Secondo messaggio di test")
    
    # Ripristina stdout
    sys.stdout = original_stdout
    
    # Verifica cattura
    captured_messages = []
    try:
        while True:
            message = log_queue.get_nowait()
            captured_messages.append(message[1])
    except queue.Empty:
        pass
    
    print(f"  📊 Messaggi catturati: {len(captured_messages)}")
    for i, msg in enumerate(captured_messages):
        print(f"    {i+1}. {msg}")
    
    if len(captured_messages) >= 2:
        print("  ✅ Print() catturati correttamente")
        return True
    else:
        print("  ❌ Print() non catturati")
        return False

def main():
    """Test principale"""
    print("🚀 TEST SISTEMA LOGGING GUI")
    print("=" * 40)
    
    success = True
    
    if not test_logging_components():
        success = False
    
    if not test_print_capture():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 LOGGING FUNZIONA!")
        print("✅ Queue funziona correttamente")
        print("✅ StdoutRedirector cattura i print()")
        print("✅ Messaggi vengono inviati alla GUI")
        print("\n💡 Se nella GUI non vedi ancora i log:")
        print("   • Verifica che update_log_display() venga chiamato")
        print("   • Controlla che il widget log_text sia configurato")
        print("   • Assicurati che non ci siano errori nel thread")
    else:
        print("❌ PROBLEMI NEL LOGGING")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)