#!/usr/bin/python

from datetime import datetime, timedelta, time
from colorama import Fore
from ..tucuxi.utils import str_to_datetime, str_to_time
from ..data.requests import Request
from typing import List


class Query:
    queryId: str
    sourceFile: str
    patientId: str
    date: datetime
    requests: List[Request]

    def __init__(self, soup=None):
        self.sourceFile = ''
        self.queryId = ''
        self.patientId = ''
        self.date = str_to_datetime("1111-11-11T11:11:11")
        self.covariates = []
        self.drugs = []
        self.requests = []

        if soup is not None:
            self.queryId = soup.query.queryId.string
            for cov in soup.drugTreatment.patient.covariates.find_all('covariate'):
                self.covariates.append(Covariate(cov))

            for d in soup.drugs.find_all('drug'):
                self.drugs.append(Drug(d))

            if soup.query.requests:
                for r in soup.query.requests.find_all('request'):
                    self.requests.append(Request.create_from_soup(r))

        self.isgenerated = False

    def get_id(self):
        return self.queryId


def get_sample_time(item):
    return item.sampledate


class Sample:
    id: str
    sampleDate: datetime
    concentration: float
    analyteId: str
    unit: str
    metadata: dict

    def __init__(self, s=None):
        self.id = ""
        self.sampledate = str_to_datetime("1111-11-11T11:11:11")
        self.concentration = 0.0
        self.analyteId = ""
        self.unit = ""
        self.metadata = {}

        if s is not None:
            self.id = s.sampleId.string
            self.sampledate = str_to_datetime(s.sampleDate.string)
            self.concentration = float(s.concentrations.concentration.value.string)
            self.analyteId = s.concentrations.concentration.analyteId.string
            self.unit = s.concentrations.concentration.unit.string

    @staticmethod
    def create_sample(sample_id, sampledate, analyte_id, concentration, unit):
        sample = Sample()
        sample.id = sample_id
        sample.sampledate = sampledate
        sample.analyteId = analyte_id
        sample.concentration = concentration
        sample.unit = unit
        return sample

    def is_valid(self):
        if not (type(self.sampledate) is datetime):
            print(Fore.RED + "Sample date invalid")
            return False
        if not (type(self.analyteId) is str):
            print(Fore.RED + "Sample analyte Id is not a string")
            return False
        if self.analyteId == '':
            print(Fore.RED + "Sample analyte Id is empty")
            return False
        # if not isinstance(self.concentration, int):
        #     print(Fore.RED + "Sample concentration is not an int")
        #     return False
        if self.concentration < 0:
            print(Fore.RED + "Sample concentration is <= 0")
            return False
        if not (type(self.unit) is str):
            print(Fore.RED + "Sample unit is not a string")
            return False
        if self.unit == '':
            print(Fore.RED + "Sample unit is empty")
            return False
        return True


class Target:
    activeMoietyId: str
    targetType: str
    unit: str
    inefficacyAlarm: str
    min: str
    best: str
    max: str
    toxicityAlarm: str

    def __init__(self, t):
        self.activeMoietyId = t.activeMoietyId.string
        self.targetType = t.targetType.string
        self.unit = t.unit.string
        self.inefficacyAlarm = t.inefficacyAlarm.string
        self.min = t.min.string
        self.best = t.best.string
        self.max = t.max.string
        self.toxicityAlarm = t.toxicityAlarm.string

    def is_valid(self) -> bool:
        if not(type(self.activeMoietyId) is str):
            print(Fore.RED + "Target active moiety Id is not a string")
            return False
        if self.activeMoietyId == '':
            print(Fore.RED + "Target active moiety Id is empty")
            return False
        if not(type(self.targetType) is str):
            print(Fore.RED + "Target type is not a string")
            return False
        if self.targetType == '':
            print(Fore.RED + "Target type is empty")
            return False
        if not(type(self.unit) is str):
            print(Fore.RED + "Target unit is not a string")
            return False
        if self.unit == '':
            print(Fore.RED + "Target unit is empty")
            return False
        if not(type(self.inefficacyAlarm) is str):
            print(Fore.RED + "Target inefficacy alarm is not a string")
            return False
        if self.inefficacyAlarm == '':
            print(Fore.RED + "Target inefficacy alarm is empty")
            return False
        if not(type(self.min) is str):
            print(Fore.RED + "Target min value not a string")
            return False
        if self.min == '':
            print(Fore.RED + "Target min value is empty")
            return False
        if not(type(self.best) is str):
            print(Fore.RED + "Target best value is not a string")
            return False
        if self.best == '':
            print(Fore.RED + "Target best value is empty")
            return False
        if not(type(self.max) is str):
            print(Fore.RED + "Target max value is not a string")
            return False
        if self.max == '':
            print(Fore.RED + "Target max value is empty")
            return False
        if not(type(self.toxicityAlarm) is str):
            print(Fore.RED + "Target toxicity alarm is not a string")
            return False
        if self.toxicityAlarm == '':
            print(Fore.RED + "Target toxicity alarm is empty")
            return False



