from unittest import TestCase, mock

import json

from testharness.bdd.loader_mixins.common import (
    DataFileError,
    BDDFeatureDataLoaderMixin,
    JSONDataLoaderMixin
)


class DataLoaderMixinTests(TestCase):

    def test_data_loader_mixin(self):
        "Prove base BDDFeatureDataLoaderMixin attributes"

        expected_data_file = 'test_data.txt'

        loader = BDDFeatureDataLoaderMixin()
        loader.FEATURE_FILE = 'project/features/TC-T1.feature'

        self.assertEqual(loader.data_files_dir, 'project/features/data/TC-T1')
        self.assertEqual(loader.get_local_path(expected_data_file),
                         'project/features/data/TC-T1/{}'.format(expected_data_file))

    def test_data_loader_mixin_load_text(self):
        "Prove BDDFeatureDataLoaderMixin load_text()"

        expected_data_file = 'text_data.txt'

        expected_data = 'Some text file.'
        mock_load_file = mock.mock_open(read_data=expected_data)

        loader = BDDFeatureDataLoaderMixin()
        loader.FEATURE_FILE = 'project/features/Texted.feature'

        with mock.patch('testharness.bdd.loader_mixins.common.open', mock_load_file):
            data = loader.load_text(expected_data_file)

            mock_load_file.assert_called_once_with(
                'project/features/data/Texted/{}'.format(expected_data_file),
                'rb')
            self.assertEqual(data, expected_data)


class JSONDataLoaderMixinTests(TestCase):

    def test_data_loader_mixin_load_json(self):
        "Prove JSONDataLoaderMixin load_json()"

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

    def test_data_loader_mixin_load_json_decode_error(self):
        "Prove JSONDataLoaderMixin load_json() raises ValueError on decode error"

        expected_data_file = 'api_data.json'

        # Invalid JSON data
        expected_data = "{'single': 'quotes', 'invalid': true}"
        mock_load_file = mock.mock_open(read_data=expected_data)

        loader = JSONDataLoaderMixin()
        loader.FEATURE_FILE = 'project/features/REST-API.feature'

        with self.assertRaisesRegex(DataFileError, loader.get_local_path(expected_data_file)):
            with mock.patch('testharness.bdd.loader_mixins.common.open', mock_load_file):
                loader.load_json(expected_data_file)

                mock_load_file.assert_called_once_with(
                    'project/features/data/REST-API/{}'.format(expected_data_file),
                    'rb')
