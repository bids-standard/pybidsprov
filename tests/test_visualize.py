#!/usr/bin/python
# coding: utf-8

""" Tests for the bids_prov.visualize module """

from os import remove
from os.path import abspath, join, exists, getsize
from math import isclose
import json

from bids_prov.visualize import (
    replace_dataset_ids, subtype_datasets, turtle_to_image,
    jsonld10_to_turtle, jsonld11_to_jsonld10, entry_point
    )
from test_data.visualize import (
    test_data, expected_data_1, expected_data_2, expected_data_3
    )

TEST_DATA_DIR = abspath(join('tests', 'test_data'))

class TestVisualizeFunctions():
    """ All tests for the bids_prov.visualize module """

    @staticmethod
    def test_replace_dataset_ids(helpers):
        """ Test the replace_dataset_ids function"""
        helpers.compare_graphs(replace_dataset_ids(test_data), expected_data_1)

    @staticmethod
    def test_subtype_datasets(helpers):
        """ Test the subtype_dataset function"""
        helpers.compare_graphs(subtype_datasets(expected_data_1), expected_data_2)

    @staticmethod
    def test_turtle_to_image():
        """ Test the turtle_to_image function
    
            From the same input graph, two output images from graphviz will not necessarly be
            the same bytewise or even pixelwise (although they represent the same graph).
            Therefore, we cannot compare them with e.g. filecmp.cmp
            In this method, the test assumes that their size in kilobytes will approx. be the same.
        """

        output_filename = 'test_turtle_to_image.png'

        if exists(output_filename):
            remove(output_filename)
        turtle_to_image(expected_data_1, output_filename, False)
        assert exists(output_filename)

        # Bytewise comparison
        # assert filecmp.cmp(output_filename, join(TEST_DATA_DIR, 'test_turtle_to_image_1.png'))

        # Byte size comparison
        assert isclose(
            getsize(join(TEST_DATA_DIR, 'test_turtle_to_image_1.png')) / 1024,
            getsize(output_filename) / 1024,
            abs_tol=1 #kB
            )
        remove(output_filename)

        turtle_to_image(expected_data_2, output_filename, True)
        assert exists(output_filename)
        assert isclose(
            getsize(join(TEST_DATA_DIR, 'test_turtle_to_image_2.png')) / 1024,
            getsize(output_filename) / 1024,
            abs_tol=1 #kB
            )
        remove(output_filename)

    @staticmethod
    def test_jsonld11_to_jsonld10():
        """ Test the jsonld11_to_jsonld10 function"""
        with open(join(TEST_DATA_DIR, 'provenance_ds02.jsonld'), encoding = 'utf-8') as test_file:
            with open(join(TEST_DATA_DIR, 'provenance_ds02_jsonld10.jsonld'),
                encoding = 'utf-8') as expected_file:
                assert jsonld11_to_jsonld10(json.load(test_file)) == json.load(expected_file)

    @staticmethod
    def test_jsonld10_to_turtle(helpers):
        """ Test the jsonld10_to_turtle function"""
        with open(join(TEST_DATA_DIR, 'provenance_ds02_jsonld10.jsonld'),
            encoding = 'utf-8') as test_file:
            helpers.compare_graphs(jsonld10_to_turtle(json.load(test_file)), expected_data_3)

    @staticmethod
    def test_entry_point():
        """ Test the entry_point function"""

        output_filename = 'test_visualize_entry_point.png'

        if exists(output_filename):
            remove(output_filename)

        entry_point(join(TEST_DATA_DIR, 'provenance_ds01.jsonld'), output_filename, False)
        assert exists(output_filename)

        remove(output_filename)

        entry_point(join(TEST_DATA_DIR, 'provenance_ds01.jsonld'), output_filename, True)
        assert exists(output_filename)

        remove(output_filename)
