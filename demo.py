import re
from DocumentExtraction import classify_single_file, classify_zip
import pprint
import json

results = classify_single_file('tests/test_data/gatsby.txt', output_dir=None, raw_json=True)
print(results)