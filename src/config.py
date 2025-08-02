"""
Configurazione Analizzatore DB OpenFiber
Centralizza tutti i parametri configurabili del progetto
"""

import os

# =============================================================================
# CONFIGURAZIONE PATHS
# =============================================================================

# Directory base del progetto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Paths relativi
PATHS = {
    'data_dir': os.path.join(BASE_DIR, 'data'),
    'output_dir': os.path.join(BASE_DIR, 'output'),
    'logs_dir': os.path.join(BASE_DIR, 'logs'),
    'docs_dir': os.path.join(BASE_DIR, 'docs'),
}

# File di default
DEFAULT_FILES = {
    'input_csv': 'dbcopertura_CD_20250715.csv',
    'output_excel': 'valle_aosta_estratto.xlsx',
    'log_file': 'estrattore.log'
}

# =============================================================================
# CONFIGURAZIONE ELABORAZIONE
# =============================================================================

# Parametri performance
PROCESSING = {
    'chunk_size': 10000,        # Righe per chunk (bilanciamento memoria/velocità)
    'progress_interval': 10,     # Mostra progress ogni N chunks
    'extract_progress': 1000,    # Mostra conteggio ogni N record estratti
}

# Ottimizzazioni per diversi sistemi
CHUNK_SIZE_PROFILES = {
    'low_memory': 5000,      # Sistemi con poca RAM
    'balanced': 10000,       # Default - buon compromesso
    'high_performance': 25000,  # Sistemi performanti
    'maximum': 50000         # Performance massime (richiede molta RAM)
}

# =============================================================================
# CONFIGURAZIONE DATI CSV
# =============================================================================

# Formato CSV OpenFiber
CSV_CONFIG = {
    'separator': '|',           # Separatore colonne
    'encoding': 'utf-8',        # Encoding file
    'dtype': 'str',            # Forza tutto come stringa
    'low_memory': False         # Disabilita ottimizzazioni che causano warning
}

# Schema colonne CSV (ordine importante)
CSV_COLUMNS = [
    'ID_SCALA',
    'REGIONE', 
    'PROVINCIA',
    'COMUNE',
    'FRAZIONE',
    'PARTICELLA_TOP',
    'INDIRIZZO',
    'CIVICO',
    'SCALA_PALAZZINA',
    'CODICE_VIA',
    'ID_BUILDING',
    'COORDINATE_BUILDING',
    'POP',
    'TOTALE_UI',
    'STATO_UI',
    'STATO_SCALA_PALAZZINA',
    'DATA_RFC_INDICATIVA',
    'DATA_RFC_EFFETTIVA',
    'DATA_RFA_INDICATIVA',
    'DATA_RFA_EFFETTIVA',
    'DATA_ULTIMA_MODIFICA_RECORD',
    'DATA_ULTIMA_VARIAZIONE_STATO_BUILDING',
    'DATA_ULTIMA_VARIAZIONE_STATO_SCALA_PALAZZINA',
    'ID_EGON_CIVICO',
    'ID_EGON_STRADA'
]

# =============================================================================
# CODICI REGIONI E STATI
# =============================================================================

# Codici regione documentati
REGIONI = {
    '01': 'Piemonte',
    '02': 'Valle d\'Aosta', 
    '03': 'Lombardia',
    '04': 'Trentino-Alto Adige',
    '05': 'Veneto',
    '06': 'Friuli-Venezia Giulia',
    '07': 'Liguria',
    '08': 'Emilia-Romagna',
    '09': 'Toscana',
    '10': 'Umbria',
    '11': 'Marche',
    '12': 'Lazio',
    '13': 'Abruzzo',
    '14': 'Molise',
    '15': 'Campania',
    '16': 'Puglia',
    '17': 'Basilicata',
    '18': 'Calabria',
    '19': 'Sicilia',
    '20': 'Sardegna'
}

