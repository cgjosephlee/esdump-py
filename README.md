# esdump
Dump Elasticsearch documents to jsonl file.

# Install
```shell
pip install 
```

# Usage
## Help
```
esdump --help

NAME
    esdump - Dump Elasticsearch documents.

SYNOPSIS
    esdump <flags>

DESCRIPTION
    Dump Elasticsearch documents to jsonl (newline-delimited) file.

FLAGS
    -i, --index=INDEX
        Type: str
        Default: ''
        Elasticsearch index.
    -h, --host=HOST
        Type: str
        Default: 'http://localhost:9200'
        Host url.
    -a, --auth=AUTH
        Type: Optional[typing.Optional[str]]
        Default: None
        A json file contains "host", "port", "user" and "secret".
    -q, --query=QUERY
        Type: str
        Default: '{"query":{"match_all":...
        Json string or json file of query.
    -f, --file=FILE
        Type: Optional[typing.Optional[str]]
        Default: None
        Output filename or leave blank to stdout.
```
## CLI
```shell
esdump --index "log-*" --host "https://user:secret@search.com:9200" --file output.jsonl
esdump --index "log-*" --auth auth.json --file output.jsonl
esdump --index "log-*" --auth auth.json | gzip > output.jsonl.gz
esdump --index "log-*" --auth auth.json --query query.json --file output.jsonl
esdump --index "log-*" --auth auth.json --query '{"query":{"term":{"name":"Jack"}}}' --file output.jsonl
```
Put classified information in shell history is not recommanded.
## Python
```python
import esdump

esdump.cli(
    index="log-*",
    host="https://user:secret@search.com:9200",
    query={"query":{"term":{"name":"Jack"}},"_source":["id"]},
    file="output.jsonl",
)
```
