"""
KMZ Exporter per Google Earth - Analizzatore DB OpenFiber v2.1.1
Genera file KMZ con sedi PAC/PAL e PCN colorati per visualizzazione cartografica
VERSIONE COMPLETA con fix icone e logging live
"""

import os
import re
import zipfile
from datetime import datetime
from collections import defaultdict
import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd

# Import configurazione
from config import PCN_VALLE_AOSTA


class KMZExporter:
    """Generatore KMZ per Google Earth con sedi PAC/PAL e PCN"""
    
    def __init__(self):
        # Colori per PCN (formato KML AABBGGRR - Alpha, Blue, Green, Red)
        self.pcn_colors = [
            'ff0000ff',  # Rosso
            'ff00ff00',  # Verde
            'ffff0000',  # Blu
            'ff00ffff',  # Giallo
            'ffff00ff',  # Magenta
            'ffffff00',  # Ciano
            'ff8000ff',  # Arancione
            'ff0080ff',  # Verde-giallo
            'ff8080ff',  # Rosa
            'ff0080c0',  # Marrone
            'ff8040ff',  # Viola-arancio
            'ff4080ff',  # Rosa-viola
            'ff00c080',  # Verde scuro
            'ffc08000',  # Blu scuro
            'ff8000c0',  # Marrone-viola
            'ff40c0ff',  # Giallo-verde
            'ffc040ff',  # Viola
            'ff4040c0',  # Rosso scuro
            'ff80c040',  # Verde-blu
            'ff404080',  # Marrone scuro
        ]
        
        # Mapping PCN -> Colore
        self.pcn_color_map = {}
        self.assign_pcn_colors()
    
    def assign_pcn_colors(self):
        """Assegna colori univoci ai PCN"""
        pcn_list = list(PCN_VALLE_AOSTA.keys())
        
        for i, pcn_id in enumerate(pcn_list):
            color_index = i % len(self.pcn_colors)
            self.pcn_color_map[pcn_id] = self.pcn_colors[color_index]
        
        print(f"✅ Assegnati colori a {len(pcn_list)} PCN")
    
    def parse_coordinates(self, coordinate_string):
        """
        Converte coordinate COORDINATE_BUILDING in formato Google Earth
        Formato input: N45.123456_E7.123456 o simili
        Formato output: (longitude, latitude, altitude)
        """
        if not coordinate_string or pd.isna(coordinate_string):
            return None
        
        try:
            # Pattern per coordinate N/S + E/W
            pattern = r'([NS])([0-9.]+)_([EW])([0-9.]+)'
            match = re.match(pattern, str(coordinate_string).strip())
            
            if not match:
                return None
            
            lat_dir, lat_val, lon_dir, lon_val = match.groups()
            
            # Converti in decimali
            latitude = float(lat_val)
            longitude = float(lon_val)
            
            # Applica segno per direzione
            if lat_dir == 'S':
                latitude = -latitude
            if lon_dir == 'W':
                longitude = -longitude
            
            # Google Earth: longitude, latitude, altitude
            return (longitude, latitude, 0)
            
        except Exception as e:
            print(f"⚠️ Errore parsing coordinate '{coordinate_string}': {e}")
            return None
    
    def get_pcn_coordinates(self, pcn_id):
        """Ottiene coordinate PCN dal config"""
        pcn_info = PCN_VALLE_AOSTA.get(pcn_id)
        if pcn_info:
            return (pcn_info['longitudine'], pcn_info['latitudine'], 0)
        return None
    
    def create_placemark_style(self, color, icon_type="sede"):
        """Crea stile per segnaposto con icone affidabili"""
        if icon_type == "sede":
            # AGGIORNATO: Icona più affidabile per sedi PAC/PAL
            icon_href = "http://maps.google.com/mapfiles/kml/pal2/icon26.png"  # Edificio governativo
            scale = "1.0"
        else:  # PCN
            # Icona antenna/torre per PCN (funziona già bene)
            icon_href = "http://maps.google.com/mapfiles/kml/shapes/phone.png"
            scale = "1.2"
        
        style = ET.Element("Style")
        
        # IconStyle
        icon_style = ET.SubElement(style, "IconStyle")
        ET.SubElement(icon_style, "color").text = color
        ET.SubElement(icon_style, "scale").text = scale
        
        icon = ET.SubElement(icon_style, "Icon")
        ET.SubElement(icon, "href").text = icon_href
        
        # LabelStyle
        label_style = ET.SubElement(style, "LabelStyle")
        ET.SubElement(label_style, "color").text = color
        ET.SubElement(label_style, "scale").text = "0.8"
        
        return style
    
    def create_placemark(self, name, description, coordinates, style_id):
        """Crea un segnaposto KML"""
        placemark = ET.Element("Placemark")
        
        ET.SubElement(placemark, "name").text = name
        ET.SubElement(placemark, "description").text = description
        ET.SubElement(placemark, "styleUrl").text = f"#{style_id}"
        
        # Point geometry
        point = ET.SubElement(placemark, "Point")
        coord_text = f"{coordinates[0]},{coordinates[1]},{coordinates[2]}"
        ET.SubElement(point, "coordinates").text = coord_text
        
        return placemark
    
    def export_kmz(self, df_data, output_file):
        """
        Esporta DataFrame in formato KMZ per Google Earth - COMPLETO v2.1.1
        
        Args:
            df_data: DataFrame con dati (può essere già filtrato per PAC/PAL o completo)
            output_file: Path file KMZ di output
        """
        try:
            print("🌍 Inizio generazione KMZ per Google Earth...")
            
            # Analisi dati input
            print(f"📊 Dati input: {len(df_data)} record")
            
            if 'STATO_UI' not in df_data.columns:
                print("❌ ERRORE: Colonna STATO_UI non trovata!")
                return False
            
            # Determina se i dati sono già filtrati per PAC/PAL
            stati_ui_unici = df_data['STATO_UI'].unique()
            print(f"📋 STATO_UI presenti: {stati_ui_unici}")
            
            # Se c'è solo STATO_UI=302, i dati sono già filtrati
            if len(stati_ui_unici) == 1 and (302 in stati_ui_unici or '302' in stati_ui_unici):
                print("✅ Dati già filtrati per PAC/PAL")
                df_pac_pal = df_data.copy()
            else:
                # Filtra per PAC/PAL (STATO_UI = 302)
                print("🔍 Filtro per sedi PAC/PAL...")
                
                # Gestisci diversi tipi di dato
                if df_data['STATO_UI'].dtype in ['int64', 'int32']:
                    df_pac_pal = df_data[df_data['STATO_UI'] == 302].copy()
                else:
                    df_pac_pal = df_data[df_data['STATO_UI'] == '302'].copy()
            
            if df_pac_pal.empty:
                print("⚠️ Nessuna sede PAC/PAL trovata (STATO_UI=302)")
                return False
            
            print(f"✅ Trovate {len(df_pac_pal)} sedi PAC/PAL da esportare")
            
            # Raggruppa per comune
            comuni_groups = df_pac_pal.groupby('COMUNE')
            
            # Crea root KML
            kml_root = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
            document = ET.SubElement(kml_root, "Document")
            
            # Nome documento
            data_oggi = datetime.now().strftime("%Y%m%d")
            doc_name = f"Sedi PAC/PAL VdA {data_oggi}"
            ET.SubElement(document, "name").text = doc_name
            ET.SubElement(document, "description").text = (
                f"Sedi PAC/PAL Valle d'Aosta - Generato il {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
                f"Analizzatore DB OpenFiber v2.1.1"
            )
            
            # Crea stili per ogni PCN
            style_counter = 0
            pcn_styles = {}
            sede_styles = {}
            
            for pcn_id, color in self.pcn_color_map.items():
                # Stile per PCN
                pcn_style_id = f"pcn_style_{style_counter}"
                pcn_style = self.create_placemark_style(color, "pcn")
                pcn_style.set("id", pcn_style_id)
                document.append(pcn_style)
                pcn_styles[pcn_id] = pcn_style_id
                
                # Stile per sedi dello stesso PCN
                sede_style_id = f"sede_style_{style_counter}"
                sede_style = self.create_placemark_style(color, "sede")
                sede_style.set("id", sede_style_id)
                document.append(sede_style)
                sede_styles[pcn_id] = sede_style_id
                
                style_counter += 1
            
            # === CARTELLA PRINCIPALE ===
            main_folder = ET.SubElement(document, "Folder")
            ET.SubElement(main_folder, "name").text = doc_name
            ET.SubElement(main_folder, "open").text = "1"
            
            # === CARTELLA PCN con logging live ===
            pcn_folder = ET.SubElement(main_folder, "Folder")
            ET.SubElement(pcn_folder, "name").text = "📡 PCN OpenFiber"
            ET.SubElement(pcn_folder, "open").text = "1"
            
            # Aggiungi PCN unici con logging live
            pcn_aggiunti = set()
            pcn_count = 0
            for _, row in df_pac_pal.iterrows():
                pcn_id = str(row['POP']).strip()
                
                if pcn_id in pcn_aggiunti or pcn_id not in PCN_VALLE_AOSTA:
                    continue
                
                pcn_coords = self.get_pcn_coordinates(pcn_id)
                if not pcn_coords:
                    continue
                
                pcn_info = PCN_VALLE_AOSTA[pcn_id]
                pcn_name = pcn_info['nome']
                pcn_description = (
                    f"<b>PCN:</b> {pcn_name}<br/>"
                    f"<b>ID:</b> {pcn_id}<br/>"
                    f"<b>Comune:</b> {pcn_info['comune']}<br/>"
                    f"<b>Coordinate:</b> {pcn_info['latitudine']:.6f}, {pcn_info['longitudine']:.6f}"
                )
                
                style_id = pcn_styles.get(pcn_id, pcn_styles[list(pcn_styles.keys())[0]])
                
                placemark = self.create_placemark(
                    pcn_name, pcn_description, pcn_coords, style_id
                )
                pcn_folder.append(placemark)
                pcn_aggiunti.add(pcn_id)
                pcn_count += 1
                
                # 🔧 FIX: Log ogni PCN singolarmente per dare "vitalità"
                print(f"📡 PCN aggiunto: {pcn_name}")
            
            print(f"📡 Completati {pcn_count} PCN unici")
            
            # === CARTELLE COMUNI con logging live ===
            sedi_aggiunte = 0
            
            for comune_nome, gruppo_data in comuni_groups:
                # Cartella per comune
                comune_folder = ET.SubElement(main_folder, "Folder")
                ET.SubElement(comune_folder, "name").text = f"🏛️ {comune_nome}"
                ET.SubElement(comune_folder, "open").text = "0"  # Chiuse di default
                
                comune_sedi_count = 0
                for _, row in gruppo_data.iterrows():
                    # Parse coordinate sede
                    coordinate_building = row['COORDINATE_BUILDING']
                    coords = self.parse_coordinates(coordinate_building)
                    
                    if not coords:
                        print(f"⚠️ Coordinate non valide per {row['ID_BUILDING']}: {coordinate_building}")
                        continue
                    
                    # Dati sede
                    sede_name = str(row['ID_BUILDING'])
                    pcn_id = str(row['POP']).strip()
                    
                    sede_description = (
                        f"<b>Sede PAC/PAL</b><br/>"
                        f"<b>ID Building:</b> {row['ID_BUILDING']}<br/>"
                        f"<b>Indirizzo:</b> {row['INDIRIZZO']} {row['CIVICO']}<br/>"
                        f"<b>Comune:</b> {comune_nome}<br/>"
                        f"<b>PCN:</b> {row['NOME_PCN']}<br/>"
                        f"<b>ISTAT:</b> {row['ISTAT']}<br/>"
                        f"<b>Coordinate:</b> {coordinate_building}"
                    )
                    
                    # Stile basato su PCN
                    style_id = sede_styles.get(pcn_id, sede_styles[list(sede_styles.keys())[0]])
                    
                    # Crea placemark
                    placemark = self.create_placemark(
                        sede_name, sede_description, coords, style_id
                    )
                    
                    comune_folder.append(placemark)
                    comune_sedi_count += 1
                    sedi_aggiunte += 1
                
                # 🔧 FIX: Log ogni comune singolarmente per dare "vitalità"
                if comune_sedi_count > 0:
                    print(f"🏛️ Comune {comune_nome}: {comune_sedi_count} sedi aggiunte")
            
            print(f"✅ Totale sedi PAC/PAL aggiunte: {sedi_aggiunte}")
            
            # === GENERA FILE KMZ ===
            return self.save_kmz(kml_root, output_file)
            
        except Exception as e:
            print(f"❌ Errore durante generazione KMZ: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def save_kmz(self, kml_root, output_file):
        """Salva KML in file KMZ compresso"""
        try:
            print(f"💾 Salvataggio KMZ: {output_file}")
            
            # Assicura che la directory esista
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Converti a stringa XML formattata
            rough_string = ET.tostring(kml_root, encoding='utf-8')
            reparsed = minidom.parseString(rough_string)
            kml_content = reparsed.toprettyxml(indent="  ", encoding='utf-8')
            
            # Rimuovi riga vuota dopo XML declaration
            kml_content = b'\n'.join(line for line in kml_content.split(b'\n') if line.strip())
            
            # Crea file KMZ (ZIP con KML dentro)
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as kmz_file:
                kmz_file.writestr('doc.kml', kml_content)
            
            # Verifica che il file sia stato creato
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file) / 1024  # KB
                print(f"✅ File KMZ salvato: {os.path.basename(output_file)} ({file_size:.1f} KB)")
                return True
            else:
                print(f"❌ File non creato: {output_file}")
                return False
            
        except Exception as e:
            print(f"❌ Errore salvataggio KMZ: {e}")
            return False


