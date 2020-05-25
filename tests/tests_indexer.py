import unittest
import os
import filecmp
from fpindexer import index_path

class TestIndexer(unittest.TestCase):

  def test_indexer(self):
    # Run the indexer
    path = os.path.abspath('./tests/test_folder')
    index_path(path)

    # Compare to expected result
    assert(filecmp.cmp(os.path.abspath('./tests/test_folder/index.json'), os.path.abspath('./tests/result/index.json')) is True)

if __name__ == '__main__':
    unittest.main()