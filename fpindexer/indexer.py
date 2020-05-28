import hashlib
import json
import os
import time
import yaml
from py7zr import SevenZipFile
from pathlib import Path
from .util import convert_size

BUF_SIZE = 65536

class IndexedFile():
  path: str
  gameId: str
  lastModified: int
  size: int
  sha256: str

"""Load an existing index file, if missing return an empty index"""
def load_index(path: Path) -> dict:
  index = {}
  if path.is_file():
    with open(path, 'r') as f:
      rawIndex = json.load(f)
      for path in rawIndex:
        index[path] = IndexedFile()
        for key in rawIndex[path]:
          setattr(index[path], key, rawIndex[path][key])
      return index
  return {}

"""Gets the ID and Content Hash from inside metadata"""
def get_meta_info(filePath, rootPath) -> (str, str):
  with SevenZipFile(filePath, 'r') as archive:
    if 'meta.yaml' in archive.getnames():
      archive.extract(targets=['meta.yaml'], path=rootPath)
    else:
      return '', ''
  metaPath = os.path.join(rootPath, 'meta.yaml')
  with open(metaPath) as f:
    data = yaml.safe_load(f)
    return data['ID'], data['Content Hash']
  os.remove(metaPath)
  pass

"""Returns an unhashed IndexedFile from a path"""
def build_unhashed_index(filePath) -> IndexedFile:
  index = IndexedFile()
  index.path = filePath
  fileStat = os.stat(filePath)
  index.lastModified = fileStat.st_mtime
  index.size = fileStat.st_size

  return index

"""Update the index in the given path"""
def index_path(pathStr):
  # Time indexing
  startTime = time.time()
  path = Path(pathStr)
  index = None
  checkedFiles = []
  countUpdated = 0
  countRemoved = 0
  countTotal = 0

  try:
    if path.is_dir():
      indexPath = path.joinpath('index.json')
      index = load_index(indexPath)
    else:
      print('Not a directory - {}'.format(path))
      return
  except:
    print('Error loading Index file')
    return

  # Update New/Changed files in index
  for root, subdirs, files in os.walk(path):
    for f in files:
      # Don't index the index itself
      if f == 'index.json' or not f.endswith('.7z'):
        continue
      filePath = os.path.join(root, f)
      relPath = os.path.relpath(filePath, path)
      newFileInfo = build_unhashed_index(filePath)
      newFileInfo.path = relPath
      oldFileInfo = index.get(relPath, None)
      
      countTotal += 1
      if (oldFileInfo is None) or \
         (oldFileInfo.lastModified != newFileInfo.lastModified ) or \
         (oldFileInfo.size         != newFileInfo.size         ):
        # File new or changed, hash and update index
        countUpdated += 1
        gameId, sha256 = get_meta_info(filePath, root)
        newFileInfo.gameId = gameId
        newFileInfo.sha256 = sha256
        index[relPath] = newFileInfo
        print('File Updated - {0}\n\tID - {1}\n\tSHA256 - {2}\n\tSize - {3}'.format(
          newFileInfo.path,
          newFileInfo.gameId,
          newFileInfo.sha256,
          convert_size(newFileInfo.size)
        ))

      # Keep list so we can find missing files later
      checkedFiles.append(relPath)

  for key in list(index.keys()):
    if key not in checkedFiles:
      countRemoved += 1
      print('File Removed - {0}'.format(key))
      index.pop(key, None)

  # Save index
  dictIndex = {}
  for key in index:
    d = index[key].__dict__
    d.pop('path', None)
    dictIndex[key] = d
  with open(indexPath, 'w') as f:
    f.write(json.dumps(dictIndex, indent=2))

  print('Indexed {0} Files ({1} updated, {2} removed) in {3} seconds'.format(
    countTotal,
    countUpdated,
    countRemoved,
    int(time.time() - startTime)))