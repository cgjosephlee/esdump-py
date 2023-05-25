from __future__ import annotations

import sys

import fire
import orjson
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from tqdm import tqdm


def esdump(search: Search, file: str | None):
    if file:
        handle = open(file, "wb")
    else:
        handle = sys.stdout.buffer
    for doc in tqdm(search.scan(), total=search.count()):
        handle.write(orjson.dumps(doc.to_dict()))
        handle.write(b"\n")
    if file:
        handle.close()


def cli(
    index: str = "my-index",
    host: str = "http://localhost:9200",
    auth: str | dict | None = None,
    query: str | dict = {"query": {"match_all": {}}},
    file: str | None = None,
):
    # style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
    """Dump Elasticsearch documents.

    Dump Elasticsearch documents to jsonl (newline-delimited) file.

    Args:
        index:
            Elasticsearch index.
        host:
            Host url.
        auth:
            A json file contains "host", "port", "user" and "secret".
        query:
            Json string or json file of query.
        file:
            Output filename or leave blank to stdout.
    """
    es_args = {"hosts": host}
    if auth:
        if isinstance(auth, str) and auth.endswith("json"):
            with open(auth) as f:
                auth_dict = orjson.loads(f.read())
        elif isinstance(auth, dict):
            auth_dict = auth
        es_args["http_auth"] = (auth_dict.get("user"), auth_dict.get("secret"))
        p = auth_dict.get("port")
        if p:
            es_args["port"] = p
        h = auth_dict.get("host")
        if h:
            es_args["hosts"] = h
    es = Elasticsearch(**es_args)

    if isinstance(query, str) and query.endswith("json"):
        with open(query) as f:
            q = orjson.loads(f.read())
    elif isinstance(query, str):
        q = orjson.loads(query)
    else:
        q = query
    s = Search.from_dict(q)
    s = s.using(es)
    s = s.index(index)
    tot = s.count()
    if tot == 0:
        print("No document found.", file=sys.stderr)
        sys.exit(1)
    esdump(s, file)


def main():
    fire.Fire(cli)


if __name__ == "__main__":
    main()