# Comuni Valle d'Aosta - Mappatura codice ISTAT -> nome
# Aggiornato da file ISTAT comuni italiani
COMUNI_VALLE_AOSTA = {
    '007001': 'Allein',
    '007002': 'Antey-Saint-André',
    '007003': 'Aosta',
    '007004': 'Arnad',
    '007005': 'Arvier',
    '007006': 'Avise',
    '007007': 'Ayas',
    '007008': 'Aymavilles',
    '007009': 'Bard',
    '007010': 'Bionaz',
    '007011': 'Brissogne',
    '007012': 'Brusson',
    '007013': 'Challand-Saint-Anselme',
    '007014': 'Challand-Saint-Victor',
    '007015': 'Chambave',
    '007016': 'Chamois',
    '007017': 'Champdepraz',
    '007018': 'Champorcher',
    '007019': 'Charvensod',
    '007020': 'Châtillon',
    '007021': 'Cogne',
    '007022': 'Courmayeur',
    '007023': 'Donnas',
    '007024': 'Doues',
    '007025': 'Emarèse',
    '007026': 'Etroubles',
    '007027': 'Fénis',
    '007028': 'Fontainemore',
    '007029': 'Gaby',
    '007030': 'Gignod',
    '007031': 'Gressan',
    '007032': 'Gressoney-La-Trinité',
    '007033': 'Gressoney-Saint-Jean',
    '007034': 'Hône',
    '007035': 'Introd',
    '007036': 'Issime',
    '007037': 'Issogne',
    '007038': 'Jovençan',
    '007039': 'La Magdeleine',
    '007040': 'La Salle',
    '007041': 'La Thuile',
    '007042': 'Lillianes',
    '007043': 'Montjovet',
    '007044': 'Morgex',
    '007045': 'Nus',
    '007046': 'Ollomont',
    '007047': 'Oyace',
    '007048': 'Perloz',
    '007049': 'Pollein',
    '007050': 'Pontboset',
    '007051': 'Pontey',
    '007052': 'Pont-Saint-Martin',
    '007053': 'Pré-Saint-Didier',
    '007054': 'Quart',
    '007055': 'Rhêmes-Notre-Dame',
    '007056': 'Rhêmes-Saint-Georges',
    '007057': 'Roisan',
    '007058': 'Saint-Christophe',
    '007059': 'Saint-Denis',
    '007060': 'Saint-Marcel',
    '007061': 'Saint-Nicolas',
    '007062': 'Saint-Oyen',
    '007063': 'Saint-Pierre',
    '007064': 'Saint-Rhémy-en-Bosses',
    '007065': 'Saint-Vincent',
    '007066': 'Sarre',
    '007067': 'Torgnon',
    '007068': 'Valgrisenche',
    '007069': 'Valpelline',
    '007070': 'Valsavarenche',
    '007071': 'Valtournenche',
    '007072': 'Verrayes',
    '007073': 'Verrès',
    '007074': 'Villeneuve'
}

