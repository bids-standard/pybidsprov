#!/usr/bin/python
# coding: utf-8

""" This module allows to perform sanity checks on JSONLD BIDSprov files. """

from argparse import ArgumentParser
import glob
from io import StringIO
import json
import logging

from pyld import jsonld

from rdflib import Dataset
from rdflib.namespace import PROV
from rdflib.plugins.sparql import prepareQuery

logger = logging.getLogger(__name__)

def analyse_activities(input_file: str):
    """ Print a report showing:
         - All prov:Activity that did not use any prov:Entity
         - All prov:Activity that did not generated any prov:Entity
    """
    logger.info('Analyse activities for file %s', input_file)

    # Open JSON-LD content
    with open(input_file, 'r', encoding = 'utf-8') as file_stream:
        input_graph = json.load(file_stream)

    # Expand the input JSON-LD
    expanded = jsonld.expand(input_graph)

    # Open file & create graph from it
    graph = Dataset()
    graph.parse(StringIO(json.dumps(expanded)), format='json-ld')

    # Print the graph
    logger.debug('Triples in the resulting graph : %s',
        len(list(graph.triples((None, None, None)))))

    # Search for all prov:Activity in the graph
    query = prepareQuery("""
        SELECT ?s ?p ?o WHERE {
            ?s a prov:Activity .
            ?s ?p ?o .
        }
        GROUP BY ?s
        """,
        initNs = {'prov': PROV}
        )
    all_activities = [s.n3(graph.namespace_manager) for s, _, _ in graph.query(query)]
    logger.debug('All prov:Activities : %s', len(all_activities))

    # Search for all prov:Activity that used something
    query = prepareQuery("""
        SELECT ?s ?p ?o WHERE {
            ?s a prov:Activity .
            ?s prov:used ?o .
            ?s ?p ?o .
        }
        GROUP BY ?s
        """,
        initNs = {'prov': PROV}
        )

    activities_that_used = [s.n3(graph.namespace_manager) for s, _, _ in graph.query(query)]
    logger.debug('All prov:Activities that used at least one prov:Entity : %s',
        len(activities_that_used))

    # Report all prov:Activity that that did not use anything
    activities_not_used = [s for s in all_activities if s not in activities_that_used]
    logger.info('All prov:Activities that did not use any prov:Entity : %s',
        len(activities_not_used))
    logger.info(activities_not_used)

    # Search for all prov:Activity that generated entities
    query = prepareQuery("""
        SELECT ?s ?p ?o WHERE {
            ?s a prov:Entity .
            ?s prov:wasGeneratedBy ?o .
            ?s ?p ?o .
        }
        GROUP BY ?o
        """,
        initNs = {'prov': PROV}
        )
    activities_that_generated = [o.n3(graph.namespace_manager) for _, _, o in graph.query(query)]
    logger.debug('All prov:Activity that generated at least one prov:Entity : %s',
        len(activities_that_generated))

    activities_not_generated = [s for s in all_activities if s not in activities_that_generated]
    logger.info('All prov:Activity that did not generated any prov:Entity : %s',
        len(activities_not_generated))
    logger.info(activities_not_generated)

if __name__ == '__main__':

    # Parse arguments
    parser = ArgumentParser(description='Analyse JSON-LD graph.')
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('-d', '--input_directory', type=str,
        help='input directory containing JSONLD files')
    inputs.add_argument('-f', '--input_file', type=str, help='input JSONLD file')
    parser.add_argument('-r', '--recursive', action='store_true', required=False, default=False,
        help='search recursively for files in the input directory')
    parser.add_argument('-v', '--verbose', action='store_true', help = 'verbose mode')
    arguments = parser.parse_args()

    # Init logging
    if arguments.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.StreamHandler().setLevel(logging.DEBUG)

    # Analyse files
    if arguments.input_file:
        analyse_activities(arguments.input_file)
    elif arguments.recursive:
        for file in glob.glob(arguments.input_directory + '/**/*.jsonld', recursive=True):
            analyse_activities(file)
    else:
        for file in glob.glob(arguments.input_directory + '/*.jsonld'):
            analyse_activities(file)
    arguments = parser.parse_args()
