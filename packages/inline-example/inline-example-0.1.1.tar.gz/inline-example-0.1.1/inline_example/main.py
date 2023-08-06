import inspect

def inline_example(example_path):
    with open(example_path, 'r') as i:
        r = i.read()
    
    frame = inspect.stack()[-1]
    module = inspect.getmodule(frame[0])
    with open(module.__file__, 'a+', newline='') as out:
        out.write('\n\n' + r)
