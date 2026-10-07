#!/usr/bin/python
# coding: utf-8

""" This module allows to perform sanity checks on JSON-LD BIDS-Prov files. """

import glob
from io import StringIO
import json
import logging
from importlib import resources

from pyld import jsonld

from jsonschema import Draft202012Validator

from rdflib import Dataset
from rdflib.namespace import PROV
from rdflib.plugins.sparql import prepareQuery

logger = logging.getLogger(__name__)

JSON_SCHEMA = resources.read_text('bids_prov', 'schema.json', encoding='utf-8')

def analyse_activities(jsonld_11: dict):
    """ Print a report showing:
         - All prov:Activity that did not use any prov:Entity
         - All prov:Activity that did not generated any prov:Entity

        jsonld_11: dict, input graph data to analyse
    """
    # Expand the input JSON-LD
    expanded = jsonld.expand(jsonld_11)

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
    nb_activities = len(activities_not_used)
    log_message = 'All prov:Activities that did not use any prov:Entity : %s'
    if nb_activities == 0:
        logger.info(log_message, nb_activities)
    else:
        logger.warning(log_message, nb_activities)
        logger.info(activities_not_used)

    # Search for all prov:Activity that generated entities
    query = prepareQuery("""
        SELECT ?s ?p ?o WHERE {
            VALUES ?type { prov:Entity prov:Collection }
            ?s a ?type .
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
    nb_activities = len(activities_not_generated)
    log_message = 'All prov:Activity that did not generated any prov:Entity : %s'
    if nb_activities == 0:
        logger.info(log_message, nb_activities)
    else:
        logger.warning(log_message, nb_activities)
        logger.info(activities_not_generated)

def validate(jsonld_11: dict) -> bool:
    """ Validate JSON-LD content against the BIDS-Prov JSON schema """

    # Setup and run validator
    validator = Draft202012Validator(json.loads(JSON_SCHEMA))
    errors = sorted(validator.iter_errors(jsonld_11), key=lambda e: e.path)

    # Display errors from validator as log lines
    for error in errors:
        logger.error('In %s: %s', error.json_path, error.message)

def analyse_connectivity(jsonld_11: dict):
    """ Print a report showing:
         - All nodes that are not connected

        jsonld_11: dict, input graph data to analyse
    """
    # Expand the input JSON-LD
    expanded = jsonld.expand(jsonld_11)

    # Open file & create graph from it
    graph = Dataset()
    graph.parse(StringIO(json.dumps(expanded)), format='json-ld')

    # Search for all not connected prov:Activity in the data
    query_activities = prepareQuery("""
        SELECT ?s WHERE {
            ?s a prov:Activity .
            FILTER NOT EXISTS { ?s prov:used ?x } .
            FILTER NOT EXISTS { ?s prov:wasAssociatedWith ?y } .
            FILTER NOT EXISTS { ?z prov:wasGeneratedBy ?s } .
            FILTER NOT EXISTS { ?t prov:wasInformedBy ?s } .
            FILTER NOT EXISTS { ?s prov:wasInformedBy ?u } .
        }
        """,
        initNs = {'prov': PROV}
        )
    isolated_activities = [s[0].n3(graph.namespace_manager) for s in graph.query(query_activities)]
    nb_activities = len(isolated_activities)
    log_message = 'All prov:Activity that are not connected to the graph : %s'
    if nb_activities == 0:
        logger.info(log_message, nb_activities)
    else:
        logger.warning(log_message, nb_activities)
        logger.info(isolated_activities)

    # Search for all not connected prov:Entity or prov:Collection in the data
    query_entities = prepareQuery("""
        SELECT ?s WHERE {
            VALUES ?type { prov:Entity prov:Collection }
            ?s a ?type .
            FILTER NOT EXISTS { ?s prov:wasGeneratedBy ?x } .
            FILTER NOT EXISTS { ?y prov:used ?s } .
            FILTER NOT EXISTS { ?s prov:wasDerivedForm ?z } .
            FILTER NOT EXISTS { ?t prov:wasDerivedForm ?s } .
            FILTER NOT EXISTS { ?s prov:wasAttributedTo ?u } .
        }
        """,
        initNs = {'prov': PROV}
        )
    isolated_entities = [s[0].n3(graph.namespace_manager) for s in graph.query(query_entities)]
    nb_entities = len(isolated_entities)
    log_message = 'All prov:Entity or prov:Collection that are not connected to the graph : %s'
    if nb_entities == 0:
        logger.info(log_message, nb_entities)
    else:
        logger.warning(log_message, nb_entities)
        logger.info(isolated_entities)

    # Search for all not connected prov:Agent in the data
    query_agents = prepareQuery("""
        SELECT ?s WHERE {
            ?s a prov:Agent .
            FILTER NOT EXISTS { ?s prov:actedOnBehalfOf ?x } .
            FILTER NOT EXISTS { ?y prov:actedOnBehalfOf ?s } .
            FILTER NOT EXISTS { ?z prov:wasAttributedTo ?s } .
            FILTER NOT EXISTS { ?t prov:wasAssociatedWith ?s } .
        }
        """,
        initNs = {'prov': PROV}
        )
    isolated_agents = [s[0].n3(graph.namespace_manager) for s in graph.query(query_agents)]
    nb_agents = len(isolated_agents)
    log_message = 'All prov:Agent that are not connected to the graph : %s'
    if nb_agents == 0:
        logger.info(log_message, nb_agents)
    else:
        logger.warning(log_message, nb_agents)
        logger.info(isolated_agents)

def entry_point(input_file:str, input_directory:str, recursive:bool, verbose:bool) -> None:
    """ Perform sanity check on JSON-LD BIDS-Prov file(s). """

    # Init logging
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logging.StreamHandler().setLevel(logging.DEBUG)

    # List file(s)
    file_list = []
    if input_file:
        file_list.append(input_file)
    elif recursive:
        for file in glob.glob(input_directory + '/**/*.jsonld', recursive=True):
            file_list.append(file)
    else:
        for file in glob.glob(input_directory + '/*.jsonld'):
            file_list.append(file)

    # Analyse file(s)
    for file in file_list:

        # Open JSON-LD content & analyse
        with open(file, 'r', encoding = 'utf-8') as file_stream:
            data = json.load(file_stream)

        logger.info('Analyse activities for file %s', file)
        analyse_activities(data)

        logger.info('Analyse connectivity for file %s', file)
        analyse_connectivity(data)

        logger.info('Validate file %s', file)
        validate(data)
