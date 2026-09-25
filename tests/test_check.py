#!/usr/bin/python
# coding: utf-8

""" Tests for the bids_prov.check module """

from os.path import abspath, join
import json

from bids_prov.check import analyse_activities

TEST_DATA_DIR = abspath(join('tests', 'test_data'))

# Here we use the caplog fixture from pytest to analyse log output
def test_analyse_activities(caplog):
    """ Test the analyse_activities function """

    with open(join(TEST_DATA_DIR, 'provenance_ds02.jsonld'), encoding = 'utf-8') as test_file:
       	analyse_activities(json.load(test_file))

	for record in caplog.records:
        assert record.levelname != "CRITICAL"
    assert "wally" not in caplog.text
