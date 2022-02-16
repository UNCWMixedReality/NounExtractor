import re
from src.DocumentExtraction import classify_single_file, classify_zip
import pprint
import json

results = classify_zip('tests/test_data/test.zip', output_dir=None, raw_json=True)
print(results)