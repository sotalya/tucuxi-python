
import sotalya.pycli as module

import os
from utils import display_computing_query_response

from bs4 import BeautifulSoup

from sotalya.importexport.exporttqf import ExportTqf
from sotalya.data.query import Query

basename = os.path.dirname(__file__)

DRUGS_FOLDER_PATHS = [basename  + "/data_input/drugfiles"]
FILE_NAME = basename + "/data_input/ch.tucuxi.imatinib.gotta2012.2.tqf"

# import sys
# import resource
        
if __name__ == "__main__":
    # resource.setrlimit(resource.RLIMIT_STACK, [0x100000000, resource.RLIM_INFINITY])
    # resource.setrlimit(resource.RLIMIT_DATA, [0x100000000, resource.RLIM_INFINITY])
    # sys.setrecursionlimit(2000)

    with open(FILE_NAME, 'r') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'xml')

    if soup.query:
        try:
            query = Query(soup)
        
        except Exception as e:
            print('Can not import the following query file : ' + FILE_NAME)
            print(e)
            
    exporter = ExportTqf()
    new_content = exporter.export_to_string(query, "../sotalya/tucuxi/templates/query_template.tqf")

    print("Tqf Content is: ")
    print(new_content)

    results = module.compute_tqf2object(new_content, DRUGS_FOLDER_PATHS)

    print(f"Results are : {results}")
    display_computing_query_response(results)

    print("Press any key to continue...")
    input()

    result_xml = module.compute_tqf(new_content, DRUGS_FOLDER_PATHS)
    print(f"Results are : {result_xml}")