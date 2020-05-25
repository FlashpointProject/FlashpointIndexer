import hashlib
import json
import os
import time
from pathlib import Path
from .util import convert_size

BUF_SIZE = 65536

class IndexedFile():
  path: str
  lastModified: int
  size: int
  sha1: str
  md5: str

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

"""Returns a tuple of md5 and sha1 hashes"""
def hash_file(path) -> (str, str):
  md5 = hashlib.md5()
  sha1 = hashlib.sha1()

  with open(path, 'rb') as f:
    data = f.read(BUF_SIZE)
    if data:
      md5.update(data)
      sha1.update(data)
    else:
      return None, None

  return md5.hexdigest(), sha1.hexdigest()
      

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
      if f == 'index.json':
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
        md5, sha1 = hash_file(filePath)
        newFileInfo.md5 = md5
        newFileInfo.sha1 = sha1
        index[relPath] = newFileInfo
        print('File Updated - {0}\n\tMD5 - {1}\n\tSHA1 - {2}\n\tSize - {3}'.format(
          newFileInfo.path,
          newFileInfo.md5,
          newFileInfo.sha1,
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