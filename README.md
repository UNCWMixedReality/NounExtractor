# Noun Extractor
### A cloud service based natural language processing pipeline
Created by the UNCW Mixed Reality Lab

## Quick Start
```bash
pip install git+https://github.com/UNCWMixedReality/NounExtractor.git
```

```python
from DocumentExtraction import classify_single_file 
```

## Setup
This package utilizes Azure's language services for it's natural language processing, and optionally a postgres database for centralized caching of results across multiple instances of the service. 

### Azure Language Services
First, set up an endpoint on Azure for the [Azure Language Service](https://azure.microsoft.com/en-us/services/cognitive-services/language-service/#demo) and generate an API key. Once that is done, set the following environment variables

__Environment Variables:__
* AZURE_KEY -> set to your Azure API key
* AZURE_ENDPOINT -> set to the url of your Azure language services endpoint

### Result Caching
To help cut down of API requests and by extension costs, this service automatically caches a hash of any requested content and the response it receives from Azure. If it encounters this exact hash again, it returns the cached output instead of making another request. By default, this cache is stored in an internal sqlite database. If you'd like to centralize this cache across numerous different services, you can pass a yaml file containing db credentials to your classify calls in order to cache against your database instead of the internal sqlite version. The file should be formatted as seen below

```yaml
db: 
  vendor: postgres 
  user: postgres
  password: super-sick-password 
  table: example
  host: localhost
  port: 5432
```

To utilize this, you'd call one of the classifier functions as seen below:

```python
from DocumentExtraction import classify_zip

results = classify_zip('app/ingest/new_content.zip', depth=5, output_dir=None, raw_json=True, db_config='app/config/db.yaml')
```

## Usage
The simplest way to use this package is through 3 exposed functions:
`classify_single_file()`, `classify_directory()`, and `classify_zip()`

These 3 functions accept file paths, and classify a single file, directory, and zip directory respectively (we're not very nuanced here, it does what it says on the tin). Output is formatted as a JSON object taking the form of our internal ClassifiedText object, [reference found here](https://github.com/UNCWMixedReality/NounExtractor/blob/main/src/DocumentExtraction/ClassifiedText.py). It can be piped either to a designated output directory, or returned as a raw json string.

### Example Usage
__Extract nouns from a single file and store in a local directory:__
```python
from DocumentExtraction import classify_single_file

classify_single_file('/app/ingest/TheGreatGatsby_Chp1.txt', output_dir="/app/export/")
```

__Extract nouns from a entire zip directory and return raw json string__
```python
from DocumentExtraction import classify_zip

classify_zip('/app/ingest/TheGreatGatsby.zip', output_dir=None, raw_json=True)
```

__Extract nouns from top two levels of directory and cache against specified database__
```python
from DocumentExtraction import classify_directory

classify_directory('/app/ingest/', depth=2, raw_json=True, db_config="prod.db.yaml")
```