# PCN Valle d'Aosta - Mappatura ID PCN -> dati completi
# Aggiornato da file "PCN 250715.xlsx" OpenFiber
PCN_VALLE_AOSTA = {
    'AOCUA': {
        'nome': 'POP_AO_11_VERRES',
        'comune': 'Verrès',
        'latitudine': 45.661442,
        'longitudine': 7.69103
    },
    'AOAGA': {
        'nome': 'POP_AO_07_DONNAS',
        'comune': 'Donnas',
        'latitudine': 45.603989,
        'longitudine': 7.775326
    },
    'AOALA': {
        'nome': 'POP_AO_04_AYAS',
        'comune': 'Ayas',
        'latitudine': 45.797209,
        'longitudine': 7.695367
    },
    'AOCCA': {
        'nome': 'POP_AO_09_RHEMES_NOTRE_DAMES',
        'comune': 'Rhêmes-Notre-Dame',
        'latitudine': 45.578314,
        'longitudine': 7.122699
    },
    'AOBJ1': {
        'nome': 'POP_AO_27_ISSIME',
        'comune': 'Issime',
        'latitudine': 45.684445,
        'longitudine': 7.854775
    },
    'AOAZ1': {
        'nome': 'POP_AO_16_EMARÈSE',
        'comune': 'Emarèse',
        'latitudine': 45.731543,
        'longitudine': 7.715043
    },
    'AOBXA': {
        'nome': 'POP_AO_28_PONTBOSET',
        'comune': 'Pontboset',
        'latitudine': 45.606504,
        'longitudine': 7.687544
    },
    'AOBPA': {
        'nome': 'POP_AO_26_LILLIANES',
        'comune': 'Lillianes',
        'latitudine': 45.633319,
        'longitudine': 7.845082
    },
    'AOBVA': {
        'nome': 'POP_AO_24_PERLOZ',
        'comune': 'Perloz',
        'latitudine': 45.604174,
        'longitudine': 7.803198
    },
    'AOBMA': {
        'nome': 'POP_AO_18_LA_MAGDELEINE',
        'comune': 'La Magdeleine',
        'latitudine': 45.811125,
        'longitudine': 7.619954
    },
    'AOARA': {
        'nome': 'POP_AO_25_CHAMBAVE',
        'comune': 'Chambave',
        'latitudine': 45.744122,
        'longitudine': 7.547691
    },
    'AOCEA': {
        'nome': 'POP_AO_01_ROISAN',
        'comune': 'Roisan',
        'latitudine': 45.783543,
        'longitudine': 7.308608
    },
    'AOAWA': {
        'nome': 'POP_AO_02_CHATILLON',
        'comune': 'Châtillon',
        'latitudine': 45.74542,
        'longitudine': 7.609981
    },
    'AOAUA': {
        'nome': 'POP_AO_29_CHAMPORCHER',
        'comune': 'Champorcher',
        'latitudine': 45.622629,
        'longitudine': 7.636796
    },
    'AOBYA': {
        'nome': 'POP_AO_34_PONTEY',
        'comune': 'Pontey',
        'latitudine': 45.738504,
        'longitudine': 7.59147
    },
    'AOBGA': {
        'nome': 'POP_AO_22_GRESSONEY-LA-TRINITÈ',
        'comune': 'Gressoney-La-Trinité',
        'latitudine': 45.826537,
        'longitudine': 7.825449
    },
    'AOBDA': {
        'nome': 'POP_AO_19_GABY',
        'comune': 'Gaby',
        'latitudine': 45.714555,
        'longitudine': 7.881129
    },
    'AOAXA': {
        'nome': 'POP_AO_14_COGNE',
        'comune': 'Cogne',
        'latitudine': 45.611333,
        'longitudine': 7.350789
    },
    'AOAFA': {
        'nome': 'POP_AO_08_GRESSONEY_SAINT_JEAN',
        'comune': 'Gressoney-Saint-Jean',
        'latitudine': 45.774432,
        'longitudine': 7.825705
    },
    'AOBIA': {
        'nome': 'POP_AO_35_INTROD',
        'comune': 'Introd',
        'latitudine': 45.696833,
        'longitudine': 7.187801
    },
    'AOCIA': {
        'nome': 'POP_AO_32_SAINT-NICOLAS',
        'comune': 'Saint-Nicolas',
        'latitudine': 45.709708,
        'longitudine': 7.198002
    },
    'AOAJA': {
        'nome': 'POP_AO_33_ARVIER',
        'comune': 'Arvier',
        'latitudine': 45.703663,
        'longitudine': 7.16933
    },
    'AOAHA': {
        'nome': 'POP_AO_48_ALLEIN',
        'comune': 'Allein',
        'latitudine': 45.80852,
        'longitudine': 7.271741
    },
    'AOCGA': {
        'nome': 'POP_AO_49_SAINT_DENIS',
        'comune': 'Saint-Denis',
        'latitudine': 45.75249,
        'longitudine': 7.556964
    },
    'AOCQA': {
        'nome': 'POP_AO_42_VALPELLINE',
        'comune': 'Valpelline',
        'latitudine': 45.826005,
        'longitudine': 7.323694
    },
    'AOANA': {
        'nome': 'POP_AO_43_BIONAZ',
        'comune': 'Bionaz',
        'latitudine': 45.864615,
        'longitudine': 7.398061
    },
    'AOBUA': {
        'nome': 'POP_AO_47_OYACE',
        'comune': 'Oyace',
        'latitudine': 45.85057,
        'longitudine': 7.381835
    },
    'AOCKA': {
        'nome': 'POP_AO_03_SAINT_PIERRE',
        'comune': 'Saint-Pierre',
        'latitudine': 45.708333,
        'longitudine': 7.222765
    },
    'AOABA': {
        'nome': 'POP_AO_36_ANTEY_SAINT_ANDRE',
        'comune': 'Antey-Saint-André',
        'latitudine': 45.806803,
        'longitudine': 7.587768
    },
    'AOASA': {
        'nome': 'POP_AO_30_CHAMOIS',
        'comune': 'Chamois',
        'latitudine': 45.83726,
        'longitudine': 7.623829
    },
    'AOBSA': {
        'nome': 'POP_AO_44_NUS',
        'comune': 'Nus',
        'latitudine': 45.740152,
        'longitudine': 7.466732
    },
    'AOCHA': {
        'nome': 'POP_AO_51_SAINT_MARCEL',
        'comune': 'Saint-Marcel',
        'latitudine': 45.731502,
        'longitudine': 7.444186
    },
    'AOBAA': {
        'nome': 'POP_AO_40_ETROUBLES',
        'comune': 'Etroubles',
        'latitudine': 45.821179,
        'longitudine': 7.229843
    },
    'AOCLA': {
        'nome': 'POP_AO_41_SAINT-RHÈMY-EN-BOSSES',
        'comune': 'Saint-Rhémy-en-Bosses',
        'latitudine': 45.821056,
        'longitudine': 7.178117
    },
    'AOAVA': {
        'nome': 'POP_AO_46_CHARVENSOD',
        'comune': 'Charvensod',
        'latitudine': 45.727882,
        'longitudine': 7.333152
    },
    'AOCPA': {
        'nome': 'POP_AO_10_VALGRISENCHE',
        'comune': 'Valgrisenche',
        'latitudine': 45.637025,
        'longitudine': 7.068104
    },
    'AOACA': {
        'nome': 'POP_AO_31_AYMAVILLES',
        'comune': 'Aymavilles',
        'latitudine': 45.701166,
        'longitudine': 7.239455
    },
    'AOBWA': {
        'nome': 'POP_AO_50_POLLEIN',
        'comune': 'Pollein',
        'latitudine': 45.728804,
        'longitudine': 7.3572
    },
    'AOBOA': {
        'nome': 'POP_AO_13_LA_THUILE',
        'comune': 'La Thuile',
        'latitudine': 45.713989,
        'longitudine': 6.950893
    },
    'AOAYA': {
        'nome': 'POP_AO_52_DOUES',
        'comune': 'Doues',
        'latitudine': 45.816728,
        'longitudine': 7.305688
    },
    'AOCBA': {
        'nome': 'POP_AO_15_QUART',
        'comune': 'Quart',
        'latitudine': 45.743229,
        'longitudine': 7.387108
    },
    'AOBFA': {
        'nome': 'POP_AO_45_GRESSAN',
        'comune': 'Gressan',
        'latitudine': 45.721333,
        'longitudine': 7.289556
    }
}

