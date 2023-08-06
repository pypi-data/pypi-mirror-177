def logic_code():
    import os
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'logic.py')
    # print("Dir name: ",dirname)
    # print("File name: ",filename)
    with open(filename) as hw:
        print(hw.read())


# logic_code()