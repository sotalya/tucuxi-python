import sotalya.pycli as pycli
import xml.etree.ElementTree as ET
import os

drugfiles_path = ["data_input/drugfiles"]
computing_queries_path = "data_input/computing-queries"


def test_compute_objects():
    # pycli.compute_objects(computing_queries_path, drugfiles_path)
    a = 1


def test_compute_tqf2object():
    for dir_path, _, computing_queries in os.walk(computing_queries_path):
        for query in computing_queries:
            with open(os.path.join(dir_path, query), 'r') as file:
                data = file.read()
            file.close()

            results = pycli.compute_tqf2object(data, drugfiles_path)

            # Check that all requests went right
            assert results.query_status == pycli.QueryStatus.ok

            for srd in results.responses:
                assert srd.computing_response.computing_status == pycli.ComputingStatus.ok


def test_compute_tqf():
    for dir_path, _, computing_queries in os.walk(computing_queries_path):
        for query in computing_queries:
            with open(os.path.join(dir_path, query), 'r') as file:
                data = file.read()
            file.close()

            xml_string = pycli.compute_tqf(data, drugfiles_path)

            # Read xml string as tree and check that all requests went right
            tree = ET.fromstring(xml_string)
            if tree[1][0].tag == "queryStatus":
                assert tree[1][0].text == "0"
            for request_status in tree.iter('requestStatus'):
                assert request_status[0].text == "0"
