# Flashpoint Indexer

## Description

Flashpoint Indexer (fpindexer) is an indexing tool / library designed to quickly create and update an index of files in a directory. Relative path, size, date modified, md5 and sha1 hashes are saved.

## Usage

An `index.json` file will be made in the directory you run the indexer on.

### As a script
> `python3 -m fpindexer [path]`

OR

> `flashpoint-indexer [path]`

If path is not provided then it will index the working directory

### As a library
```python 
from fpindexer import index_path

path = '/path/to/folder'
index_path(path)
```

## Output
```json
{
  "relative/path/to/file": {
    "dateModified": 12345678900,
    "size": 1234,
    "md5": "7ddf32e17a6ac5ce04a8ecbf782ca509",
    "sha1": "a415ab5cc17c8c093c015ccdb7e552aee7911aa4"
  }
}
```