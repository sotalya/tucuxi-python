#!/usr/bin/python3


import datetime

from colorama import Fore
import numbers

from datetime import datetime
from ..tucuxi.utils import str_to_datetime

from typing import List

class PRSample:
    def __init__(self):
        self.id = None
        self.sampledate = None
        self.arrivaldate = None
        self.analyteId = None
        self.concentration = 0.0
        self.unit = None
        self.metadata = {}

    @staticmethod
    def create_sample(sample_id, sampledate, analyte_id, concentration, unit, arrivaldate):
        sample = PRSample()
        sample.id = sample_id
        sample.sampledate = sampledate
        sample.analyteId = analyte_id
        sample.concentration = concentration
        sample.unit = unit
        sample.arrivaldate = arrivaldate
        return sample

    def is_valid(self):
        if not(type(self.sampledate) is datetime):
            print(Fore.RED + "Sample date invalid")
            return False
        # if not(type(self.arrivaldate) is datetime):
        #     print(Fore.RED + "Sample arrival date invalid")
        #     return False
        if not(type(self.analyteId) is str):
            print(Fore.RED + "Sample analyte Id is not a string")
            return False
        if self.analyteId == '':
            print(Fore.RED + "Sample analyte Id is empty")
            return False
        if not isinstance(self.concentration, numbers.Number):
            print(Fore.RED + "Sample concentration is not a number")
            return False
        if self.concentration < 0:
            print(Fore.RED + "Sample concentration is <= 0")
            return False
        if not(type(self.unit) is str):
            print(Fore.RED + "Sample unit is not a string")
            return False
        if self.unit == '':
            print(Fore.RED + "Sample unit is empty")
            return False
        return True


class PRPatientCovariate:
    def __init__(self):
        self.covariateId = None
        self.date = None
        self.value = None
        self.unit = None
        self.dataType = None
        self.nature = None

    @staticmethod
    def create_patient_covariate(covariate_id, date, value, unit, data_type, nature):
        covariate = PRPatientCovariate()
        covariate.covariateId = covariate_id
        covariate.date = date
        covariate.value = value
        covariate.unit = unit
        covariate.dataType = data_type
        covariate.nature = nature
        return covariate

    def is_valid(self) -> bool:
        if not(type(self.covariateId) is str):
            print(Fore.RED + "Covariate Id is not a string")
            return False
        if self.covariateId == '':
            print(Fore.RED + "Covariate Id is empty")
            return False

        if not(type(self.date) is datetime):
            print(Fore.RED + "Covariate " + self.covariateId + ": date is invalid")
            return False

        if not(type(self.value) is str):
            print(Fore.RED + "Covariate " + self.covariateId + ": value is not a string")
            return False
        if self.value == '':
            print(Fore.RED + "Covariate " + self.covariateId + ": value is empty")
            return False

        if not(type(self.unit) is str):
            print(Fore.RED + "Covariate " + self.covariateId + ": unit is not a string")
            return False
        if self.unit == '':
            print(Fore.RED + "Covariate " + self.covariateId + ": unit is empty")
            return False

        if not(type(self.dataType) is str):
            print(Fore.RED + "Covariate " + self.covariateId + ": data type is not a string")
            return False
        if self.value == '':
            print(Fore.RED + "Covariate " + self.covariateId + ": data type is empty")
            return False

        if not(type(self.nature) is str):
            print(Fore.RED + "Covariate " + self.covariateId + ": nature is not a string")
            return False
        if self.value == '':
            print(Fore.RED + "Covariate " + self.covariateId + ": nature is empty")
            return False

        return True


