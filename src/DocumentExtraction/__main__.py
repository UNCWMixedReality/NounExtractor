import argparse
import json
import sys
from pathlib import Path
from typing import Dict
from uuid import uuid4 as rand_id
import os

from .ClassifiedText import ClassifiedTextEncoder
from .TextClassification import TextClassifier
from .TextExtraction import TextExtractor


# CLI + Helpers
def setup_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract text from text documents and classify it with Azure Web Services"
    )
    parser.add_argument(
        "-z",
        "--zip",
        type=str,
        help="Run the text classification process on a zip directory.  Note the --depth flag",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        help="Run the text classification on a directory. Note the --depth flag",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Run the text classification process on a single file",
    )
    parser.add_argument(
        "--depth",
        type=int,
        help="Specify the depth to traverse a directory for files. 0 indexed",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        help="The directory where results should be written",
    )
    parser.add_argument(
        "-r",
        "--raw-json",
        action="store_true",
        help="Determines whether output will be written to a file or returned to stdout",
    )

    return parser


def write_results_to_output_dir(result_dict: Dict, output_dir: str):
    file_name = Path(output_dir)
    file_name = file_name / f"results-{rand_id}.json"

    with open(file_name, "w") as outfile:
        json.dump(result_dict, outfile, cls=ClassifiedTextEncoder)


# Classification Orchestration
def classify_zip(
    zip_path: str, depth: int = None, output_dir: str = ".", raw_json=False
):
    TE = TextExtractor()
    TC = TextClassifier(azure=True)

    results = TE.extract_text_from_a_zip_directory(zip_path, depth)

    output = {}
    print(os.environ.get('AZURE_KEY'))

    for val in results.keys():
        print(val)
        output[val] = TC.classify_single_text_element(results[val])

    if raw_json:
        return json.dumps(output, cls=ClassifiedTextEncoder)

    write_results_to_output_dir(output, output_dir)


def classify_single_file(path: str, output_dir: str, raw_json=False):
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
    TE = TextExtractor()
    TC = TextClassifier(azure=True)

    results = TE.extract_text_from_all_files_in_directory(path, depth)

    output = {}

    for val in results.keys():
        output[val] = TC.classify_single_text_element(results[val])

    if raw_json:
        return json.dumps(output, cls=ClassifiedTextEncoder)

    write_results_to_output_dir(output, output_dir)


# ============================================================================ #
# MAIN

if __name__ == "__main__":
    if os.environ.get("DEBUG", False):
        import sys
        print("Ooooh someones having a bad day. Here's some info")
        print("=================================================")
        print(f'{sys.path = }')
        print(f'{os.getcwd() = }')
        print("=================================================\n\n")

    parser = setup_cli()

    args = parser.parse_args()

    if args.file:
        if args.raw_json:
            print(classify_single_file(args.file, args.output_dir, raw_json=True))
        else:
            classify_single_file(args.file, args.output_dir)
    elif args.directory:
        if args.raw_json:
            print(classify_directory(args.directory, args.depth, args.output_dir, raw_json=True))
        else:
            classify_directory(args.directory, args.depth, args.output_dir)
    elif args.zip:
        if args.raw_json:
            print(classify_zip(args.file, args.depth, args.output_dir, raw_json=True))
        else:
            classify_directory(args.directory, args.depth, args.output_dir)
    else:
        parser.print_help()    
