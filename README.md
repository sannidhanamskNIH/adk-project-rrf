# UMLS RRF File Reader Agent

## Overview

This is an ADK (Agent Development Kit) agent designed to read and analyze UMLS (Unified Medical Language System) RRF (Rich Release Format) files. The agent processes the MRDEF.RRF file and provides comprehensive analysis and statistics about the medical terminology data contained within.

## Files

### Main Agent
- **`host_agent.py`** - FastAPI-based web host with REST API and interactive UI
- **`umls_agent.py`** - Full-featured agent with comprehensive analysis
- **`test_agent.py`** - Lightweight test agent for quick verification
- **`MRDEF.RRF`** - The source UMLS data file (Medical Record Definitions, ~487K records)

## Features

The agent provides:

✅ **File Statistics**
- Total record count
- Number of unique medical concepts (CUIs - Concept Unique Identifiers)
- Language and semantic type detection
- Average records per concept

✅ **Web API & Dashboard**
- FastAPI host providing REST endpoints
- Two-pane interactive explorer at `/ui` for searching and visualizing data

✅ **Language/Semantic Type Detection**
- Identifies all 66+ languages and semantic types in the file
- Examples: MSH (Medical Subject Headings), MSHSWE (Swedish), CSP, LNC, etc.

✅ **Sample Data Display**
- Shows the first 5 concepts with their multilingual definitions
- Displays actual medical terminology translations

✅ **Progress Reporting**
- Reports processing progress every 100,000 records
- Handles large files efficiently

## Usage

### Running the Web Interface
```bash
uv run python host_agent.py
```

### CLI Analysis
```bash
python umls_agent.py
```

### Quick Test
```bash
python test_agent.py
```

## Output Example

The agent generates a formatted report showing:

```
📊 STATISTICS:
  • Total Records: 487,338
  • Unique Concepts (CUIs): 298,649
  • Languages/Semantic Types: 66
  • Average Records per Concept: 1.63

🌍 Languages/Semantic Types Detected:
  • MSH (Medical Subject Headings - English)
  • MSHSWE (Swedish)
  • MSHCZE (Czech)
  • CSP (Cumulative Supplement)
  • ... and 62 more

📋 SAMPLE RECORDS:
  CUI: C0000039 (Synthetic phospholipid)
    [1] MSH: "Synthetic phospholipid used in liposomes..."
    [2] MSHSWE: "Syntetisk fosfolipid som anvnds..."
    [3] MSHCZE: "Syntetick fosfolipid..."
```

## File Format (RRF)

The MRDEF.RRF file uses pipe-delimited format:
```
CUI|AUI|ATTRIBUTE_ID|SOURCE|LANGUAGE|DEFINITION|STATUS|SOURCE_ID
```

Example:
```
C0000039|A0016515|AT38152019||MSH|Synthetic phospholipid...|N||
```

## Agent Capabilities

The `UMLSAgent` class provides:

- **`read_file()`** - Reads and parses the RRF file efficiently
- **`_parse_line()`** - Parses individual RRF records
- **`get_statistics()`** - Returns comprehensive statistics
- **`get_sample_records()`** - Retrieves sample records
- **`print_report()`** - Generates formatted output report

## Data Insights

From analyzing MRDEF.RRF:
- **487,338 total definition records**
- **298,649 unique medical concepts**
- **66 different languages and semantic sources**
- **Multilingual support** with translations in English, Swedish, Czech, Portuguese, Spanish, and more

## Requirements

- Python 3.6+
- No external dependencies required

## Future Enhancements

Possible additions:
- Export to CSV/JSON formats
- Concept search functionality
- Language-specific filtering
- Definition comparison across languages
- Concept relationship analysis
- Database integration
