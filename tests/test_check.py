#!/usr/bin/python
# coding: utf-8

""" Tests for the bids_prov.check module """

from os.path import abspath, join
import json
from logging import INFO, DEBUG

from bids_prov.check import analyse_activities, entry_point

TEST_DATA_DIR = abspath(join('tests', 'test_data'))
TEST_DIR = abspath('tests')

class TestCheckFunctions():
    """ All tests for the bids_prov.check module """

    # Here we use the caplog fixture from pytest to analyse log output
    def test_analyse_activities(self, caplog):
        """ Test the analyse_activities function """
        caplog.set_level(INFO)

        for filename in ['provenance_ds01.jsonld', 'provenance_ds02.jsonld', 'provenance_ds03.jsonld']:
            # Clear log before each run
            caplog.clear()

            with open(join(TEST_DATA_DIR, filename), encoding = 'utf-8') as test_file:
                analyse_activities(json.load(test_file))

            assert "All prov:Activities that did not use any prov:Entity : 0" in caplog.text
            assert "All prov:Activity that did not generated any prov:Entity : 0" in caplog.text

    def test_analyse_activities_issues(self, caplog):
        """ Test the analyse_activities function with issues """
        caplog.set_level(INFO)

        caplog.clear()
        with open(join(TEST_DATA_DIR, 'test_check_1.jsonld'), encoding = 'utf-8') as test_file:
            analyse_activities(json.load(test_file))

        assert "All prov:Activities that did not use any prov:Entity : 2" in caplog.records[0].message
        assert "['<bids::prov#preprocessing-yBHdvts7>', '<bids::prov#movefile-26803be5>']" in caplog.records[1].message
        assert "All prov:Activity that did not generated any prov:Entity : 0" in caplog.records[2].message
        assert "[]" in caplog.records[3].message

        caplog.clear()
        with open(join(TEST_DATA_DIR, 'test_check_2.jsonld'), encoding = 'utf-8') as test_file:
            analyse_activities(json.load(test_file))

        assert "All prov:Activities that did not use any prov:Entity : 0" in caplog.records[0].message
        assert "[]" in caplog.records[1].message
        assert "All prov:Activity that did not generated any prov:Entity : 1" in caplog.records[2].message
        assert "['<bids::prov#conversion-00f3a18f>']" in caplog.records[3].message

        caplog.clear()
        with open(join(TEST_DATA_DIR, 'test_check_3.jsonld'), encoding = 'utf-8') as test_file:
            analyse_activities(json.load(test_file))

        assert "All prov:Activities that did not use any prov:Entity : 1" in caplog.records[0].message
        assert "['<bids::prov#preprocessing-xMpFqB5q>']" in caplog.records[1].message
        assert "All prov:Activity that did not generated any prov:Entity : 1" in caplog.records[2].message
        assert "['<bids::prov#preprocessing-xMpFqB5q>']" in caplog.records[3].message

    def test_entry_point(self, caplog):
        """ Test the entry_point function """

        caplog.set_level(INFO)
        caplog.clear()
        entry_point(join(TEST_DATA_DIR, 'test_check_1.jsonld'), None, False, False)
        assert "All prov:Activities that did not use any prov:Entity : 2" in caplog.records[1].message
        assert "['<bids::prov#preprocessing-yBHdvts7>', '<bids::prov#movefile-26803be5>']" in caplog.records[2].message
        assert "All prov:Activity that did not generated any prov:Entity : 0" in caplog.records[3].message
        assert "[]" in caplog.records[4].message

        caplog.set_level(DEBUG)
        caplog.clear()
        entry_point(join(TEST_DATA_DIR, 'test_check_1.jsonld'), None, False, True)
        assert len(caplog.records) == 10
        assert 'DEBUG' in set([r.levelname for r in caplog.records])

        caplog.set_level(INFO)
        caplog.clear()
        entry_point(None, TEST_DIR, False, False)
        assert len(caplog.records) == 0

        caplog.set_level(INFO)
        caplog.clear()
        entry_point(None, TEST_DIR, True, False)
        assert len(caplog.records) == 55