# Stati UI documentati (Specifiche OF_DB_Copertura_CD v1.7)
STATI_UI = {
    '101': 'Sede FTTH - NON VENDIBILE',
    '102': 'Sede FTTH',
    '201': 'Sede FWA - NON VENDIBILE',
    '202': 'Sede FWA',
    '205': 'Sede FWA - TRANSITORIO',
    '302': 'Sede PAC/PAL',
    '80': 'Prevendibilità', 
    '602': 'FTTH - Easy Delivery',  
    '603': 'FTTH - Uso Futuro',  
    '604': 'FTTH - Uso Futuro',  
    '902': 'FWA - Uso Futuro',  
    '905': 'FWA - Uso Futuro',  
 
}

# Stati scala/palazzina
STATI_SCALA = {
    '100': 'Non definito',
    '101': 'Pianificato',
    '102': 'In costruzione',
    '200': 'Attivo',
    '201': 'In corso',
    '202': 'Non attivo'
}

# =============================================================================
# CONFIGURAZIONE OUTPUT
# =============================================================================

# Formati di output supportati
OUTPUT_FORMATS = {
    'excel': {
        'extension': '.xlsx',
        'engine': 'openpyxl',
        'parameters': {'index': False}
    },
    'csv': {
        'extension': '.csv', 
        'separator': ';',
        'parameters': {'index': False, 'encoding': 'utf-8'}
    }
}

# Colonne essenziali per output ridotto
ESSENTIAL_COLUMNS = [
    'ID_SCALA',
    'REGIONE',
    'PROVINCIA', 
    'COMUNE',
    'INDIRIZZO',
    'CIVICO',
    'COORDINATE_BUILDING',
    'STATO_UI',
    'STATO_SCALA_PALAZZINA',
    'DATA_RFC_EFFETTIVA',
    'DATA_RFA_EFFETTIVA'
]

# =============================================================================
# CONFIGURAZIONE FILTRI
# =============================================================================

# Filtri predefiniti comuni
FILTRI_COMUNI = {
    'solo_coperti': {
        'STATO_UI': ['200', '201'],
        'description': 'Solo edifici con copertura attiva o in corso'
    },
    'solo_pianificati': {
        'STATO_UI': ['101', '102'],
        'description': 'Solo edifici pianificati o in costruzione'
    },
    'tutti_attivi': {
        'STATO_SCALA_PALAZZINA': ['200'],
        'description': 'Solo scale/palazzine attive'
    }
}

