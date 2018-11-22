""" BDD Feature Files: Data File Loaders
"""

import json
import os.path


class BDDFeatureDataLoaderMixin:
    """ BDD Feature Data Loader Mixin.

    Find and load a "Scenario Outline" parameter from a data file.
    The data filename is the "Examples:" data table value.
    """

    @property
    def data_files_dir(self):
        """ Data Files Directory.

        Parse the FEATURE_FILE attribute to find this directory.
        The directory must already exist and be popluated.

            FEATURE_FILE:   'project/features/TC-T2.feature'
            data_files_dir: 'project/features/data/TC-T2/'
        """

        if not hasattr(self, '_data_files_dir'):
            (root_dir, feature_file) = os.path.split(self.FEATURE_FILE)
            feature_code = feature_file.split('.')[0]
            self._data_files_dir = os.path.join(root_dir, 'data', feature_code)

        return self._data_files_dir

    def load_data(self, data_filename):
        """ Load Data.

        Load data from the file in the data_files_dir.

        Subclasses may override this method to change
        the return value. By default it is a str object.

        :param str data_filename: short filename without directory
        :returns: file data as some python object
        """

        file_path = os.path.join(self.data_files_dir, data_filename)

        data = ''
        with open(file_path, 'rb') as f:
            data = f.read()
        return data


class JSONDataLoaderMixin:
    """ JSON Data Loader Mixin.

    Find and load a "Scenario Outline" parameter from a data file.
    The data filename is the "Examples:" data table value.
    """

    def load_data(self, data_filename):
        file_path = os.path.join(self.data_files_dir, data_filename)

        data = {}
        with open(file_path, 'rb') as f:
            data = json.load(f)
        return data


if __name__ == '__main__':

    class ExampleLoader(BDDFeatureDataLoaderMixin):
        FEATURE_FILE = 'project/features/TC-T2.feature'

    loader = ExampleLoader()
    print(loader.data_files_dir)

    loader.load_data('hello.txt')
