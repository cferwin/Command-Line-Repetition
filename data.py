import pickle

def load_data_file(path):
    """ Load a data file containing collection and slide data. """
    f = open(path, 'rb')

    return pickle.load(f)

def save_data_file(path, collections):
    """ Save a data file containing collection and slide data.

        Variables:
        path            string      Location of the data file.
        collections     list        Collection objects to be saved.

        Ex:
        save_data_file(".sr_data", [collection1, collection2])
    """
    f = open(path, 'wb')

    pickle.dump(collections, f)