# Filtri predefiniti per tipologie comuni
FILTRI_TIPOLOGIE_SEDE = {
    'ftth_vendibili': {
        'codici': ['102'],
        'descrizione': '🏠 FTTH Vendibili',
        'tooltip': 'Solo sedi FTTH vendibili'
    },
    'ftth_tutti': {
        'codici': ['101', '102'],
        'descrizione': '🌐 FTTH Tutte',
        'tooltip': 'Tutte le sedi FTTH (vendibili e non)'
    },
    'fwa_vendibili': {
        'codici': ['202'],
        'descrizione': '📡 FWA Vendibili',
        'tooltip': 'Solo sedi FWA vendibili'
    },
    'fwa_tutti': {
        'codici': ['201', '202', '205'],
        'descrizione': '📶 FWA Tutte',
        'tooltip': 'Tutte le sedi FWA'
    },
    'pac_pal': {
        'codici': ['302'],
        'descrizione': '🏛️ PAC/PAL',
        'tooltip': 'Solo sedi Pubblica Amministrazione'
    },
    'prevendibili': {
        'codici': ['80'],
        'descrizione': '⏳ Prevendibilità',
        'tooltip': 'Sedi in prevendibilità'
    },
    'easy_delivery': {
        'codici': ['602'],
        'descrizione': '🚚 Easy Delivery',
        'tooltip': 'FTTH Easy Delivery'
    },
    'uso_futuro': {
        'codici': ['603', '604', '902', '905'],
        'descrizione': '🔮 Uso Futuro',
        'tooltip': 'Sedi pianificate per uso futuro'
    },
    'vendibili_tutti': {
        'codici': ['102', '202', '302'],
        'descrizione': '💰 Vendibili (FTTH+FWA+PAC)',
        'tooltip': 'Tutte le sedi attualmente vendibili'
    },
    'tutti_stati': {
        'codici': list(STATI_UI.keys()),
        'descrizione': '🌍 Tutti gli Stati',
        'tooltip': 'Tutti gli stati disponibili'
    }
}


# Filtri specifici per comuni Valle d'Aosta
FILTRI_COMUNI_VDA = {
    'solo_aosta': {
        'COMUNE': ['007003'],
        'description': 'Solo il comune di Aosta'
    },
    'comuni_turistici': {
        'COMUNE': ['007022', '007041', '007053', '007021'],  # Courmayeur, La Thuile, Pré-Saint-Didier, Cogne
        'description': 'Principali comuni turistici montani'
    },
    'area_metropolitana': {
        'COMUNE': ['007003', '007019', '007031', '007049', '007058'],  # Aosta, Charvensod, Gressan, Pollein, Saint-Christophe
        'description': 'Area metropolitana di Aosta'
    },
    'valle_centrale': {
        'COMUNE': ['007003', '007008', '007027', '007045', '007054', '007058', '007063'],
        'description': 'Comuni della valle centrale'
    }
}

# =============================================================================
# CONFIGURAZIONE LOGGING
# =============================================================================

LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'console_output': True,
    'file_output': True
}

# =============================================================================
# CONFIGURAZIONE SVILUPPO
# =============================================================================

# Flag per ambiente di sviluppo
DEBUG = False
VERBOSE = True