class Covariate:
    covariateId: str
    date: str
    value: str
    unit: str
    dataType: str
    nature: str

    def __init__(self, cov=None):
        self.covariateId = ""
        self.date = ""
        self.value = ""
        self.unit = ""
        self.dataType = ""
        self.nature = ""

        if cov is not None:
            self.covariateId = cov.covariateId.string
            self.date = cov.date.string
            self.value = cov.value.string
            self.unit = cov.unit.string
            self.dataType = cov.dataType.string
            self.nature = cov.nature.string

    @staticmethod
    def create_covariate(covariate_id, date, value, unit, data_type, nature):
        covariate = Covariate()
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


class DosageTime:
    start: datetime
    end: datetime

    def __init__(self, d=None):
        self.start = str_to_datetime("1111-11-11T11:11:11")
        self.end = str_to_datetime("1111-11-11T11:11:11")
        self.dosage = None
        if d is not None:
            self.start = str_to_datetime(d.start.string)
            self.end = str_to_datetime(d.end.string)

            if d.dosage.dosageLoop:
                dosage = choose_dosage(d.dosage.dosageLoop)
            else:
                dosage = choose_dosage(d.dosage)

            self.dosage = dosage

    @staticmethod
    def create_dosage_time_range(start: datetime, dosage, end: datetime):
        dosage_time_range = DosageTime()
        dosage_time_range.start = start
        dosage_time_range.end = end
        dosage_time_range.dosage = dosage
        return dosage_time_range

    def is_valid(self):
        if not (type(self.start) is datetime):
            print(Fore.RED + "Dosage start date invalid")
            return False
        if not (type(self.end) is datetime):
            print(Fore.RED + "Dosage start date invalid")
            return False
        return True


class DosageHistory:
    dosageTimeRanges: List[DosageTime]

    def __init__(self, h=None):
        self.dosageTimeRanges = []
        if h is not None:
            for d in h.find_all('dosageTimeRange'):
                self.dosageTimeRanges.append(DosageTime(d))


class DosageRepeat:
    iterations: str

    def __init__(self, soup=None):
        self.iterations = ''
        self.dosage = None
        if soup is not None:
            self.iterations = soup.iterations.string
            if soup.lastingDosage:
                dosage = LastingDosage(soup.lastingDosage)
            elif soup.dailyDosage:
                dosage = DailyDosage(soup.dailyDosage)
            else:
                dosage = WeeklyDosage(soup.weeklyDosage)

            self.dosage = dosage

    def is_valid(self)-> bool:
        return self.dosage.is_valid()

class DosageSequence:
    def __init__(self, soup=None):
        self.dosage = None
        if soup is not None:
            if soup.lastingDosage:
                dosage = LastingDosage(soup.lastingDosage)
            elif soup.dailyDosage:
                dosage = DailyDosage(soup.dailyDosage)
            else:
                dosage = WeeklyDosage(soup.weeklyDosage)

            self.dosage = dosage

    def is_valid(self)-> bool:
        return self.dosage.is_valid()


def choose_dosage(soup):
    if soup.dosageRepeat:
        dosage = DosageRepeat(soup.dosageRepeat)
    elif soup.dosageSequence:
        dosage = DosageSequence(soup.dosageSequence)
    elif soup.lastingDosage:
        dosage = LastingDosage(soup.lastingDosage)
    elif soup.dailyDosage:
        dosage = DailyDosage(soup.dailyDosage)
    else:
        dosage = WeeklyDosage(soup.weeklyDosage)
    return dosage


class FormulationAndRoute:
    formulation: str
    administrationName: str
    administrationRoute: str
    absorptionModel: str

    def __init__(self, soup=None):
        self.formulation = ''
        self.administrationName = ''
        self.administrationRoute = ''
        self.absorptionModel = ''
        if soup is not None:
            self.formulation = soup.formulation.string
            self.administrationName = soup.administrationName.string
            self.administrationRoute = soup.administrationRoute.string
            self.absorptionModel = soup.absorptionModel.string


