#!/usr/bin/python
# coding: utf-8

""" Tests for the bids_prov.visualize module """

from os import remove
from os.path import abspath, join, exists
import json
from filecmp import cmp

from rdflib import Graph

from bids_prov.visualize import (
    replace_dataset_ids, subtype_datasets, turtle_to_image,
    jsonld10_to_turtle, jsonld11_to_jsonld10, entry_point
    )
from test_data.visualize import (
    test_data, expected_data_1, expected_data_2, expected_data_3
    )

TEST_DATA_DIR = abspath(join('tests', 'test_data'))

def compare_graphs(turtle_a: str, turtle_b: str):
    """ Comparte two turtle graphs passed as strings """

    graph_a = Graph()
    graph_a.parse(data=turtle_a, format='turtle')
    graph_b = Graph()
    graph_b.parse(data=turtle_b, format='turtle')

    # Assert all triples from one graph are in the other
    for triple in graph_b:
        assert graph_a.query(f"""
            ASK {{
                {triple[0].n3(graph_b.namespace_manager)}
                {triple[1].n3(graph_b.namespace_manager)}
                {triple[2].n3(graph_b.namespace_manager)}
            }}
            """)
    for triple in graph_a:
        assert graph_b.query(f"""
            ASK {{
                {triple[0].n3(graph_a.namespace_manager)}
                {triple[1].n3(graph_a.namespace_manager)}
                {triple[2].n3(graph_a.namespace_manager)}
            }}
            """)

def test_replace_dataset_ids():
    """ Test the replace_dataset_ids function"""
    compare_graphs(replace_dataset_ids(test_data), expected_data_1)

def test_subtype_datasets():
    """ Test the subtype_dataset function"""
    compare_graphs(subtype_datasets(test_data), expected_data_2)

def test_turtle_to_image():
    """ Test the turtle_to_image function"""

    output_filename = 'test_turtle_to_image.png'

    if exists(output_filename):
        remove(output_filename)
    turtle_to_image(expected_data_1, output_filename, False)
    assert exists(output_filename)
    assert cmp(output_filename, join(TEST_DATA_DIR, 'test_turtle_to_image_1.png'))
    remove(output_filename)

    turtle_to_image(expected_data_1, output_filename, True)
    assert exists(output_filename)
    assert cmp(output_filename, join(TEST_DATA_DIR, 'test_turtle_to_image_2.png'))
    remove(output_filename)

def test_jsonld11_to_jsonld10():
    """ Test the jsonld11_to_jsonld10 function"""
    with open(join(TEST_DATA_DIR, 'provenance_ds02.jsonld'), encoding = 'utf-8') as test_file:
        with open(join(TEST_DATA_DIR, 'provenance_ds02_jsonld10.jsonld'), encoding = 'utf-8') as expected_file:
            assert jsonld11_to_jsonld10(json.load(test_file)) == json.load(expected_file)

def test_jsonld10_to_turtle():
    """ Test the jsonld10_to_turtle function"""
    with open(join(TEST_DATA_DIR, 'provenance_ds02_jsonld10.jsonld'), encoding = 'utf-8') as test_file:
        compare_graphs(jsonld10_to_turtle(json.load(test_file)), expected_data_3)

def test_entry_point():
    """ Test the entry_point function"""
    return