# === FUNZIONI STANDALONE ===

def genera_kmz_pac_pal(df_data, output_file):
    """
    Funzione standalone per generare KMZ delle sedi PAC/PAL
    
    Args:
        df_data: DataFrame con dati Valle d'Aosta (completi o già filtrati per PAC/PAL)
        output_file: Path del file KMZ di output
    
    Returns:
        bool: True se successo, False se errore
    """
    exporter = KMZExporter()
    return exporter.export_kmz(df_data, output_file)


def test_kmz_export():
    """Funzione di test per il modulo KMZ con dati fake"""
    print("🧪 Test KMZ Exporter...")
    
    # Dati di test fake
    test_data = pd.DataFrame([
        {
            'COMUNE': 'Aosta',
            'ISTAT': '007003',
            'INDIRIZZO': 'Via Test',
            'CIVICO': '123',
            'ID_BUILDING': 'TEST_001',
            'COORDINATE_BUILDING': 'N45.737649_E7.320166',
            'STATO_UI': '302',
            'POP': 'AOCUA',
            'NOME_PCN': 'POP_AO_11_VERRES'
        },
        {
            'COMUNE': 'Verrès',
            'ISTAT': '007073',
            'INDIRIZZO': 'Via Prova',
            'CIVICO': '456',
            'ID_BUILDING': 'TEST_002',
            'COORDINATE_BUILDING': 'N45.661442_E7.691030',
            'STATO_UI': '302',
            'POP': 'AOAGA',
            'NOME_PCN': 'POP_AO_07_DONNAS'
        }
    ])
    
    output_test = "test_kmz_fake.kmz"
    success = genera_kmz_pac_pal(test_data, output_test)
    
    if success:
        print("✅ Test modulo KMZ completato!")
        if os.path.exists(output_test):
            os.remove(output_test)  # Cleanup
        return True
    else:
        print("❌ Test modulo KMZ fallito!")
        return False


if __name__ == "__main__":
    test_kmz_export()