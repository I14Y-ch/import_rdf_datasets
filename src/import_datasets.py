import requests
from config import *
from dcat_properties_utils import *
from rdflib import Graph, URIRef
from rdflib.namespace import DCTERMS, FOAF, RDFS, DCAT, RDF, RDFS
from rdflib import Namespace
ADMS = Namespace("http://www.w3.org/ns/adms#")
SPDX = Namespace("http://spdx.org/rdf/terms#")
dcat3 = Namespace("http://www.w3.org/ns/dcat#")

def parse_rdf_file(file_path):
    """Parses an RDF file and extracts datasets."""
    graph = Graph()
    graph.parse(file_path, format="xml")  
    
    datasets = []
    for dataset_uri in graph.subjects(RDF.type, DCAT.Dataset):
        print(f"Processing dataset URI: {dataset_uri}")  
        dataset = extract_dataset(graph, dataset_uri)

        if dataset and isinstance(dataset, dict):
            datasets.append(dataset)
        else:
            print(f"Skipping invalid dataset: {dataset}") 
    print(f"Total datasets found: {len(datasets)}") 
    return datasets

def extract_dataset(graph, dataset_uri):
    """Extracts dataset details from RDF graph."""
    dataset = { 
        "identifier": get_literal(graph, dataset_uri, DCTERMS.identifier),
        "title": get_multilingual_literal(graph, dataset_uri, DCTERMS.title),
        "description": get_multilingual_literal(graph, dataset_uri, DCTERMS.description),
        "accessRights": {"code": "PUBLIC"},  
        "issued": get_literal(graph, dataset_uri, DCTERMS.issued, is_date=True),
        "modified": get_literal(graph, dataset_uri, DCTERMS.modified, is_date=True),
        "publisher": DEFAULT_PUBLISHER, 
        "landingPages": get_resource_list(graph, dataset_uri, DCAT.landingPage),
        "keywords": get_multilingual_keywords(graph, dataset_uri, DCAT.keyword),
        "distributions": extract_distributions(graph, dataset_uri),
        "identifiers": [get_literal(graph, dataset_uri, DCTERMS.identifier)],
        "languages": get_languages(graph, dataset_uri, DCTERMS.language),
        "contactPoints": extract_contact_points(graph, dataset_uri),
        "documentation": get_resource_list(graph, dataset_uri, FOAF.page),
        "images": get_resource_list(graph, dataset_uri, SCHEMA.image),
        "temporalCoverage": get_temporal_coverage(graph, dataset_uri), 
        "frequency": get_frequency(graph, dataset_uri),
        "isReferencedBy": get_is_referenced_by(graph, dataset_uri),
        "relations": get_relations(graph, dataset_uri),
        "spatial": get_spatial(graph, dataset_uri),
        "version": get_literal(graph, dataset_uri, dcat3.version),
        "versionNotes": get_multilingual_literal(graph, dataset_uri, ADMS.versionNotes),
        "conformsTo": get_conforms_to(graph, dataset_uri),
        "themes": get_themes(graph, dataset_uri, DCAT.theme), 
    }
    return dataset

