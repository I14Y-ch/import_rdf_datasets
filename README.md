# I14Y Dataset Import Tool

A Python-based tool for importing DCAT datasets in rdf format into the I14Y platform of the Swiss Federal Statistical Office (BFS).

## Features
- Import DCAT datasets from rdf files to I14Y API

## Prerequisites

- Python 3.8+
- pip package manager

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd bfs/2025_02_batchimport
```

2. (Optional but recommended) Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the application:
   - Edit `src/config.py` with your I14Y API token and organization ID

## Usage

### Import Datasets

1. Log in on the interoperability platform. Copy the token clicking on the profile symbol. Fill in the token in the file config.py. Also provide the identifier of your organsation. 
2. Run the import script:

```bash
python src/import_datasets.py
```

The script will process each row and display real-time progress and error messages in the terminal.

## File Structure

```
2025_02_batchimport/
├── data/
│   └── datasets.rdf
├── src/
│   ├── config.py
│   ├── dcat_properies_utils.py
│   ├── import_datasets.py
│   └── mappings.py
├── requirements.txt
└── README.md
```

## Contributing

Please ensure any pull requests or contributions adhere to the following guidelines:
- Keep the code simple and well-documented
- Follow PEP 8 style guidelines
- Include appropriate error handling
- Test thoroughly before submitting
