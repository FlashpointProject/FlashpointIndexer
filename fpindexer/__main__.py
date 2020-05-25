import os
import argparse

from .indexer import index_path

def setup():
  parser = argparse.ArgumentParser(description='Run FP Indexer.')
  parser.add_argument('path', nargs='?', default=os.getcwd(), help='path to run indexer on')
  args = parser.parse_args()

  index_path(args.path)

if __name__ == "__main__":
  setup()