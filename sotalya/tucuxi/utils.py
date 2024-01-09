import os
from colorama import Fore
import sys
from typing import List
import subprocess
from subprocess import Popen, check_output
from datetime import *
from enum import Enum
from inspect import getframeinfo, stack

BOOLEAN = "BOOLEAN"
PATH = "PATH"
URL = "URL"

def raise_exception(message: str):
    caller = getframeinfo(stack()[1][0])
    print("%s:%d - %s" % (caller.filename, caller.lineno, message))
    raise RuntimeError(caller.filename + ":" + str(caller.lineno) + " - " + str(message))

def are_args_given(config_values: dict):
    # False if one or more of the requested path is missing (does not check boolean value)
    pathsflag = True
    for value in config_values.values():
        pathsflag = pathsflag and (False if value == "" else True)
    return pathsflag


def are_paths_wrong(config_values: dict):
    # True if one of all the requested path is missing (does not check boolean value)
    pathsflag = False
    for value in config_values.values():
        pathsflag = pathsflag or not (False if value == "" else True)
    return pathsflag


def choose_data_from(configfile, dictionary: dict, dictsection: str, variablename: str):
    # Cmd line argument is priority to config.ini value. If no value (neither config.ini value nor cmd line argument),
    # some case take default value some other not --> error is underlined afterward
    try:
        if not configfile[dictsection][variablename]:
            if not dictionary[variablename]:
                if dictsection == PATH:
                    check_path_section(dictionary, variablename)

                elif dictsection == URL:
                    dictionary[variablename] = "http://193.134.218.125:9090/" + variablename
                    print(Fore.RED, variablename +
                          " value not found, default was choosen : http://193.134.218.125:9090/" + variablename)

                elif dictsection == BOOLEAN:
                    dictionary[variablename] = False
                    print(Fore.RED + variablename + " value not found. Set to false.\n")
                else:
                    print(Fore.RED + "ERROR, wrong dictionary section")
                    raise_exception("ERROR, wrong dictionary section")

                configfile[dictsection][variablename] = str(dictionary[variablename])
        else:
            if dictionary[variablename]:
                configfile[dictsection][variablename] = str(dictionary[variablename])
            else:
                if dictsection == BOOLEAN:
                    dictionary[variablename] = evaluate_boolean(configfile[dictsection][variablename])
                else:
                    dictionary[variablename] = configfile[dictsection][variablename]
    except KeyError:
        print(Fore.RED, "Error, missing variable ", variablename, " in section ", dictsection)
        raise_exception("Error, missing variable " + variablename + " in section " + dictsection)


def evaluate_boolean(variable):
    if variable == 'False' or variable == 'false' or variable == '0' or variable == 'FALSE':
        return False
    elif variable == 'True' or variable == 'true' or variable == '1' or variable == 'TRUE':
        return True
    else:
        print("Error with boolean values in config.ini")
        raise_exception("Error with casting a boolean")


def check_path_section(dictionary, variablename):
    if variablename == 'queryfile':
        filename = 'query_template.tqf'
        dictionary[variablename] = os.path.join(os.getcwd(), "..", "common", "templates", filename)
        print(Fore.RED,
              variablename + " value not found, default was choosen : ../common/../templates/" + variablename)
    elif variablename == 'requesttemplate':
        filename = 'request_template.xml'
        dictionary[variablename] = os.path.join(os.getcwd(), "..", "common", "templates", filename)
        print(Fore.RED,
              variablename + " value not found, default was choosen : ../common/../templates/" + variablename)
    elif variablename == 'listtemplate':
        filename = 'List_template.xml'
        dictionary[variablename] = os.path.join(os.getcwd(), "..", "common", "templates", filename)
        print(Fore.RED,
              variablename + " value not found, default was choosen : ../common/../templates/" + variablename)
    else:
        dictionary[variablename] = ""
        print(Fore.RED + variablename + " value not found. Nothing was set.\n")


def str_to_time(string):
    td = string.split(':')
    return timedelta(hours=int(td[0]), minutes=int(td[1]), seconds=int(td[2]))


def str_to_datetime(string):
    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')

def timedelta_to_str(td):
    seconds = td.total_seconds()
    interval_hour = seconds / 3600
    interval_minute = round((interval_hour - int(interval_hour)) * 60)
    interval_second = (interval_minute - int(interval_minute)) * 60
    return "{h}:{m}:{s}".format(h=int(interval_hour), m=int(interval_minute), s=interval_second)

def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]

def run_cmd(command: List[str]):
    if get_platform() == 'Windows':
        process = subprocess.Popen('cmd.exe', shell=False, universal_newlines=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        concatenate = ''
        for cmd in command:
            concatenate = concatenate + cmd + '\n'
        out, err = process.communicate(concatenate)
    else:
        concatenate = ''
        for cmd in command:
            concatenate = concatenate + cmd + ';'

        check_output([concatenate, ''], shell=True)


class CliStatusCode(Enum):
    Ok = "0"
    PartiallyOk = "1"
    Error = "2"
    ImportError = "3"
    BadFormat = "4"
    Undefined = "5"