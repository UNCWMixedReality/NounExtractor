import json
from pathlib import Path
from typing import Dict
from uuid import uuid4 as rand_id

from .ClassifiedText import ClassifiedTextEncoder
from .TextClassification import TextClassifier
from .TextExtraction import TextExtractor

def write_results_to_output_dir(result_dict: Dict, output_dir: str):
    file_name = Path(output_dir)
    file_name = file_name / f"results-{rand_id}.json"

    with open(file_name, "w") as outfile:
        json.dump(result_dict, outfile, cls=ClassifiedTextEncoder)

# Classification Orchestration
def classify_zip(
    zip_path: str, depth: int = None, output_dir: str = ".", raw_json=False
):
    """
    Args: 
    * zip_path: A filepath pointing at an existing zip file full of documents
    * depth: [Optional] Specify how many levels down to search for files (1-indexed)
    * output_dir: a filepath pointing at the directory to save the results in
    * raw_json: A boolean representing whether output should be returned as a json string
    """
    TE = TextExtractor()
    TC = TextClassifier(azure=True)

    results = TE.extract_text_from_a_zip_directory(zip_path, depth)

    output = {}

    for val in results.keys():
        output[val] = TC.classify_single_text_element(results[val])

    if raw_json:
        return json.dumps(output, cls=ClassifiedTextEncoder)

    write_results_to_output_dir(output, output_dir)


def classify_single_file(path: str, output_dir: str, raw_json=False):
    """
    Args: 
    * File path: A filepath pointing at a single document
    * output_dir: a filepath pointing at the directory to save the results in
    * raw_json: A boolean representing whether output should be returned as a json string
    """
    TE = TextExtractor()
    TC = TextClassifier(azure=True)

    result = TE.extract_text_from_single_file(path)

    output = {path: TC.classify_single_text_element(result)}

    if raw_json:
        return json.dumps(output, cls=ClassifiedTextEncoder)

    write_results_to_output_dir(output, output_dir)


def classify_directory(
    path: str, depth: int = None, output_dir: str = None, raw_json=False
):
    """
    Args: 
    * path: A filepath pointing at a directory full of documents
    * depth: [Optional] Specify how many levels down to search for files (1-indexed)
    * output_dir: a filepath pointing at the directory to save the results in
    * raw_json: A boolean representing whether output should be returned as a json string
    """
    TE = TextExtractor()
    TC = TextClassifier(azure=True)

    results = TE.extract_text_from_all_files_in_directory(path, depth)

    output = {}

    for val in results.keys():
        output[val] = TC.classify_single_text_element(results[val])

    if raw_json:
        return json.dumps(output, cls=ClassifiedTextEncoder)

    write_results_to_output_dir(output, output_dir)