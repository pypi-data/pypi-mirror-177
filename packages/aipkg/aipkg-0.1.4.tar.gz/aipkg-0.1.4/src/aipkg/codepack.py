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

def lppexamples():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'lppexamples.py')
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

def theory():
    print("Removed to save size, use getdocpath() or theorytext() instead")
#     dirname = os.path.dirname(__file__)
#     imgsdir = os.path.join(dirname, 'AI_Notes_imgs')
#     # print(imgsdir)
#     img_names = []
#     for img in os.listdir(imgsdir):
#         img_names.append(img)
#     # print(img_names)

#     from IPython.display import Image, display

#     for imageName in img_names:
#         display(Image(filename=(os.path.join(imgsdir, imageName))))

def getdocpath():
    dirname = os.path.dirname(__file__)
    docpath = os.path.join(dirname, 'AI_Notes.docx')
    print(docpath)