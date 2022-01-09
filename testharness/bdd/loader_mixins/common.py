""" BDD Feature Files: Data File Loaders
"""

import json
# from pathlib import Path

UNPARSEABLE_JSON_TOKEN = '<Unparseable JSON Document>'


class DataFileError(ValueError):
    """ BDD Data File Error.

    The data file cannot be read or is corrupt.
    """
    pass


class BaseDataLoaderMixin:
    """ Base Data Loader Mixin.

    Find and load a "Scenario Outline" parameter from a data file.
    The data filename is the "Examples:" data table cell.
    """

    FEATURE_FILE = None  # Should be a Path() object

    @property
    def data_files_dir(self):
        """ Data Files Directory.

        Parse the FEATURE_FILE attribute to find this directory.
        The directory must already exist and be populated.

            FEATURE_FILE:   Path('project/features/TC-T2.feature')
            data_files_dir: Path('project/features/data/TC-T2')
        """

        if not hasattr(self, '_data_files_dir'):
            (root_dir, feature_file) = (self.FEATURE_FILE.parent, self.FEATURE_FILE.name)
            feature_code = feature_file.split('.')[0]
            self._data_files_dir = root_dir / 'data' / feature_code

        return self._data_files_dir

    def get_path(self, data_filename):
        """ Get Data File Path.

        Get the data file path in the data_files_dir.

        :param data_filename: short filename without directory
        :returns: path to file
        """

        file_path = self.data_files_dir / data_filename
        return file_path

    def load_data(self, data_filename):
        """ Load Raw Data.

        Load data from the file in the data_files_dir.

        Subclasses should make similar methods to return other
        python object types.

        :param data_filename: short filename without directory
        :returns: file data as bytes
        """

        file_path = self.get_path(data_filename)

        try:
            with open(file_path, 'rb') as f:
                data = f.read()
        except IOError:
            data = b''
        return data

# ================================================================


class TextDataLoaderMixin(BaseDataLoaderMixin):
    """ Text Data Loader Mixin.

    Find and load a "Scenario Outline" parameter from a data file.
    The data filename is the "Examples:" data table cell.
    """

    def load_text(self, data_filename):
        """ Load Data as Text.

        Load text data from the file in the data_files_dir.

        :param data_filename: short filename without directory
        :returns: file data as str
        """

        file_path = self.get_path(data_filename)

        try:
            with open(file_path, 'r') as f:
                data = f.read()
        except IOError:
            data = b''
        return data


class JSONDataLoaderMixin(BaseDataLoaderMixin):
    """ JSON Data Loader Mixin.

    Find and load a "Scenario Outline" parameter from a data file.
    The data filename is the "Examples:" data table cell.
    """

    def load_json(self, data_filename):
        """ Load Data as JSON.

        Load JSON data from the file in the data_files_dir.

        :param data_filename: short filename without directory
        :returns: file data as JSON dict
        """

        file_path = self.get_path(data_filename)

        try:
            with open(file_path, 'rb') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = UNPARSEABLE_JSON_TOKEN
        except OSError as e:
            raise DataFileError(file_path) from e

        return data


if __name__ == '__main__':  # pragma: no cover

    class ExampleLoader(JSONDataLoaderMixin):
        FEATURE_FILE = 'project/features/TC-T2.feature'

    loader = ExampleLoader()
    print(loader.data_files_dir)

    loader.load_json('hello.txt')
