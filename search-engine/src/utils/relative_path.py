from os import path

def relative_path(*args):
    return path.join(path.dirname(__file__), "..", "..", *args)