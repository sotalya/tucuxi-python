import sotalya.pycli as module

from utils import display_computing_query_response

DRUGS_FOLDER_PATHS = ["data_input/drugfiles"]
FILE_NAME = "data_input/ch.tucuxi.imatinib.gotta2012.2.tqf"

# import sys
# import resource
        
if __name__ == "__main__":
    # resource.setrlimit(resource.RLIMIT_STACK, [0x100000000, resource.RLIM_INFINITY])
    # resource.setrlimit(resource.RLIMIT_DATA, [0x100000000, resource.RLIM_INFINITY])
    # sys.setrecursionlimit(2000)

    with open(FILE_NAME, 'r') as file:
        data = file.read()

    results = module.compute_tqf2object(data, DRUGS_FOLDER_PATHS)

    print(f"Results are : {results}")
    display_computing_query_response(results)

    print("Press any key to continue...")
    input()

    result_xml = module.compute_tqf(data, DRUGS_FOLDER_PATHS)
    print(f"Results are : {result_xml}")