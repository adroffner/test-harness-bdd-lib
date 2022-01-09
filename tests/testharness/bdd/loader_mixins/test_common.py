from unittest import TestCase, mock

import json

from testharness.bdd.loader_mixins.common import (
    UNPARSEABLE_JSON_TOKEN,
    DataFileError,
    BaseDataLoaderMixin,
    JSONDataLoaderMixin,
    TextDataLoaderMixin
)


class BaseDataLoaderMixinTests(TestCase):

    def test_data_loader_mixin(self):
        """Prove base BaseDataLoaderMixin attributes"""

        expected_data_file = 'test_data.txt'

        loader = BaseDataLoaderMixin()
        loader.FEATURE_FILE = 'project/features/TC-T1.feature'

        self.assertEqual(loader.data_files_dir, 'project/features/data/TC-T1')
        self.assertEqual(loader.get_path(expected_data_file),
                         'project/features/data/TC-T1/{}'.format(expected_data_file))

    def test_data_loader_mixin_load_data(self):
        """Prove BaseDataLoaderMixin load_data()"""

        expected_data_file = 'raw_data'

        expected_data = b'some raw file'
        mock_load_file = mock.mock_open(read_data=expected_data)

        loader = BaseDataLoaderMixin()
        loader.FEATURE_FILE = 'project/features/Raw.feature'

        with mock.patch('testharness.bdd.loader_mixins.common.open', mock_load_file):
            data = loader.load_data(expected_data_file)

            mock_load_file.assert_called_once_with(
                'project/features/data/Raw/{}'.format(expected_data_file),
                'rb')
            self.assertEqual(data, expected_data)
            self.assertIsInstance(data, bytes)


class JSONDataLoaderMixinTests(TestCase):

    def test_data_loader_mixin_load_json(self):
        """Prove JSONDataLoaderMixin load_json()"""

        expected_data_file = 'api_data.json'

        # JSON data becomes a dict object.
        expected_data = {
            'hello': 'tester',
            'time': {
                'hour': 9,
                'minute': 33
            }
        }
        mock_load_file = mock.mock_open(read_data=json.dumps(expected_data))

        loader = JSONDataLoaderMixin()
        loader.FEATURE_FILE = 'project/features/REST-API.feature'

        with mock.patch('testharness.bdd.loader_mixins.common.open', mock_load_file):
            data = loader.load_json(expected_data_file)

            mock_load_file.assert_called_once_with(
                'project/features/data/REST-API/{}'.format(expected_data_file),
                'rb')
            self.assertEqual(data, expected_data)
            self.assertIsInstance(data, dict)

    def test_data_loader_mixin_load_json_decode_error(self):
        """Prove JSONDataLoaderMixin load_json() returns error token on decode error"""

        expected_data_file = 'api_data.json'

        # Invalid JSON data
        input_data = "{'single': 'quotes', 'invalid': true}"
        expected_data = UNPARSEABLE_JSON_TOKEN
        mock_load_file = mock.mock_open(read_data=input_data)

        loader = JSONDataLoaderMixin()
        loader.FEATURE_FILE = 'project/features/REST-API.feature'

        with mock.patch('testharness.bdd.loader_mixins.common.open', mock_load_file):
            data = loader.load_json(expected_data_file)

            mock_load_file.assert_called_once_with(
                'project/features/data/REST-API/{}'.format(expected_data_file),
                'rb')
            self.assertEqual(data, expected_data)
            self.assertIsInstance(data, str)

    def test_data_loader_mixin_load_json_os_error(self):
        """Prove JSONDataLoaderMixin load_json() raises DataFileError on file I/O error """

        expected_data_file = 'api_data.json'

        # Missing data file!
        mock_load_file = mock.MagicMock(side_effect=FileNotFoundError('missing data file'))

        loader = JSONDataLoaderMixin()
        loader.FEATURE_FILE = 'project/features/REST-API.feature'

        with self.assertRaises(DataFileError):
            with mock.patch('testharness.bdd.loader_mixins.common.open', mock_load_file):
                loader.load_json(expected_data_file)

                mock_load_file.assert_called_once_with(
                    'project/features/data/REST-API/{}'.format(expected_data_file),
                    'rb')


class TextDataLoaderMixinTests(TestCase):

    def test_data_loader_mixin_load_text(self):
        """Prove TextDataLoaderMixin load_text()"""

        expected_data_file = 'text_data.txt'

        expected_data = 'Some text file.'
        mock_load_file = mock.mock_open(read_data=expected_data)

        loader = TextDataLoaderMixin()
        loader.FEATURE_FILE = 'project/features/Texted.feature'

        with mock.patch('testharness.bdd.loader_mixins.common.open', mock_load_file):
            data = loader.load_text(expected_data_file)

            mock_load_file.assert_called_once_with(
                'project/features/data/Texted/{}'.format(expected_data_file),
                'r')
            self.assertEqual(data, expected_data)
            self.assertIsInstance(data, str)
