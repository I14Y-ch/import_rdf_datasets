# DCAT Dataset in xml/rdf or ttl format Import Tool

A Python-based tool for importing DCAT datasets in xml/rdf or ttl format into the I14Y platform of the Swiss Federal Statistical Office (BFS).

## Features
- Import DCAT datasets from xml/rdf or ttl files to I14Y API
- Supported properties for dcat.Dataset:
  
| Property | Requirement level | 
| ----| ---- | 
| __dct:title__ | mandatory |
| __dct:description__ | mandatory | 
| __dct:accessRight__ (chosen from:  [PUBLIC, NON_PUBLIC, CONFIDENTIAL, RESTRICTED](http://publications.europa.eu/resource/authority/access-right)) | mandatory | 
| __dct:publisher__ (stated in config.py) | mandatory |
| __dct:identifier__ | mandatory |
| __dct:issued__ | optional |
| __dct:modified__ | optional |
| __dcat:landingPage__ | optional |
| __dcat:keyword__ | optional |
| __dct:language__ | optional |
| __dcat:contactPoint__ | optional |
| __documentation (foaf:page)__ | optional |
| __schema:image__ | optional |
| __dct:temporalCoverage__ | optional |
| __dcat:temporalResolution__ | optional |
| __frequency (dct:accrualPeriodicity)__ | optional |
| __dct:isReferencedBy__ | optional |
| __dct:relation__ | optional |
| __spatial/geographical coverage (dct:spatial)__ | optional |
| __dct:conformsTo__ | optional |
| __dcat:theme__ | optional |
| __dcat:version__ | optional |
| __adms:versionNotes__ | optional |


prov.qualifiedAttribution and prov.qualifiedRelation are not supported automatically, you can add those informations manually on I14Y. 

- Supported properties for dcat.Distribution:
  
| Property | Requirement level | 
| ----| ---- | 
| __dct:title__ (if not stated, set automatically to 'Datenexport') | mandatory |
| __dct:description__ (if not stated, set automatically to 'Export der Daten') | mandatory |
| __dcat:accessURL__ | mandatory |
| __dcat:downloadURL__ | optional |
| __dct:license__ |optional |
| __dct:issued__ | optional |
| __dct:modified__ | optional |
| __dct:rights__ | optional |
| __dct:language__ | optional |
| __schema:image__ | optional |
| __dcat:spatialResolutionInMeters__ | optional |
| __dcat:temporalResolution__ | optional | |
| __dct:conformsTo__ | optional |
| __dcat:mediaType__ | optional |
| __dct:format__ | optional |
| __dct:packageFormat__ | optional |
| __spdx:checksum__ | optional |
| __dcat:byteSize__ | optional |

## Prerequisites

- Python 3.8+
- pip package manager

## Installation

1. Clone this repository:
```bash
git clone [repository-url]
cd import_rdf_datasets
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
   - Edit `src/config.py` with your I14Y API token, organization ID and right file format ("xml" or "ttl")

## Usage

### Import Datasets

1. Log in on the interoperability platform. Copy the token clicking on the profile symbol. Fill in the token in the file config.py. Also provide the identifier of your organsation.
2. Place your RDF files in the data/ folder (.xml, .rdf or .ttl)
3. Run the import script:

```bash
python src/import_datasets.py
```

The script will process each row and display real-time progress and error messages in the terminal.

## File Structure

```
import_rdf_datasets/
├── data/
│   └── datasets.xml
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
