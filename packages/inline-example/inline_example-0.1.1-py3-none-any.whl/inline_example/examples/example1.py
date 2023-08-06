from inline_example import inline_example
from pathlib import Path

class MyAwesomeClass:
    def __init__(self):
        self.attribute = str()
    
    def does_something(self):
        print('yay!')
    

def example_usage():
    # assumes that your package has examples folder
    inline_example(
        example_path=Path(__file__).parent / 'examples/example.py')

# now your user could call this:

# from yourpackage.your_module import example_usage
# example_usage()