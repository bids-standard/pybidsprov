#!/usr/bin/python
# coding: utf-8

""" Test data for the bids_prov.visualize module """

test_data = """
    @prefix prov: <http://www.w3.org/ns/prov#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    <bids::.> a prov:Collection ;
        rdfs:label "Current dataset" ;
        prov:wasGeneratedBy <bids::prov#activity_1> .

    <bids:ds000011:.> a prov:Collection ;
        rdfs:label "ds00011" .

    <bids::prov#activity_1> a prov:Activity ;
        rdfs:label "Activity 1" ;
        prov:used <bids:ds000011:.> .

    <bids::prov#activity_2> a prov:Activity ;
        rdfs:label "Activity 2" ;
        prov:used <bids::.> .
    """

expected_data_1 = """
    @prefix prov: <http://www.w3.org/ns/prov#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    <bids::prov#activity_2> a prov:Activity ;
        rdfs:label "Activity 2" ;
        prov:used <bids:ds> .

    <bids::prov#activity_1> a prov:Activity ;
        rdfs:label "Activity 1" ;
        prov:used <bids:ds000011> .

    <bids:ds> a prov:Collection ;
        rdfs:label "Current dataset" ;
        prov:wasGeneratedBy <bids::prov#activity_1> .

    <bids:ds000011> a prov:Collection ;
        rdfs:label "ds00011" .
    """

expected_data_2 = """
    @prefix prov: <http://www.w3.org/ns/prov#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    <bids::.> a prov:Collection ;
        a prov:Entity ;
        rdfs:label "Current dataset" ;
        prov:wasGeneratedBy <bids::prov#activity_1> .

    <bids:ds000011:.> a prov:Collection ;
        a prov:Entity ;
        rdfs:label "ds00011" .

    <bids::prov#activity_1> a prov:Activity ;
        rdfs:label "Activity 1" ;
        prov:used <bids:ds000011:.> .

    <bids::prov#activity_2> a prov:Activity ;
        rdfs:label "Activity 2" ;
        prov:used <bids::.> .
    """

expected_data_3 = """
    @prefix prov: <http://www.w3.org/ns/prov#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    <bids::sub-02/anat/sub-02_T1w.json> a prov:Entity ;
        rdfs:label "sub-02_T1w.json" ;
        prov:wasGeneratedBy <bids::prov#conversion-00f3a18f> .

    <bids::sub-02/anat/sub-02_T1w.nii> a prov:Entity ;
        rdfs:label "sub-02_T1w.nii" ;
        prov:wasGeneratedBy <bids::prov#conversion-00f3a18f> .

    <bids::prov#dcm2niix-khhkm7u1> a prov:Agent ;
        rdfs:label "dcm2niix" .

    <bids::prov#fedora-uldfv058> a prov:Entity ;
        rdfs:label "Fedora release 36 (Thirty Six)" .

    <bids::sourcedata/hirni-demo/acq1/dicoms/example-dicom-structural-master/dicoms> a prov:Entity ;
        rdfs:label "dicoms" .

    <bids::prov#conversion-00f3a18f> a prov:Activity ;
        rdfs:label "Conversion" ;
        prov:used <bids::prov#fedora-uldfv058>,
            <bids::sourcedata/hirni-demo/acq1/dicoms/example-dicom-structural-master/dicoms> ;
        prov:wasAssociatedWith <bids::prov#dcm2niix-khhkm7u1> .
"""