def extract_distributions(graph, dataset_uri):
    """Extracts distributions for a dataset."""
    distributions = []
    for distribution_uri in graph.objects(dataset_uri, DCAT.distribution):
        title = get_multilingual_literal(graph, distribution_uri, DCTERMS.title)
        description = get_multilingual_literal(graph, distribution_uri, DCTERMS.description)
        if not title: 
            title = {'de': 'Datenexport'}
        if not description:  
            description = {'de': 'Export der Daten'}

        media_type_uri = get_single_resource(graph, distribution_uri, DCAT.mediaType)
        media_type_code = MEDIA_TYPE_MAPPING.get(str(media_type_uri)) if media_type_uri else None
        format_uri = get_single_resource(graph, distribution_uri, DCTERMS.format)
        format_code = format_uri.split("/")[-1] if format_uri else None  
        download_url = get_single_resource(graph, distribution_uri, DCAT.downloadURL)
        access_url = get_single_resource(graph, distribution_uri, DCAT.accessURL)
        common_url = access_url if access_url else download_url
        download_title = get_multilingual_literal(graph, distribution_uri, RDFS.label)
        availability_uri = get_single_resource(graph, distribution_uri, URIRef("http://data.europa.eu/r5r/availability"))
        license_uri = get_single_resource(graph, distribution_uri, DCTERMS.license)
        license_code = license_uri.split("/")[-1] if license_uri else None
        checksum_algorithm = get_literal(graph, distribution_uri, SPDX.checksumAlgorithm)
        checksum_value = get_literal(graph, distribution_uri, SPDX.checksumValue)
        packaging_format = get_literal(graph, distribution_uri, DCAT.packageFormat)

        distribution = {
            "title": title, 
            "description": description,  
            "format": {"code": format_code} if format_code and format_code in VALID_FORMAT_CODES else None,  
            "downloadUrl": {
                "label": download_title,  
                "uri": common_url  
            } if common_url else None,
            "mediaType": {"code": media_type_code} if media_type_code else None,  
            "accessUrl": {
                "label": download_title,  
                "uri": common_url 
            } if common_url else None,
            "license": {"code": license_code} if license_code else None,  
            "availability": {"code": get_availability_code(availability_uri)} if get_availability_code(availability_uri) else None,  
            "issued": get_literal(graph, distribution_uri, DCTERMS.issued, is_date=True),
            "modified": get_literal(graph, distribution_uri, DCTERMS.modified, is_date=True),
            "rights": get_literal(graph, distribution_uri, DCTERMS.rights),
            "accessServices": get_access_services(graph, distribution_uri),
            "byteSize": get_literal(graph, distribution_uri, DCAT.byteSize),
            "checksum": {
                "algorithm": {"code": checksum_algorithm} if checksum_algorithm else None,
                "checksumValue": checksum_value
            } if checksum_algorithm or checksum_value else None,
            "conformsTo": get_conforms_to(graph, distribution_uri),
            "coverage": get_coverage(graph, distribution_uri),
            "documentation": get_resource_list(graph, distribution_uri, FOAF.page),
            "identifier": get_literal(graph, distribution_uri, DCTERMS.identifier),
            "images": get_resource_list(graph, distribution_uri, SCHEMA.image),
            "languages": get_resource_codes(graph, distribution_uri, DCTERMS.language),
            "packagingFormat": {"code": packaging_format} if packaging_format else None,
            "spatialResolution": get_literal(graph, distribution_uri, DCAT.spatialResolutionInMeters), 
            "temporalResolution": get_literal(graph, distribution_uri, DCAT.temporalResolution) 
        }
        distributions.append(distribution)
    return distributions

def create_dataset_payload(dataset):
    """Creates the JSON payload for the dataset submission."""
    if not isinstance(dataset, dict):
        raise ValueError("Dataset must be a dictionary.")
    return {"data": dataset}

def submit_to_api(payload):
    """Submits the dataset payload to the API."""
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post(f"{API_BASE_URL}/datasets", json=payload, headers=headers, verify=False) 
    if response.status_code not in [200, 201, 204]:
        raise Exception(f"API error: {response.status_code} - {response.text}")
    
    return response.json()
   

def main():
    datasets = parse_rdf_file(TEMPLATE_PATH)
    print(f"Total datasets extracted: {len(datasets)}")
    success_count, error_count = 0, 0
    
    print("\nStarting dataset import...\n")
    
    for dataset in datasets:
        print(f"Submitting dataset: {dataset['identifier']}")
        print(f"Processing dataset: {dataset['identifier']}")
        try:
            payload = create_dataset_payload(dataset)
            print(payload)
            response = submit_to_api(payload)
            print(f"Success - Dataset ID: {response}\n")
            success_count += 1

        except Exception as e:
            error_count += 1
            print(f"Error: {str(e)}\n")

    print("=== Import Summary ===")
    print(f"Total processed: {success_count + error_count}")
    print(f"Successful: {success_count}")
    print(f"Failed: {error_count}")


if __name__ == "__main__":
    main()
