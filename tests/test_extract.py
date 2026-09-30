#!/usr/bin/python
# coding: utf-8

""" Tests for the bids_prov.extract module """

from os import remove
from os.path import abspath, join, exists
import json

from bids_prov.extract import get_subgraph, entry_point

TEST_DATA_DIR = abspath(join('tests', 'test_data'))

class TestExtractFunctions():
    """ All tests for the bids_prov.extract module """

    @staticmethod
    def test_get_subgraph():
        """ Test the get_subgraph function """

        with open(join(TEST_DATA_DIR, 'provenance_ds01.jsonld'), encoding = 'utf-8') as test_file:
            with open(join(TEST_DATA_DIR, 'test_extract_entry_point_2.jsonld'),
                encoding = 'utf-8') as expected_file:
                json_data = json.load(test_file)
                assert get_subgraph(json_data,
                    'bids::sub-01/anat/sub-01_T1w.nii') == json.load(expected_file)

            with open(join(TEST_DATA_DIR, 'test_extract_get_subgraph.jsonld'),
                encoding = 'utf-8') as expected_file:
                assert get_subgraph(json_data,
                    'bids::sub-01/func/meansub-01_task-tonecounting_bold.nii'
                    ) == json.load(expected_file)

    @staticmethod
    def test_entry_point(helpers):
        """ Test the entry_point function """

        output_filename = 'test_extract_entry_point.json-ld'

        if exists(output_filename):
            remove(output_filename)

        entry_point(join(TEST_DATA_DIR, 'provenance_ds00.jsonld'),
            'bids::sub-01/anat/sub-01_T1w.nii', output_filename)
        assert exists(output_filename)
        assert helpers.compare_files(
            output_filename, join(TEST_DATA_DIR, 'test_extract_entry_point_1.jsonld'))

        remove(output_filename)

        entry_point(join(TEST_DATA_DIR, 'provenance_ds01.jsonld'),
            'bids::sub-01/anat/sub-01_T1w.nii', output_filename)
        assert exists(output_filename)
        assert helpers.compare_files(
            output_filename, join(TEST_DATA_DIR, 'test_extract_entry_point_2.jsonld'))

        remove(output_filename)
