import os

def logic():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'logic.py')
    with open(filename) as hw:
        print(hw.read())

def searches():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'searches.py')
    with open(filename) as hw:
        print(hw.read())

def constraint():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'constraint.py')
    with open(filename) as hw:
        print(hw.read())

def optimization():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'optimization.py')
    with open(filename) as hw:
        print(hw.read())

def tictactoe():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'tictactoe.py')
    with open(filename) as hw:
        print(hw.read())