
def read_from_file(filename):

    with open(filename) as file:
        data = file.read()

    return data
