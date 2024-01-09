#!/usr/bin/python3


from ..data.prdrugtreatment import *
from colorama import Fore
from ..data.query import *


class Mandator:
    def __init__(self):
        self.name = ''

    def is_valid(self):
        if not(type(self.name) is str):
            print(Fore.RED + "Mandator name is not a string")
            return False
        return True


class Patient:
    def __init__(self):
        self.firstname = ''
        self.lastname = ''
        self.patientId = ''

    def is_valid(self):
        if not(type(self.patientId) is str):
            print(Fore.RED + "Patient Id is not a string")
            return False
        if self.patientId == '':
            print(Fore.RED + "Patient Id is empty")
            return False

        return True


class Clinical:
    def __init__(self):
        self.name = ''
        self.date = None
        self.value = ''
        self.comments = []

    def is_valid(self):
        # TODO : Better validity check
        if not(type(self.name) is str):
            print(Fore.RED + "Clinical name is not a string")
            return False
        if self.name == '':
            print(Fore.RED + "Clinical name is empty")
            return False
        return True


class PendingRequest:
    requestId: str
    drugTreatment: DrugTreatment
    patient: Patient
    mandator: Mandator
    requestId: str
    requestState: str
    clinicals: List[Clinical]

    def __init__(self):
        # self.drugTreatment = None  # Must be a DrugTreatment
        # self.patient = None  # Must be a Patient
        # self.mandator = None  # Must be a mandator
        self.requestId = ''
        self.requestState = ''
        self.clinicals = []

    def is_valid(self):
        if self.drugTreatment is None:
            print(Fore.RED + "Pending request without a drug treatment")
            return False
        if not self.drugTreatment.is_valid():
            print(Fore.RED + "Pending request with an invalid drug treatment")
            return False
        if self.patient is None:
            print(Fore.RED + "Pending request without a patient")
            return False
        if not self.patient.is_valid():
            print(Fore.RED + "Pending request with an invalid patient")
            return False
        if not (self.mandator is None):
            if not self.mandator.is_valid():
                return False

        if len(self.clinicals) != 0:
            for clinical in self.clinicals:
                if not clinical.is_valid():
                    print(Fore.RED + "DrugTreatment has at least one wrong clinical")
                    return False
        return True
