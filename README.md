# Flashpoint Indexer

## Description

Flashpoint Indexer (fpindexer) is an indexing tool / library designed to quickly create and update an index of Flashpoint Launcher curations in a directory. Relative path, size, date modified, game ID and sha256 content hashes are saved.

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
  "someDumbName.7z": {
    "lastModified": 1590658883.555613,
    "size": 1758212,
    "gameId": "5cd8c62b-f488-4586-98fc-3da7c3c3206e",
    "sha256": "9ea3cbaf8f7d485f3b44d483f743559c4a2241c45a131ef94368445e3f013cc8"
  }
}
```