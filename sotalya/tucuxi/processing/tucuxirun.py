from colorama import Back, Fore
import subprocess
from subprocess import STDOUT, PIPE
from ..data.query import Query
from ..data.computingqueryresponse import QueryResponse
from ..importexport.exporttqf import *
from ..tucuxi.utils import CliStatusCode
from ..data.requests import *
from ..pycli import compute_tqf
# import requests


class TucuxiRun:

    def run_tucuxi(self, query: Query):
        pass


class TucuServerRun(TucuxiRun):

    def __init__(self, api_url):
        self.api_url = api_url
 

    def run_tucuxi(self, query: Query):

        # 1. Extract XML from query
        exporter_tqf = ExportTqf()
        xml_query = exporter_tqf.export_to_string(query)

        # 2. Execute query
        response = requests.post(self.api_url, data=xml_query)
        # print("status code: " + str(response.status_code))
        # print(response.text)

        # 3. Return the response if it went well
        # Check the response code first
        if response.status_code != 200:
            # something bad happened
            return None

        # If 200, then
        # Import from response.text
        xml_response = response.text
        soup = BeautifulSoup(xml_response, 'xml')
        query_response = QueryResponse(soup)

        statusCode = query_response.queryStatus.statusCode

        verify_cli_status(int(statusCode))

        return query_response

    def run_tucuxi_from_file(self, source_file: str):
        """
        This method runs an entire query, and builds the responses

        :param str source_file: The .tqf file containing the query
        :return: The query response
        :rtype: QueryResponse
        """

        print(Back.MAGENTA + '*************************************')
        print(Back.MAGENTA + 'RUNNING TUCUXI')
        print(Back.MAGENTA + '*************************************')

        # Execute query
        response = requests.post(self.api_url, data=source_file)
        # print("status code: " + str(response.status_code))
        # print(response.text)

        # 3. Return the response if it went well
        # Check the response code first
        if response.status_code != 200:
            # something bad happened
            return None

        # If 200, then
        # Import from response.text
        xml_response = response.text
        soup = BeautifulSoup(xml_response, 'xml')
        query_response = QueryResponse(soup)

        statusCode = query_response.queryStatus.statusCode

        verify_cli_status(int(statusCode))

        return query_response

class TucuCliRun(TucuxiRun):
    """
    This class exposes methods to prepare and execute the tucucli executable with arguments.
    Each execution of tucucli occurs in a new process.
    The sequence of commands and the flow of data is managed in the constructor, which accepts arguments from
    GlobalTester to configure what tucucli will do.
    Each command is echoed to the console such that to manually reproduce what this class automates, one could
    copy/paste the tucucli commands from the console output (useful in cases of error).
    """

    tucucli: str
    drug_path: str
    foldername: str

    def __init__(self, tucucli: str, drug_path: str, output_file: str):
        """
        This constructor only sets three values, the path to tucucli, and the path to the drug files
        and the output folder.

        :param str tucucli: The path to tucucli executable
        :param str drug_path: The path to the drug files
        :param str foldername: The folder in which the output file is generated
        """
        self.tucucli = tucucli
        self.drugPath = drug_path
        self.outputFile = output_file

    def run_tucuxi(self, query: Query):
        # TODO gérer avec le répertoire de travail en générant le fichier
        # en appelant ensuite run_tucuxi_from_file()
        return None

    def run_tucuxi_from_file(self, source_file: str):
        """
        This method runs an entire query, and builds the responses

        :param str source_file: The .tqf file containing the query
        :return: The query response
        :rtype: QueryResponse
        """
        print(Back.MAGENTA + '*************************************')
        print(Back.MAGENTA + 'RUNNING TUCUXI')
        print(Back.MAGENTA + '*************************************')

        proc = subprocess.run([self.tucucli, '-d', self.drugPath, '-i', source_file, '-o', self.outputFile],
                              stderr=STDOUT, stdout=PIPE)

        # exec_out = proc.stdout
        verify_cli_status(proc.returncode)

        try:
            content = open(self.outputFile).read()
            soup = BeautifulSoup(content, 'xml')

            queryresponse = QueryResponse(soup)
            return queryresponse
        except FileNotFoundError:
            print(Fore.RED + "File '" + self.outputFile + "' not found")
            return None


def verify_cli_status(status_code : int):
    if status_code != 0:
        print('\n')
        print(Back.RED + '*************************************')
        print(Fore.RED + 'Error with the execution of tucucli')
        print(Fore.RED + 'Return code : {code} ({msg})'.format(code=status_code,
                                                               msg=CliStatusCode(str(status_code)).name))
        print(Back.RED + '*************************************')

class TucuPycliRun(TucuxiRun):
    """
    This class exposes methods to prepare and execute the tucuxi core offered with python binding.
    """

    drug_path: str

    def __init__(self, drug_path: str):
        """
        This constructor only sets the path to the drug files.

        :param str drug_path: The path to the drug files
        """
        self.drugPath = drug_path

    def run_tucuxi(self, query: Query):
        """
        This method runs an entire query, and builds the responses

        :param Query query: The query to be run
        :return: The query response
        :rtype: QueryResponse
        """

        # 1. Extract XML from query
        exporter_tqf = ExportTqf()
        xml_query = exporter_tqf.export_to_string(query)
        result_xml = compute_tqf(xml_query, [self.drugPath])

        soup = BeautifulSoup(result_xml, 'xml')

        queryresponse = QueryResponse(soup)
        return queryresponse

    def run_tucuxi_from_file(self, source_file: str):
        """
        This method runs an entire query, and builds the responses

        :param str source_file: The .tqf file containing the query
        :return: The query response
        :rtype: QueryResponse
        """
        print(Back.MAGENTA + '*************************************')
        print(Back.MAGENTA + 'RUNNING TUCUXI')
        print(Back.MAGENTA + '*************************************')

        xml_query = open(source_file).read()
        result_xml = compute_tqf(xml_query, [self.drugPath])

        soup = BeautifulSoup(result_xml, 'xml')

        queryresponse = QueryResponse(soup)
        return queryresponse