class Dose:
    value: float
    unit: str
    infusionTimeInMinutes: timedelta

    def __init__(self, soup=None):
        self.value = float(0)
        self.unit = ''
        self.infusionTimeInMinutes = str_to_time('00:00:00')
        if soup is not None:
            self.value = float(soup.value.string)
            self.unit = soup.unit.string
            infusion = soup.infusionTimeInMinutes.string
            self.infusionTimeInMinutes = timedelta(minutes=float(infusion))

    def get_infusion_time_in_minutes(self):
        return self.infusionTimeInMinutes.total_seconds() // 60


class LastingDosage:
    interval: timedelta
    dose: Dose
    formulationAndRoute: FormulationAndRoute

    def __init__(self, soup=None):
        self.interval = str_to_time("00:00:00")
        self.dose = Dose()
        self.formulationAndRoute = FormulationAndRoute()
        if soup is not None:
            self.interval = str_to_time(soup.interval.string)
            self.dose = Dose(soup.dose)
            self.formulationAndRoute = FormulationAndRoute(soup.formulationAndRoute)

    def is_valid(self)-> bool:
        if not (type(self.interval) is time):
            print(Fore.RED + "Dosage interval invalid")
            return False


class DailyDosage:
    time: timedelta
    dose: Dose
    formulationAndRoute: FormulationAndRoute

    def __init__(self, soup=None):
        self.time = str_to_time("00:00:00")
        self.dose = Dose()
        self.formulationAndRoute = FormulationAndRoute()
        if soup is not None:
            self.time = str_to_time(soup.time.string)
            self.dose = Dose(soup.dose)
            self.formulationAndRoute = FormulationAndRoute(soup.formulationAndRoute)

    def is_valid(self)-> bool:
        if not (type(self.time) is time):
            print(Fore.RED + "Dosage time invalid")
            return False


class WeeklyDosage:
    day: str
    time: timedelta
    dose: Dose
    formulationAndRoute: FormulationAndRoute

    def __init__(self, soup=None):
        # TODO : create day
        self.day = ''
        self.time = str_to_time("00:00:00")
        self.dose = Dose()
        self.formulationAndRoute = FormulationAndRoute()
        if soup is not None:
            self.day = soup.day.string
            self.time = str_to_time(soup.time.string)
            self.dose = Dose(soup.dose)
            self.formulationAndRoute = FormulationAndRoute(soup.formulationAndRoute)

    def is_valid(self)-> bool:
        if not (type(self.time) is time):
            print(Fore.RED + "Dosage time invalid")
            return False

class Drug:
    drugId: str
    activePrinciple: str
    brandName: str
    ATC: str
    samples: List[Sample]
    targets: List[Target]
    dosageHistory: DosageHistory

    def __init__(self, d=None):
        self.drugId = ''
        self.activePrinciple = ''
        self.brandName = ''
        self.ATC = ''
        self.samples = []
        self.targets = []
        self.dosageHistory = DosageHistory()
        if d is not None:
            self.drugId = d.drugId.string
            self.activePrinciple = d.activePrinciple.string
            self.brandName = d.brandName.string
            self.ATC = d.atc.string
            self.samples = []
            for s in d.samples.find_all('sample'):
                self.samples.append(Sample(s))
            self.samples.sort(key=get_sample_time)
            self.targets = []
            if d.targets:
                for t in d.targets.find_all('target'):
                    self.targets.append(Target(t))
            self.dosageHistory = DosageHistory(d.treatment.dosageHistory)


class DrugTreatment:
    drugId: str
    activePrinciple: str
    samples: List[Sample]
    targets: List[Target]
    patientCovariates: List[Covariate]

    def __init__(self):
        self.drugId = ''
        self.activePrinciple = ''
        self.samples = []  # Must contain objects of type Sample
        self.targets = []  # Must contain objects of type Target
        self.dosages = []  # Must contain objects of type related to Dosage
        self.patientCovariates = []  # Must contain objects of type Covariate

    def is_valid(self):
        if not (type(self.drugId) is str):
            print(Fore.RED + "DrugTreatment drugId is not a string")
            return False
        if self.drugId == '':
            print(Fore.RED + "DrugTreatment drugId is empty")
            return False
        if not (type(self.activePrinciple) is str):
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


class IntakeEvent:
    date: datetime
    doseValue: str
    doseInfusionInMin: int

    def __init__(self):
        self.date = str_to_datetime("1111-11-11T00:00:00")
        self.doseValue = ""
        self.doseInfusionInMin = 0
