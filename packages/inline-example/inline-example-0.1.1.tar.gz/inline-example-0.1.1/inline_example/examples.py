from .main import inline_example
from pathlib import Path

def example_usage():
    inline_example(Path(__file__).parent / 'examples/example1.py')
