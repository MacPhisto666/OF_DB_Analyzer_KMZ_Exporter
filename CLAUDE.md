# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **OpenFiber DB Analyzer v2.1.1** - a specialized data extraction and analysis tool for processing OpenFiber's national FTTH coverage database. The application processes large CSV files (1.5GB+) to extract, enrich, and export Valle d'Aosta region data with geographic and infrastructure information.

## Core Architecture

### Module Structure
- **`estrattore_of.py`**: Core extraction engine with chunked CSV processing, data enrichment, and Excel export
  - Function `estrai_regione_02()`: Main processing function with optional KMZ export
  - Function `process_record()`: Individual record enrichment with PCN/municipality mapping
  - Function `sanitize_sheet_name()`: Excel-safe worksheet naming
- **`estrattore_of_GUI.py`**: Modern GUI application with fullscreen interface, progress tracking, and logo support
  - Class `ModernOpenFiberGUI`: Main GUI application with ttkbootstrap theming
  - Class `StdoutRedirector`: Thread-safe stdout redirection for live logging
  - Threading implementation for non-blocking UI during processing
- **`kmz_exporter.py`**: Google Earth KMZ export module for geographic visualization
  - Class `KMZExporter`: Complete KMZ generation with color-coded PCN mapping
  - Function `genera_kmz_pac_pal()`: High-level export function
  - Coordinate parsing for OpenFiber format (N45.123_E7.456)
- **`config.py`**: Centralized configuration with municipality mappings, PCN data, and UI state codes
  - `COMUNI_VALLE_AOSTA`: 74 municipality mappings (ISTAT → Italian names)
  - `PCN_VALLE_AOSTA`: 42 PCN locations with GPS coordinates
  - `STATI_UI`: Complete reference of UI state codes

### Data Processing Pipeline
1. **CSV Reading**: Chunked processing (default 10,000 rows) to handle large files efficiently
2. **Region Filtering**: Automatic extraction of region 02 (Valle d'Aosta) from national dataset
3. **Data Enrichment**: Municipality name mapping (ISTAT codes → Italian names) and PCN coordinate integration
4. **Output Generation**: Multi-sheet Excel files (one per municipality) and optional KMZ for Google Earth
5. **File Naming**: Automatic timestamp-based naming (YYYYMMDD format)

## Development Commands

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
# GUI version (recommended) - launches fullscreen
cd src
python estrattore_of_GUI.py

# Console version with direct CSV processing
cd src
python estrattore_of.py
```

### Building Executable
```bash
# Install PyInstaller (if not already installed)
pip install pyinstaller

# Build using automated script
python build_executable.py

# Alternative: Use batch script (Windows)
crea_eseguibile.bat
```

### Testing
```bash
# Test KMZ export functionality (requires existing Excel file)
cd src
python test_excel_to_kmz.py

# Test integration with mock data
cd src
python test_kmz_integration.py
```

### Development Testing
```bash
# Quick functionality test (from project root)
cd src && python estrattore_of.py

# GUI development test
cd src && python estrattore_of_GUI.py
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
- Configurable chunk sizes in `config.py:CHUNK_SIZE_PROFILES`

### GUI Implementation Details
- **Framework**: ttkbootstrap with "superhero" dark theme
- **Threading**: Queue-based communication between worker and UI threads
- **Logging**: Custom `StdoutRedirector` for real-time progress updates
- **Fullscreen**: Automatic `zoomed` state on launch
- **Logo Support**: PIL/Pillow for dynamic logo loading and resizing

### KMZ Export Architecture
- **Color System**: 20 rotating colors for PCN differentiation
- **Coordinate Parsing**: Custom regex for OpenFiber format (N45.123_E7.456)
- **File Structure**: Hierarchical folders (PCN folder + municipality folders)
- **Icon System**: Google Maps icons for buildings and phones

### File Structure and Git Strategy
- **Input files**: `data/` (ignored by Git due to size)
- **Output files**: `output/` (ignored by Git - local results)
- **Build artifacts**: `build/`, `dist/`, `*_Portable/` (ignored by Git)
- **Source code**: `src/` (tracked in Git)
- **Documentation**: `docs/` (tracked in Git)
- **Executable creation**: PyInstaller with custom `.spec` file

### Code Conventions
- **Error Handling**: Graceful degradation for missing dependencies (KMZ, PIL)
- **Import Strategy**: Optional imports with feature detection
- **Configuration**: Centralized in `config.py` with logical grouping
- **Logging**: Timestamp-prefixed messages with queue-based GUI integration

## Testing Strategy

### Test Files Structure
- `test_excel_to_kmz.py`: Tests KMZ export using existing Excel files
- `test_kmz_integration.py`: Tests KMZ with synthetic data
- Run tests from `src/` directory for proper module path resolution

### Manual Testing
- Large file processing: Use 1.5GB+ CSV files to test memory efficiency
- GUI responsiveness: Verify progress updates during long operations
- KMZ validation: Open generated files in Google Earth
- Executable testing: Use portable package on clean Windows systems