# Test files (file piccoli per sviluppo)
TEST_FILES = {
    'small_sample': 'test_sample_small.csv',
    'valle_aosta_only': 'dbcopertura_CD_20250715_valle_d_aostaRidotto.csv'
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_full_path(path_type, filename=None):
    """
    Restituisce il path completo per un tipo di file
    
    Args:
        path_type: Tipo di path ('data_dir', 'output_dir', etc.)
        filename: Nome file opzionale
    
    Returns:
        Path completo
    """
    base_path = PATHS.get(path_type, '')
    if filename:
        return os.path.join(base_path, filename)
    return base_path

def get_regione_name(codice_regione):
    """
    Restituisce il nome della regione dal codice
    
    Args:
        codice_regione: Codice regione (es. '02')
    
    Returns:
        Nome regione o 'Regione sconosciuta'
    """
    return REGIONI.get(codice_regione, f'Regione sconosciuta ({codice_regione})')

def get_comune_name(codice_comune):
    """
    Restituisce il nome del comune dal codice ISTAT (solo Valle d'Aosta)
    
    Args:
        codice_comune: Codice ISTAT comune (es. '007003')
    
    Returns:
        Nome comune o 'Comune sconosciuto'
    """
    return COMUNI_VALLE_AOSTA.get(codice_comune, f'Comune sconosciuto ({codice_comune})')

def get_pcn_info(id_pcn):
    """
    Restituisce le informazioni complete del PCN dall'ID
    
    Args:
        id_pcn: ID PCN (es. 'AOCUA')
    
    Returns:
        Dict con nome, comune, latitudine, longitudine o None se non trovato
    """
    return PCN_VALLE_AOSTA.get(id_pcn, None)

def get_pcn_name(id_pcn):
    """
    Restituisce il nome del PCN dall'ID
    
    Args:
        id_pcn: ID PCN (es. 'AOCUA')
    
    Returns:
        Nome PCN o 'PCN sconosciuto'
    """
    pcn_info = PCN_VALLE_AOSTA.get(id_pcn)
    if pcn_info:
        return pcn_info['nome']
    return f'PCN sconosciuto ({id_pcn})'

def get_pcn_coordinates(id_pcn):
    """
    Restituisce le coordinate GPS del PCN
    
    Args:
        id_pcn: ID PCN (es. 'AOCUA')
    
    Returns:
        Tuple (latitudine, longitudine) o (None, None) se non trovato
    """
    pcn_info = PCN_VALLE_AOSTA.get(id_pcn)
    if pcn_info:
        return (pcn_info['latitudine'], pcn_info['longitudine'])
    return (None, None)

def get_stato_ui_description(codice_stato):
    """
    Restituisce la descrizione dello stato UI dal codice
    
    Args:
        codice_stato: Codice stato UI (es. '102', '302')
    
    Returns:
        Descrizione stato o 'Stato sconosciuto'
    """
    return STATI_UI.get(codice_stato, f'Stato sconosciuto ({codice_stato})')

def get_sedi_pac_pal(df):
    """
    Filtra DataFrame per ottenere solo sedi PAC/PAL (codice 302)
    
    Args:
        df: DataFrame con colonna STATO_UI
    
    Returns:
        DataFrame filtrato per sole sedi PA
    """
    return df[df['STATO_UI'] == '302']

# Filtri specifici per tipologie di sede
FILTRI_TIPOLOGIE_SEDE = {
    'solo_pac_pal': {
        'STATO_UI': ['302'],
        'description': 'Solo sedi Pubblica Amministrazione (PAC/PAL)'
    },
    'solo_residenziali': {
        'STATO_UI': ['102'],
        'description': 'Solo sedi residenziali'
    },
    'sedi_pubbliche_e_residenziali': {
        'STATO_UI': ['102', '302'],
        'description': 'Sedi residenziali + Pubblica Amministrazione'
    }
}

def get_all_pcn_valle_aosta():
    """
    Restituisce tutti i PCN della Valle d'Aosta
    
    Returns:
        Dict completo ID->info PCN Valle d'Aosta
    """
    return PCN_VALLE_AOSTA.copy()

def get_comuni_by_name_pattern(pattern):
    """
    Trova comuni Valle d'Aosta che contengono un pattern nel nome
    
    Args:
        pattern: Stringa da cercare nel nome (case insensitive)
    
    Returns:
        Dict con codici e nomi dei comuni trovati
    """
    pattern_lower = pattern.lower()
    result = {}
    
    for codice, nome in COMUNI_VALLE_AOSTA.items():
        if pattern_lower in nome.lower():
            result[codice] = nome
            
    return result

def get_all_comuni_valle_aosta():
    """
    Restituisce tutti i comuni della Valle d'Aosta
    
    Returns:
        Dict completo codice->nome comuni Valle d'Aosta
    """
    return COMUNI_VALLE_AOSTA.copy()

def validate_config():
    """
    Valida la configurazione e crea directory necessarie
    
    Returns:
        bool: True se configurazione valida
    """
    try:
        # Crea directory se non esistono
        for path_type, path in PATHS.items():
            os.makedirs(path, exist_ok=True)
            
        # Verifica parametri critici
        assert PROCESSING['chunk_size'] > 0, "chunk_size deve essere positivo"
        assert CSV_CONFIG['separator'], "separator non può essere vuoto"
        
        return True
        
    except Exception as e:
        print(f"❌ Errore validazione configurazione: {e}")
        return False

# Valida configurazione all'import
if __name__ == '__main__':
    if validate_config():
        print("✅ Configurazione valida")
    else:
        print("❌ Configurazione non valida")