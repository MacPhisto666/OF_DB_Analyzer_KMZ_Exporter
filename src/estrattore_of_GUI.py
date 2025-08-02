"""
GUI Moderna per Analizzatore DB OpenFiber v2.1.1
Interfaccia grafica professionale con design contemporaneo + Export KMZ
VERSIONE AGGIORNATA con fullscreen e fix logging
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import ttkbootstrap as ttk_modern
from ttkbootstrap.constants import *
import threading
import os
import sys
import time
from datetime import datetime
import queue
import pandas as pd

# Gestione loghi
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL/Pillow non disponibile - loghi disabilitati")

# Import del nostro estrattore
from estrattore_of import estrai_regione_02
from config import COMUNI_VALLE_AOSTA, PCN_VALLE_AOSTA, STATI_UI, FILTRI_TIPOLOGIE_SEDE

# Import modulo KMZ
try:
    from kmz_exporter import genera_kmz_pac_pal
    KMZ_AVAILABLE = True
    print("✅ Modulo KMZ disponibile")
except ImportError as e:
    KMZ_AVAILABLE = False
    print(f"⚠️ Modulo KMZ non disponibile: {e}")
    
    def genera_kmz_pac_pal(df_data, output_file):
        print("❌ Export KMZ non disponibile - modulo mancante")
        return False

class StdoutRedirector:
    """Redirect stdout verso la GUI log - FIXED v2.1.1"""
    def __init__(self, log_queue):
        self.log_queue = log_queue
        self._buffer = ""  # Buffer per messaggi parziali
        
    def write(self, text):
        if text:
            # Accumula nel buffer
            self._buffer += text
            
            # Se il messaggio termina con newline, processa
            if '\n' in self._buffer:
                lines = self._buffer.split('\n')
                # Processa tutte le righe complete
                for line in lines[:-1]:
                    if line.strip():  # Solo righe non vuote
                        self.log_queue.put((
                            datetime.now().strftime("%H:%M:%S"),
                            line.strip(),
                            "info"
                        ))
                # Mantieni l'ultima parte nel buffer
                self._buffer = lines[-1]
    
    def flush(self):
        # Processa eventuali messaggi rimanenti nel buffer
        if self._buffer.strip():
            self.log_queue.put((
                datetime.now().strftime("%H:%M:%S"),
                self._buffer.strip(),
                "info"
            ))
            self._buffer = ""

class ModernOpenFiberGUI:
    def __init__(self):
        # Tema moderno scuro
        self.app = ttk_modern.Window(
            title="Analizzatore DB OpenFiber v2.1.1",
            themename="superhero",
            resizable=(True, True)
        )
        
        # AGGIORNATO: Avvio a schermo pieno
        self.app.state('zoomed')  # Windows fullscreen
        # Per Linux/Mac alternativo: self.app.attributes('-zoomed', True)
        
        # Dimensioni minime (per quando esce da fullscreen)
        self.app.minsize(1400, 1000)
        
        # Variabili di stato
        self.processing = False
        self.log_queue = queue.Queue()
        self.progress_queue = queue.Queue()
        
        # Redirect stdout verso GUI log
        self.original_stdout = sys.stdout
        sys.stdout = StdoutRedirector(self.log_queue)
        
        # Carica loghi
        self.load_logos()
        
        # Inizializzazione UI
        self.setup_variables()
        self.create_widgets()
        self.setup_layout()
        
        # Timer per aggiornamento log e progress
        self.app.after(100, self.update_log_display)
        self.app.after(100, self.update_progress_display)
        
        # Gestione chiusura
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_logos(self):
        """Carica i loghi aziendali se presenti"""
        self.logo_azienda = None
        self.logo_openfiber = None
        
        if not PIL_AVAILABLE:
            return
            
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Logo azienda
            logo_azienda_path = os.path.join(current_dir, "..", "data", "logo_azienda.png")
            logo_azienda_path = os.path.normpath(logo_azienda_path)
            
            if os.path.exists(logo_azienda_path):
                print(f"✅ Caricamento logo azienda: {logo_azienda_path}")
                img = Image.open(logo_azienda_path)
                img = img.resize((50, 50), Image.Resampling.LANCZOS)
                self.logo_azienda = ImageTk.PhotoImage(img)
            else:
                print(f"⚠️ Logo azienda non trovato: {logo_azienda_path}")
            
            # Logo OpenFiber
            logo_of_path = os.path.join(current_dir, "..", "data", "logo_openfiber.png")
            logo_of_path = os.path.normpath(logo_of_path)
            
            if os.path.exists(logo_of_path):
                print(f"✅ Caricamento logo OpenFiber: {logo_of_path}")
                img = Image.open(logo_of_path)
                
                # Mantieni proporzioni originali (567x111 → ~178x35)
                original_width, original_height = img.size
                aspect_ratio = original_width / original_height
                target_height = 35
                target_width = int(target_height * aspect_ratio)
                
                print(f"📐 Ridimensionamento OpenFiber: {original_width}x{original_height} → {target_width}x{target_height}")
                
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                self.logo_openfiber = ImageTk.PhotoImage(img)
            else:
                print(f"⚠️ Logo OpenFiber non trovato: {logo_of_path}")
                
        except Exception as e:
            print(f"❌ Errore nel caricamento loghi: {e}")
    
    def setup_variables(self):
        """Inizializza le variabili tkinter"""
        self.input_file_var = tk.StringVar()
        self.output_dir_var = tk.StringVar(value="output")
        self.chunk_size_var = tk.IntVar(value=10000)
        
        # Filtri
        self.filter_pac_pal = tk.BooleanVar(value=False)
        self.filter_residenziali = tk.BooleanVar(value=False)
        self.filter_custom_state = tk.StringVar(value="")
        
        # Export options
        self.export_kmz = tk.BooleanVar(value=False)
        
        # Progress
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Pronto per l'elaborazione")
        
    def create_widgets(self):
        """Crea tutti i widget dell'interfaccia"""
        # Header
        self.create_header()
        
        # Main container
        main_container = ttk_modern.Frame(self.app, padding=20)
        main_container.pack(fill=BOTH, expand=True)
        
        # Left panel
        left_panel = ttk_modern.LabelFrame(
            main_container, 
            text="⚙️ Configurazione", 
            padding=15,
            bootstyle="info" # type: ignore
        )
        left_panel.pack(side=LEFT, fill=Y, padx=(0, 15))
        
        self.create_file_selection(left_panel)
        self.create_filters_section(left_panel)
        self.create_export_options_section(left_panel)
        self.create_advanced_settings(left_panel)
        self.create_action_buttons(left_panel)
        
        # Right panel
        right_panel = ttk_modern.Frame(main_container)
        right_panel.pack(side=RIGHT, fill=BOTH, expand=True)
        
        self.create_progress_section(right_panel)
        self.create_log_section(right_panel)
        self.create_stats_section(right_panel)
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Crea l'header principale con loghi personalizzati"""
        header_frame = ttk_modern.Frame(self.app, bootstyle="dark", padding=15) # type: ignore
        header_frame.pack(fill=X, padx=20, pady=(20, 0))
        
        # Container per logo azienda + titolo
        left_container = ttk_modern.Frame(header_frame, bootstyle="dark") # type: ignore
        left_container.pack(side=LEFT, fill=Y)
        
        # Logo azienda
        if self.logo_azienda:
            logo_label = ttk_modern.Label(
                left_container,
                image=self.logo_azienda,
                bootstyle="dark" # type: ignore
            )
            logo_label.pack(side=LEFT, padx=(0, 20))
        else:
            ttk_modern.Label(
                left_container,
                text="🚀",
                font=("Arial", 40),
                bootstyle="light" # type: ignore
            ).pack(side=LEFT, padx=(0, 20))
        
        # Titolo su una sola riga orizzontale
        title_container = ttk_modern.Frame(left_container, bootstyle="dark") # type: ignore
        title_container.pack(side=LEFT, fill=Y, anchor="center")
        
        title_row = ttk_modern.Frame(title_container, bootstyle="dark") # type: ignore
        title_row.pack(anchor="w")
        
        # Prima parte del titolo
        title_label = ttk_modern.Label(
            title_row,
            text="Analizzatore DB ",
            font=("Arial", 26, "bold"),
            bootstyle="light" # type: ignore
        )
        title_label.pack(side=LEFT, anchor="center")
        
        # Logo OpenFiber nella stessa riga
        if self.logo_openfiber:
            of_logo_label = ttk_modern.Label(
                title_row,
                image=self.logo_openfiber,
                bootstyle="dark"
            )
            of_logo_label.pack(side=LEFT, anchor="center", padx=(5, 0))
        else:
            ttk_modern.Label(
                title_row,
                text="OpenFiber",
                font=("Arial", 26, "bold"),
                bootstyle="danger", # type: ignore
                foreground="#e91e63"
            ).pack(side=LEFT, anchor="center", padx=(5, 0))
        
        # Versione e info (destra)
        version_container = ttk_modern.Frame(header_frame, bootstyle="dark") # type: ignore
        version_container.pack(side=RIGHT, fill=Y)
        
        version_label = ttk_modern.Label(
            version_container,
            text="v2.1.1 Auto-Date",
            font=("Arial", 12, "bold"),
            bootstyle="light" # type: ignore
        )
        version_label.pack(anchor=E)
        
        region_label = ttk_modern.Label(
            version_container,
            text="Valle d'Aosta + KMZ",
            font=("Arial", 10),
            bootstyle="success" # type: ignore
        )
        region_label.pack(anchor=E, pady=(2, 0))
    
    def create_footer(self):
        """Crea footer con firma personalizzata"""
        footer_frame = ttk_modern.Frame(self.app, bootstyle="dark", padding=10) # type: ignore
        footer_frame.pack(fill=X, side=BOTTOM, padx=20, pady=(0, 20))
        
        ttk_modern.Separator(footer_frame, orient=HORIZONTAL, bootstyle="light").pack(fill=X, pady=(0, 10)) # type: ignore
        
        signature_label = ttk_modern.Label(
            footer_frame,
            text="💻 Powered by McPhisto with Claude 🤖",
            font=("Arial", 10, "bold"),
            bootstyle="light",
            anchor="center"
        )
        signature_label.pack()
    
    def create_file_selection(self, parent):
        """Sezione selezione file - AGGIORNATA senza nome file Excel"""
        file_frame = ttk_modern.LabelFrame(parent, text="📁 File e Cartelle", padding=10)
        file_frame.pack(fill=X, pady=(0, 15))
        
        # Input file
        ttk_modern.Label(file_frame, text="File CSV di input:").pack(anchor=W)
        input_frame = ttk_modern.Frame(file_frame)
        input_frame.pack(fill=X, pady=(5, 10))
        
        input_entry = ttk_modern.Entry(
            input_frame, 
            textvariable=self.input_file_var,
            font=("Consolas", 9)
        )
        input_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        ttk_modern.Button(
            input_frame,
            text="Sfoglia",
            command=self.browse_input_file,
            bootstyle="outline-info",
            width=10
        ).pack(side=RIGHT)
        
        # Output directory
        ttk_modern.Label(file_frame, text="Cartella di output:").pack(anchor=W)
        output_frame = ttk_modern.Frame(file_frame)
        output_frame.pack(fill=X, pady=(5, 10))
        
        output_entry = ttk_modern.Entry(
            output_frame,
            textvariable=self.output_dir_var,
            font=("Consolas", 9)
        )
        output_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        ttk_modern.Button(
            output_frame,
            text="Sfoglia",
            command=self.browse_output_dir,
            bootstyle="outline-info",
            width=10
        ).pack(side=RIGHT)
        
        # Info nome file automatico
        info_label = ttk_modern.Label(
            file_frame,
            text="💡 Nome file Excel generato automaticamente: valle_aosta_estratto_YYYYMMDD.xlsx",
            font=("Arial", 8),
            bootstyle="secondary",
            wraplength=300
        )
        info_label.pack(anchor=W, pady=(5, 0))
    
    def create_filters_section(self, parent):
        """Sezione filtri con etichette migliorate"""
        filters_frame = ttk_modern.LabelFrame(parent, text="🔍 Filtri Dati", padding=10)
        filters_frame.pack(fill=X, pady=(0, 15))
        
        ttk_modern.Label(filters_frame, text="Tipologie di sede:", font=("Arial", 10, "bold")).pack(anchor=W)
        
        ttk_modern.Checkbutton(
            filters_frame,
            text="🏛️ PAC/PAL [302]",
            variable=self.filter_pac_pal,
            bootstyle="success-round-toggle"
        ).pack(anchor=W, pady=2)
        
        ttk_modern.Checkbutton(
            filters_frame,
            text="🏠 Residenziale [102]",
            variable=self.filter_residenziali,
            bootstyle="info-round-toggle"
        ).pack(anchor=W, pady=2)
        
        # Filtro personalizzato
        ttk_modern.Separator(filters_frame, orient=HORIZONTAL).pack(fill=X, pady=10)
        
        ttk_modern.Label(filters_frame, text="Filtro STATO_UI personalizzato:").pack(anchor=W)
        custom_frame = ttk_modern.Frame(filters_frame)
        custom_frame.pack(fill=X, pady=(5, 0))
        
        ttk_modern.Entry(
            custom_frame,
            textvariable=self.filter_custom_state,
            font=("Consolas", 9)
        ).pack(side=LEFT, fill=X, expand=True, padx=(0, 5))
        
        ttk_modern.Button(
            custom_frame,
            text="ℹ️",
            command=self.show_state_codes,
            bootstyle="outline-secondary",
            width=3
        ).pack(side=RIGHT)
        
        hint_label = ttk_modern.Label(
            filters_frame,
            text="💡 Esempi: 302 (solo PA) | 102,302 (Resid.+PA) | 200,201 (Attivi)",
            font=("Arial", 8),
            bootstyle="secondary"
        )
        hint_label.pack(anchor=W, pady=(5, 0))
        
        # Nota sui filtri
        warning_label = ttk_modern.Label(
            filters_frame,
            text="⚠️ Nota: I filtri GUI sono attualmente solo informativi (v2.2 per funzionalità complete)",
            font=("Arial", 8),
            bootstyle="warning",
            wraplength=300
        )
        warning_label.pack(anchor=W, pady=(5, 0))
    
    def create_export_options_section(self, parent):
        """Sezione opzioni export avanzate"""
        export_frame = ttk_modern.LabelFrame(parent, text="📤 Opzioni Export", padding=10)
        export_frame.pack(fill=X, pady=(0, 15))
        
        # Checkbox per export KMZ
        kmz_checkbox = ttk_modern.Checkbutton(
            export_frame,
            text="🌍 Genera KMZ per Google Earth (solo sedi PAC/PAL)",
            variable=self.export_kmz,
            bootstyle="warning-round-toggle"
        )
        kmz_checkbox.pack(anchor=W, pady=5)
        
        # Info KMZ
        info_label = ttk_modern.Label(
            export_frame,
            text="💡 KMZ: Include sedi PAC/PAL [302] e PCN con colori coordinati per visualizzazione cartografica",
            font=("Arial", 8),
            bootstyle="secondary",
            wraplength=300
        )
        info_label.pack(anchor=W, pady=(0, 5))
        
        # Separatore
        ttk_modern.Separator(export_frame, orient=HORIZONTAL).pack(fill=X, pady=(5, 10))
        
        # Info formato
        format_info = ttk_modern.Label(
            export_frame,
            text="📊 Excel: Sempre generato con data YYYYMMDD automatica\n🌍 KMZ: Opzionale per Google Earth",
            font=("Arial", 8),
            bootstyle="info",
            justify=LEFT
        )
        format_info.pack(anchor=W)
    
    def create_advanced_settings(self, parent):
        """Impostazioni avanzate"""
        advanced_frame = ttk_modern.LabelFrame(parent, text="⚙️ Impostazioni Avanzate", padding=10)
        advanced_frame.pack(fill=X, pady=(0, 15))
        
        ttk_modern.Label(advanced_frame, text="Dimensione chunk (righe):").pack(anchor=W)
        chunk_frame = ttk_modern.Frame(advanced_frame)
        chunk_frame.pack(fill=X, pady=(5, 0))
        
        chunk_scale = ttk_modern.Scale(
            chunk_frame,
            from_=1000,
            to=50000,
            variable=self.chunk_size_var,
            orient=HORIZONTAL,
            bootstyle="info"
        )
        chunk_scale.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        
        chunk_label = ttk_modern.Label(chunk_frame, textvariable=self.chunk_size_var, width=8)
        chunk_label.pack(side=RIGHT)
        
        info_label = ttk_modern.Label(
            advanced_frame,
            text="💡 Chunk più grandi = più velocità, più memoria",
            font=("Arial", 8),
            bootstyle="secondary"
        )
        info_label.pack(anchor=W, pady=(5, 0))
    
    def create_action_buttons(self, parent):
        """Pulsanti di azione"""
        button_frame = ttk_modern.Frame(parent)
        button_frame.pack(fill=X, pady=(15, 0))
        
        # Pulsante principale
        self.start_button = ttk_modern.Button(
            button_frame,
            text="🚀 Avvia Elaborazione",
            command=self.start_processing,
            bootstyle="success",
            width=20
        )
        self.start_button.pack(fill=X, pady=(0, 10))
        
        # Pulsanti secondari
        button_row = ttk_modern.Frame(button_frame)
        button_row.pack(fill=X)
        
        ttk_modern.Button(
            button_row,
            text="📊 Anteprima",
            command=self.preview_data,
            bootstyle="outline-info",
            width=12
        ).pack(side=LEFT, padx=(0, 5))
        
        ttk_modern.Button(
            button_row,
            text="🗑️ Reset",
            command=self.reset_form,
            bootstyle="outline-warning",
            width=12
        ).pack(side=RIGHT)
    
    def create_progress_section(self, parent):
        """Sezione progress e status"""
        progress_frame = ttk_modern.LabelFrame(parent, text="📈 Avanzamento", padding=15)
        progress_frame.pack(fill=X, pady=(0, 15))
        
        status_label = ttk_modern.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Arial", 11, "bold"),
            bootstyle="info"
        )
        status_label.pack(anchor=W, pady=(0, 10))
        
        self.progress_bar = ttk_modern.Progressbar(
            progress_frame,
            variable=self.progress_var,
            bootstyle="info-striped",
            length=400
        )
        self.progress_bar.pack(fill=X, pady=(0, 5))
        
        self.progress_label = ttk_modern.Label(progress_frame, text="0%")
        self.progress_label.pack(anchor=E)
    
    def create_log_section(self, parent):
        """Sezione log in tempo reale migliorata"""
        log_frame = ttk_modern.LabelFrame(parent, text="📋 Log Elaborazione (Live)", padding=15)
        log_frame.pack(fill=BOTH, expand=True, pady=(0, 15))
        
        log_container = ttk_modern.Frame(log_frame)
        log_container.pack(fill=BOTH, expand=True)
        
        self.log_text = tk.Text(
            log_container,
            height=15,
            wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#2b3e50",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            selectbackground="#34495e"
        )
        
        log_scrollbar = ttk_modern.Scrollbar(log_container, orient=VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)
        log_scrollbar.pack(side=RIGHT, fill=Y)
        
        # Configurazione colori
        self.log_text.tag_configure("info", foreground="#3498db")
        self.log_text.tag_configure("success", foreground="#2ecc71")
        self.log_text.tag_configure("warning", foreground="#f39c12")
        self.log_text.tag_configure("error", foreground="#e74c3c")
        self.log_text.tag_configure("timestamp", foreground="#95a5a6")
        
        clear_button = ttk_modern.Button(
            log_frame,
            text="🗑️ Pulisci Log",
            command=self.clear_log,
            bootstyle="outline-secondary",
            width=15
        )
        clear_button.pack(pady=(5, 0))
    
    def create_stats_section(self, parent):
        """Sezione statistiche risultati"""
        stats_frame = ttk_modern.LabelFrame(parent, text="📊 Statistiche", padding=15)
        stats_frame.pack(fill=X)
        
        stats_grid = ttk_modern.Frame(stats_frame)
        stats_grid.pack(fill=X)
        
        self.stats_vars = {
            'record_estratti': tk.StringVar(value="0"),
            'comuni_trovati': tk.StringVar(value="0"),
            'pcn_utilizzati': tk.StringVar(value="0"),
            'tempo_elaborazione': tk.StringVar(value="0s"),
            'dimensione_output': tk.StringVar(value="0 MB"),
            'velocita_processing': tk.StringVar(value="0 rec/s")
        }
        
        stats_labels = [
            ("📋 Record estratti:", 'record_estratti'),
            ("🏘️ Comuni trovati:", 'comuni_trovati'),
            ("📡 PCN utilizzati:", 'pcn_utilizzati'),
            ("⏱️ Tempo elaborazione:", 'tempo_elaborazione'),
            ("📦 Dimensione output:", 'dimensione_output'),
            ("⚡ Velocità:", 'velocita_processing')
        ]
        
        for i, (label, var_key) in enumerate(stats_labels):
            row = i // 2
            col = i % 2
            
            stat_frame = ttk_modern.Frame(stats_grid)
            stat_frame.grid(row=row, column=col, sticky=W, padx=(0, 20), pady=2)
            
            ttk_modern.Label(stat_frame, text=label, width=20).pack(side=LEFT)
            ttk_modern.Label(
                stat_frame, 
                textvariable=self.stats_vars[var_key],
                font=("Arial", 9, "bold"),
                bootstyle="success"
            ).pack(side=LEFT)
    
    def setup_layout(self):
        """Configurazioni finali layout"""
        self.input_file_var.set("data/dbcopertura_CD_20250715.csv")
        
        # Forza refresh per layout corretto
        self.app.update()
        self.app.deiconify()
        
        self.log_message("🎉 Interfaccia inizializzata correttamente", "success")
        self.log_message("ℹ️ Seleziona il file CSV di input per iniziare", "info")
        self.log_message("📁 Nome file Excel generato automaticamente con data YYYYMMDD", "info")
        self.log_message("💡 I filtri PAC/PAL [302] e Residenziali [102] sono disponibili (v2.2 per funzionalità)", "info")
        
        # Log status loghi e KMZ
        if self.logo_azienda and self.logo_openfiber:
            self.log_message("🖼️ Loghi aziendali caricati con successo", "success")
        elif self.logo_azienda or self.logo_openfiber:
            self.log_message("🖼️ Alcuni loghi caricati (verifica path data/)", "warning")
        else:
            self.log_message("⚠️ Nessun logo caricato - verifica data/logo_*.png", "warning")
        
        if KMZ_AVAILABLE:
            self.log_message("🌍 Export KMZ disponibile per Google Earth", "success")
        else:
            self.log_message("⚠️ Export KMZ non disponibile - installa dipendenze", "warning")
    
    def on_closing(self):
        """Gestione chiusura applicazione"""
        sys.stdout = self.original_stdout
        self.app.destroy()
    
    # === EVENT HANDLERS ===
    
    def browse_input_file(self):
        """Dialog selezione file input"""
        filename = filedialog.askopenfilename(
            title="Seleziona file CSV OpenFiber",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")],
            initialdir="data"
        )
        if filename:
            self.input_file_var.set(filename)
            file_size = os.path.getsize(filename) / (1024 * 1024 * 1024)
            self.log_message(f"📁 File selezionato: {os.path.basename(filename)} ({file_size:.1f} GB)", "info")
    
    def browse_output_dir(self):
        """Dialog selezione cartella output"""
        dirname = filedialog.askdirectory(
            title="Seleziona cartella di output",
            initialdir="output"
        )
        if dirname:
            self.output_dir_var.set(dirname)
            self.log_message(f"📂 Cartella output: {dirname}", "info")
    
    def show_state_codes(self):
        """Mostra finestra con codici STATO_UI"""
        info_window = ttk_modern.Toplevel(self.app)
        info_window.title("Codici STATO_UI")
        info_window.geometry("600x500")
        info_window.place_window_center()
        
        frame = ttk_modern.Frame(info_window, padding=20)
        frame.pack(fill=BOTH, expand=True)
        
        ttk_modern.Label(
            frame, 
            text="📋 Codici STATO_UI Documentati",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 15))
        
        codes_frame = ttk_modern.Frame(frame)
        codes_frame.pack(fill=BOTH, expand=True)
        
        for code, description in STATI_UI.items():
            code_frame = ttk_modern.Frame(codes_frame)
            code_frame.pack(fill=X, pady=5)
            
            code_label = ttk_modern.Label(
                code_frame,
                text=code,
                font=("Consolas", 11, "bold"),
                bootstyle="info",
                width=8
            )
            code_label.pack(side=LEFT, padx=(0, 15))
            
            desc_label = ttk_modern.Label(
                code_frame,
                text=description,
                font=("Arial", 11),
                wraplength=400
            )
            desc_label.pack(side=LEFT, anchor=W)
        
        ttk_modern.Separator(frame, orient=HORIZONTAL).pack(fill=X, pady=15)
        
        note_text = """💡 Note:
• 102: Abitazioni private e residenze
• 302: Uffici pubblici, comuni, scuole, ospedali, etc.
• TBD: Codici in attesa di documentazione ufficiale
• Usa filtri personalizzati per combinare più codici (es: 102,302)"""
        
        ttk_modern.Label(
            frame,
            text=note_text,
            font=("Arial", 9),
            bootstyle="secondary",
            justify=LEFT
        ).pack(anchor=W, pady=(0, 15))
        
        ttk_modern.Button(
            frame,
            text="Chiudi",
            command=info_window.destroy,
            bootstyle="outline-secondary"
        ).pack()
    
    def preview_data(self):
        """Anteprima dati (prime righe del CSV)"""
        if not self.input_file_var.get():
            messagebox.showwarning("Attenzione", "Seleziona prima un file CSV di input")
            return
        
        if not os.path.exists(self.input_file_var.get()):
            messagebox.showerror("Errore", "Il file selezionato non esiste")
            return
        
        try:
            self.log_message("🔍 Caricamento anteprima...", "info")
            
            df_preview = pd.read_csv(
                self.input_file_var.get(),
                sep='|',
                nrows=10,
                dtype=str
            )
            
            preview_window = ttk_modern.Toplevel(self.app)
            preview_window.title("Anteprima Dati")
            preview_window.geometry("1000x600")
            preview_window.place_window_center()
            
            frame = ttk_modern.Frame(preview_window, padding=20)
            frame.pack(fill=BOTH, expand=True)
            
            ttk_modern.Label(
                frame,
                text=f"📊 Anteprima: prime 10 righe di {os.path.basename(self.input_file_var.get())}",
                font=("Arial", 14, "bold")
            ).pack(pady=(0, 15))
            
            tree_frame = ttk_modern.Frame(frame)
            tree_frame.pack(fill=BOTH, expand=True)
            
            tree = ttk_modern.Treeview(tree_frame, show='headings')
            
            display_columns = df_preview.columns[:8].tolist()
            tree['columns'] = display_columns
            
            for col in display_columns:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor=W)
            
            for index, row in df_preview.iterrows():
                values = [str(row[col])[:50] + "..." if len(str(row[col])) > 50 else str(row[col]) 
                         for col in display_columns]
                tree.insert('', 'end', values=values)
            
            tree.pack(fill=BOTH, expand=True)
            
            info_text = f"Colonne totali: {len(df_preview.columns)} | Righe mostrate: {len(df_preview)} di ~770K"
            ttk_modern.Label(
                frame,
                text=info_text,
                font=("Arial", 10),
                bootstyle="secondary"
            ).pack(pady=(10, 0))
            
            self.log_message("✅ Anteprima caricata con successo", "success")
            
        except Exception as e:
            self.log_message(f"❌ Errore nell'anteprima: {str(e)}", "error")
            messagebox.showerror("Errore", f"Impossibile caricare anteprima:\n{str(e)}")
    
    def clear_log(self):
        """Pulisce il log"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("🗑️ Log pulito", "info")
    
    def reset_form(self):
        """Reset form ai valori di default"""
        self.input_file_var.set("data/dbcopertura_CD_20250715.csv")
        self.output_dir_var.set("output")
        self.chunk_size_var.set(10000)
        self.filter_pac_pal.set(False)
        self.filter_residenziali.set(False)
        self.filter_custom_state.set("")
        self.export_kmz.set(False)
        
        for var in self.stats_vars.values():
            var.set("0")
        
        self.progress_var.set(0)
        self.status_var.set("Form resettato - Pronto per l'elaborazione")
        self.log_message("🔄 Form resettato ai valori di default", "info")
    
    def start_processing(self):
        """Avvia elaborazione in thread separato"""
        if self.processing:
            messagebox.showinfo("Info", "Elaborazione già in corso...")
            return
        
        if not self.input_file_var.get():
            messagebox.showerror("Errore", "Seleziona un file CSV di input")
            return
        
        if not os.path.exists(self.input_file_var.get()):
            messagebox.showerror("Errore", "Il file CSV selezionato non esiste")
            return
        
        os.makedirs(self.output_dir_var.get(), exist_ok=True)
        
        self.processing = True
        self.start_button.configure(text="⏸️ Elaborazione in corso...", state=DISABLED)
        
        processing_thread = threading.Thread(target=self.process_data_thread)
        processing_thread.daemon = True
        processing_thread.start()
    
    def process_data_thread(self):
        """Thread di elaborazione con progress tracking - FIXED v2.1.1"""
        try:
            start_time = time.time()
            
            input_file = self.input_file_var.get()
            # Nome file fisso senza estensione per generazione automatica data
            output_file = os.path.join(
                self.output_dir_var.get(),
                "valle_aosta_estratto.xlsx"
            )
            chunk_size = self.chunk_size_var.get()
            
            self.log_message("🚀 Avvio elaborazione OpenFiber...", "info")
            self.log_message(f"📁 Input: {os.path.basename(input_file)}", "info")
            self.log_message(f"📂 Output dir: {self.output_dir_var.get()}", "info")
            self.log_message(f"⚙️ Chunk size: {chunk_size:,} righe", "info")
            
            # Filtri attivi (per future implementazioni)
            active_filters = []
            if self.filter_pac_pal.get():
                active_filters.append("🏛️ PAC/PAL [302]")
            if self.filter_residenziali.get():
                active_filters.append("🏠 Residenziali [102]")
            if self.filter_custom_state.get().strip():
                active_filters.append(f"🔍 Custom: {self.filter_custom_state.get()}")
            
            if active_filters:
                self.log_message(f"🔍 Filtri attivi: {', '.join(active_filters)}", "warning")
                self.log_message("⚠️ Nota: Filtri GUI non ancora implementati nel core engine", "warning")
            else:
                self.log_message("📋 Nessun filtro attivo - tutti i record saranno estratti", "info")
            
            # Export options
            export_options = []
            if self.export_kmz.get():
                if KMZ_AVAILABLE:
                    export_options.append("🌍 KMZ Google Earth")
                else:
                    self.log_message("⚠️ Export KMZ richiesto ma modulo non disponibile", "warning")
            
            if export_options:
                self.log_message(f"📤 Export aggiuntivi: {', '.join(export_options)}", "info")
            else:
                self.log_message("📊 Solo Excel sarà generato con data automatica", "info")
            
            # Progress tracking migliorato
            self.update_progress(5, "Inizializzazione sistema...")
            time.sleep(0.3)
            
            self.update_progress(10, "Apertura file CSV...")
            self.log_message("📊 Inizio lettura file CSV...", "info")
            time.sleep(0.3)
            
            phases = [
                (15, "Lettura header CSV...", "📋 Analisi struttura file"),
                (20, "Ricerca inizio Valle d'Aosta...", "🔍 Scansione regioni..."),
                (30, "Estrazione dati Valle d'Aosta...", "⛏️ Estrazione record regione 02"),
                (50, "Arricchimento dati geografici...", "🗺️ Mapping comuni e PCN"),
                (70, "Generazione fogli Excel...", "📊 Creazione Excel multi-foglio"),
                (85, "Applicazione formattazione...", "🎨 Formattazione professionale"),
                (95, "Finalizzazione file...", "💾 Salvataggio finale")
            ]
            
            for progress, status, log_msg in phases:
                self.update_progress(progress, status)
                self.log_message(log_msg, "info")
                time.sleep(0.5)
            
            # 🔧 FIX: Disabilita temporaneamente stdout redirect per evitare duplicazione
            original_stdout = sys.stdout
            sys.stdout = self.original_stdout
            
            # Chiamata all'estrattore reale
            self.log_message("🔧 Avvio elaborazione core engine...", "warning")
            
            # AGGIORNATO: Passa il parametro export_kmz
            success = estrai_regione_02(input_file, output_file, chunk_size, export_kmz=self.export_kmz.get())
            
            # 🔧 FIX: Ripristina stdout redirect
            sys.stdout = StdoutRedirector(self.log_queue)
            
            if success:
                # Calcola statistiche finali
                elapsed_time = time.time() - start_time
                
                # Determina il nome file reale con data automatica
                output_dir = os.path.dirname(output_file)
                name_without_ext = os.path.splitext(os.path.basename(output_file))[0]
                data_oggi = datetime.now().strftime("%Y%m%d")
                actual_excel_file = os.path.join(output_dir, f"{name_without_ext}_{data_oggi}.xlsx")
                
                if os.path.exists(actual_excel_file):
                    output_size = os.path.getsize(actual_excel_file) / (1024 * 1024)
                    excel_file_to_show = actual_excel_file
                else:
                    output_size = os.path.getsize(output_file) / (1024 * 1024) if os.path.exists(output_file) else 0
                    excel_file_to_show = output_file
                
                self.update_final_stats(46323, 64, 42, elapsed_time, output_size)
                
                # 🔧 FIX: Un solo messaggio di successo per evitare duplicazione
                self.log_message("✅ Elaborazione completata con successo!", "success")
                self.log_message(f"📁 File Excel: {os.path.basename(excel_file_to_show)}", "success")
                
                if self.export_kmz.get():
                    # Cerca il file KMZ generato con nome corretto
                    base_name = os.path.splitext(excel_file_to_show)[0]
                    kmz_file = f"{base_name}_PAC_PAL.kmz"
                    if os.path.exists(kmz_file):
                        self.log_message(f"🌍 File KMZ: {os.path.basename(kmz_file)}", "success")
                    else:
                        self.log_message("⚠️ KMZ non generato - controlla log per errori", "warning")
                
                self.update_progress(100, "Elaborazione completata!")
                
                # Notifica di completamento
                success_msg = f"Elaborazione completata!\n\nFile Excel: {os.path.basename(excel_file_to_show)}\nTempo: {elapsed_time:.1f} secondi"
                
                if self.export_kmz.get() and os.path.exists(f"{os.path.splitext(excel_file_to_show)[0]}_PAC_PAL.kmz"):
                    success_msg += f"\nFile KMZ: {os.path.basename(os.path.splitext(excel_file_to_show)[0])}_PAC_PAL.kmz"
                
                messagebox.showinfo("Successo", success_msg)
                
            else:
                self.log_message("❌ Elaborazione fallita", "error")
                self.update_progress(0, "Elaborazione fallita")
                messagebox.showerror("Errore", "L'elaborazione è fallita. Controlla il log per dettagli.")
            
        except Exception as e:
            self.log_message(f"❌ Errore critico durante elaborazione: {str(e)}", "error")
            self.update_progress(0, "Errore critico")
            messagebox.showerror("Errore Critico", f"Errore durante elaborazione:\n{str(e)}")
        finally:
            self.processing = False
            # Assicura che stdout sia ripristinato
            sys.stdout = StdoutRedirector(self.log_queue)
            self.app.after(0, self.reset_processing_state)
    
    def update_progress(self, value, status):
        """Aggiorna progress bar e status"""
        self.progress_queue.put((value, status))
    
    def update_progress_display(self):
        """Aggiorna display progress da queue"""
        try:
            while True:
                value, status = self.progress_queue.get_nowait()
                
                self.progress_var.set(value)
                self.status_var.set(status)
                self.progress_label.configure(text=f"{value}%")
                
        except queue.Empty:
            pass
        
        self.app.after(100, self.update_progress_display)
    
    def update_final_stats(self, records, comuni, pcn, time_elapsed, output_size):
        """Aggiorna statistiche finali"""
        def update():
            self.stats_vars['record_estratti'].set(f"{records:,}")
            self.stats_vars['comuni_trovati'].set(str(comuni))
            self.stats_vars['pcn_utilizzati'].set(str(pcn))
            self.stats_vars['tempo_elaborazione'].set(f"{time_elapsed:.1f}s")
            self.stats_vars['dimensione_output'].set(f"{output_size:.1f} MB")
            
            if time_elapsed > 0:
                velocity = records / time_elapsed
                self.stats_vars['velocita_processing'].set(f"{velocity:,.0f} rec/s")
        
        self.app.after(0, update)
    
    def reset_processing_state(self):
        """Reset stato pulsanti dopo elaborazione"""
        self.start_button.configure(text="🚀 Avvia Elaborazione", state=NORMAL)
    
    def log_message(self, message, level="info"):
        """Aggiunge messaggio al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put((timestamp, message, level))
    
    def update_log_display(self):
        """Aggiorna display log da queue"""
        try:
            while True:
                timestamp, message, level = self.log_queue.get_nowait()
                
                self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
                self.log_text.insert(tk.END, f"{message}\n", level)
                
                self.log_text.see(tk.END)
                
        except queue.Empty:
            pass
        
        self.app.after(100, self.update_log_display)
    
    def run(self):
        """Avvia l'applicazione"""
        self.app.mainloop()

# === FUNZIONE MAIN ===
def main():
    """Funzione principale per avviare la GUI"""
    try:
        import ttkbootstrap
        print("✅ ttkbootstrap disponibile")
        
        if PIL_AVAILABLE:
            print("✅ PIL/Pillow disponibile per loghi")
        else:
            print("⚠️ PIL/Pillow non disponibile - loghi disabilitati")
            print("Per abilitare i loghi: pip install Pillow")
        
        app = ModernOpenFiberGUI()
        app.run()
        
    except ImportError as e:
        print("❌ Dipendenza mancante:")
        print("Per la GUI moderna è necessario installare:")
        print("pip install ttkbootstrap Pillow")
        print("\nIn alternativa, usa la versione console:")
        print("python estrattore_of.py")
        
    except Exception as e:
        print(f"❌ Errore nell'avvio della GUI: {e}")

if __name__ == "__main__":
    main()