#!/usr/bin/python
# coding: utf-8

""" Configuration for pytest """

from difflib import unified_diff

from pytest import fixture

from rdflib import Graph

class Helpers:
    """ A class for all pytest helper functions in the project """

    @staticmethod
    def compare_files(filename_a: str, filename_b: str) -> bool:
        """ Return True if file contents of files are identical, False otherwise """

        with open(filename_a, 'r', encoding='utf-8') as file_a:
            with open(filename_b, 'r', encoding='utf-8') as file_b:
                comp = list(unified_diff(file_a.readlines(), file_b.readlines()))
                return len(comp) == 0

    @staticmethod
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

@fixture
def helpers():
    """ A fixture to easily access the helpers from inside tests """
    return Helpers
