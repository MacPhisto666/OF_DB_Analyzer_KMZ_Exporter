# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **OpenFiber DB Analyzer v2.1.1** - a specialized data extraction and analysis tool for processing OpenFiber's national FTTH coverage database. The application processes large CSV files (1.5GB+) to extract, enrich, and export Valle d'Aosta region data with geographic and infrastructure information.

## Core Architecture

### Module Structure
- **`estrattore_of.py`**: Core extraction engine with chunked CSV processing, data enrichment, and Excel export
- **`estrattore_of_GUI.py`**: Modern GUI application with fullscreen interface, progress tracking, and logo support
- **`kmz_exporter.py`**: Google Earth KMZ export module for geographic visualization
- **`config.py`**: Centralized configuration with municipality mappings, PCN data, and UI state codes

### Data Processing Pipeline
1. **CSV Reading**: Chunked processing (default 10,000 rows) to handle large files
2. **Region Filtering**: Automatic extraction of region 02 (Valle d'Aosta)
3. **Data Enrichment**: Municipality name mapping (ISTAT codes → Italian names) and PCN coordinate integration
4. **Output Generation**: Multi-sheet Excel files and optional KMZ for Google Earth

## Development Commands

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
# GUI version (recommended)
cd src
python estrattore_of_GUI.py

# Console version
cd src
python estrattore_of.py
```

### Testing
```bash
# Test KMZ export functionality
cd src
python test_excel_to_kmz.py

# Test integration
cd src
python test_kmz_integration.py
```

## Key Configuration

### Required Data Files
- Place large CSV input files in `data/` directory (ignored by Git)
- Optional logos: `data/logo_azienda.png` and `data/logo_openfiber.png`
- Output files are generated in `output/` directory (ignored by Git)

### Main Parameters (`estrattore_of.py`)
- `chunk_size`: Memory optimization (default 10,000 rows)
- `export_kmz`: Enable Google Earth KMZ generation
- Automatic timestamp naming: Files include YYYYMMDD format

### Dependencies
- **Core**: pandas, openpyxl for data processing and Excel export
- **GUI**: ttkbootstrap for modern interface, Pillow for logo handling
- **Optional**: KMZ export requires xml.etree.ElementTree (built-in)

## Data Mappings

### Municipality Integration
- 74 Valle d'Aosta municipalities mapped via ISTAT codes in `config.py:COMUNI_VALLE_AOSTA`
- Automatic conversion from numeric codes to Italian names

### PCN Infrastructure Data
- 42 PCN (Point of Connection) locations with GPS coordinates in `config.py:PCN_VALLE_AOSTA`
- Automatic join via POP field for infrastructure enrichment

### UI State Codes
- STATO_UI filtering: 302 (Public Administration), 102 (Residential)
- Complete state code reference in `config.py:STATI_UI`

## Development Notes

### Performance Characteristics
- Processes ~30,000 rows/second
- 770K row dataset completes in ~45 seconds
- Memory-efficient chunked processing for large files

### GUI Features
- Fullscreen launch with modern dark theme
- Live progress tracking with queue-based logging
- Optional KMZ export checkbox
- Integrated logo display system

### File Structure
- Input files: `data/` (excluded from Git)
- Output files: `output/` (excluded from Git)
- All source code: `src/`
- Documentation: `docs/`

## Testing Strategy

The project includes integration tests for KMZ export functionality. Run tests from the `src/` directory to ensure proper module path resolution.