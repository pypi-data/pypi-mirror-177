# ID converter between PMID, PMCID and DOI
> https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/

## Installation
```bash
python3 -m pip install pmc-id-converter
```

## Usage
### Command Line
```bash
pmc_idconv --help

# PMID
pmc_idconv 30003000
# PMCID
pmc_idconv PMC6039336
# DOI
pmc_idconv 10.1007/s13205-018-1330-z
# Multiple IDs
pmc_idconv 30003000 30003001 30003002
# Output to a file
pmc_idconv 30003000 30003001 30003002 -o out.json
```

### Python
```python
from pmc_id_converter import API

API.idconv('PMC3531190')
API.idconv('PMC3531190', 'PMC3531191123', 'PMC3531191')
API.idconv('23193287')
API.idconv('10.1093/nar/gks1195')
```
