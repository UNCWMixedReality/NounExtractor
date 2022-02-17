import re
from src.DocumentExtraction import classify_single_file, classify_zip
import pprint
import json

results = classify_single_file('/Users/sethangell/Desktop/RobinhoodPaper.docx', output_dir=None, raw_json=True)
print(results)