class PRDose:
    def __init__(self):
        self.doseValue = None
        self.doseUnit = None
        self.infusionTime = None
        self.infusionTimeUnit = None
        self.formulation = None
        self.administrationName = None
        self.administrationRoute = None

    def is_valid(self):
        if not(type(self.doseValue) is str):
            print(Fore.RED + "Dose value " + str(self.doseValue) + ": dose value is not a string")
            return False
        if self.doseValue == '':
            print(Fore.RED + "Dose value is empty")
            return False

        if not(type(self.doseUnit) is str):
            print(Fore.RED + "Dose unit " + str(self.doseUnit) + ": unit is not a string")
            return False
        if self.doseUnit == '':
            print(Fore.RED + "Dose unit is empty")
            return False

        if not(type(self.infusionTime) is str):
            print(Fore.RED + "infusionTime " + str(self.infusionTime) + ": value is not a string")
            return False
        if self.infusionTime == '':
            print(Fore.RED + "Dose infusionTime is empty")
            return False

        if not(type(self.infusionTimeUnit) is str):
            print(Fore.RED + "infusionTimeUnit " + str(self.infusionTimeUnit) + ": unit is not a string")
            return False
        if self.infusionTimeUnit == '':
            print(Fore.RED + "Dose infusionTimeUnit is empty")
            return False

        if not(type(self.formulation) is str):
            print(Fore.RED + "formulation " + str(self.formulation) + ": formulation is not a string")
            return False
        if self.formulation == '':
            print(Fore.RED + "Dose formulation is empty")
            return False

        if not(type(self.administrationName) is str):
            print(Fore.RED + "administrationName " + str(self.administrationName) + ": administrationName is not a string")
            return False
        if self.administrationName == '':
            print(Fore.RED + "Dose administrationName is empty")
            return False

        if not(type(self.administrationRoute) is str):
            print(Fore.RED + "administrationRoute " + str(self.administrationRoute) +
                  ": administrationRoute is not a string")
            return False
        if self.administrationRoute == '':
            print(Fore.RED + "Dose administrationRoute is empty")
            return False

        return True


class PRDosageRepeat:
    def __init__(self):
        self.startDate = datetime(1, 1, 1)  # Year 1, month 1, day 1
        self.endDate = datetime(1, 1, 1)  # Year 1, month 1, day 1
        self.interval = -1
        self.interval_unit = ''
        self.dose = PRDose()

    def is_valid(self):
        # TODO : Better check validity
        return self.dose.is_valid()


class PRSingleDose:
    def __init__(self):
        self.date = datetime(1, 1, 1)  # Year 1, month 1, day 1
        self.dose = PRDose()

    def is_valid(self):
        # TODO : Better check validity
        return self.dose.is_valid()


class PRDrugTreatment:
    samples: List[PRSample]
    # targets: List[Target]
    # dosages: List[]
    patientCovariates: List[PRPatientCovariate]

    def __init__(self):
        self.drugId = ''
        self.activePrinciple = ''
        self.brandName = ''
        self.samples = []  # Must contain objects of type Sample
        self.targets = []  # Must contain objects of type Target
        self.dosages = []  # Must contain objects of type related to Dosage
        self.patientCovariates = []  # Must contain objects of type PatientCovariate

    def is_valid(self):
        if not(type(self.drugId) is str):
            print(Fore.RED + "DrugTreatment drugId is not a string")
            return False
        if self.drugId == '':
            print(Fore.RED + "DrugTreatment drugId is empty")
            return False
        if not(type(self.activePrinciple) is str):
            print(Fore.RED + "DrugTreatment activePrinciple is not a string")
            return False
        if self.activePrinciple == '':
            print(Fore.RED + "DrugTreatment activePrinciple is empty")
            return False
        if len(self.samples) != 0:
            for sample in self.samples:
                if not sample.is_valid():
                    print(Fore.RED + "DrugTreatment has at least one wrong sample")
                    return False
        if len(self.targets) != 0:
            for target in self.targets:
                if not target.is_valid():
                    print(Fore.RED + "DrugTreatment has at least one wrong target")
                    return False
        if len(self.dosages) != 0:
            for dosage in self.dosages:
                if not dosage.is_valid():
                    print(Fore.RED + "DrugTreatment has at least one wrong dosage")
                    return False
        if len(self.patientCovariates) != 0:
            for patientCovariate in self.patientCovariates:
                if not patientCovariate.is_valid():
                    print(Fore.RED + "DrugTreatment has at least one wrong patientCovariate")
                    return False
        return True
