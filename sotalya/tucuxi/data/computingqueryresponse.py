#!/usr/bin/python

from ..tucuxi.utils import str_to_datetime, str_to_time, CliStatusCode
from datetime import timedelta


class QueryResponse:
    def __init__(self, soup):
        self.soup = soup
        self.queryId = soup.tucuxiComputation.queryId.string
        self.queryStatus = Status(soup.queryStatus)
        self.responses = []
        if soup.responses:
            for r in soup.responses.find_all('response'):
                self.responses.append(Response(r))


class Status:
    def __init__(self, soup):
        self.statusCode = soup.statusCode.string
        self.statusCodeLit = soup.statusCodeLit.string
        self.message = soup.message.string
        self.description = soup.description.string


class Response:
    def __init__(self, soup):
        self.requestId = soup.requestId.string
        self.requestStatus = Status(soup.requestStatus)
        if soup.dataAdjustment:
            computing_trait = DataAdjustement(soup.dataAdjustment)
        elif soup.dataPrediction:
            computing_trait = DataPrediction(soup.dataPrediction)
        elif soup.dataPoints:
            computing_trait = DataPoints(soup.dataPoints)
        elif soup.dataPercentiles:
            computing_trait = DataPercentiles(soup.dataPercentiles)
        else:
            return None

        self.requestType = soup.requestType.string
        self.computingTrait = computing_trait


class DataPrediction:
    def __init__(self, soup):
        if soup.logLikelihood:
            self.loglikelihood = float(soup.logLikelihood.string)
        self.analyteIds = []
        for an in soup.analyteIds.find_all('analyteId'):
            self.analyteIds.append(an.string)

        self.cycleDatas = []
        for cd in soup.cycleDatas.find_all('cycleData'):
            self.cycleDatas.append(CycleData(cd))


class DataPoints:
    def __init__(self, soup):
        self.unit = soup.unit.string

        self.points = []
        for p in soup.points.find_all('point'):
            self.points.append(Point(p))


class Point:
    def __init__(self, soup):
        self.time = soup.time.string
        self.value = float(soup.value.string)


class DataPercentiles:
    def __init__(self, soup):
        self.percentileList = []

        for p in soup.find_all('percentile'):
            self.percentileList.append(Percentile(p))


class Percentile:
    def __init__(self, soup):
        self.rank = soup.rank.string
        self.cycleDatas = []
        for cd in soup.cycleDatas.find_all('cycleData'):
            self.cycleDatas.append(CycleData(cd))


class DataAdjustement:
    def __init__(self, soup):
        self.analyteIds = []
        for an in soup.analyteIds.find_all('analyteId'):
            self.analyteIds.append(an.string)

        self.adjustments = []
        for ad in soup.adjustments.find_all('adjustment'):
            self.adjustments.append(Adjustement(ad))


class Adjustement:
    def __init__(self, soup):
        self.score = soup.score.string

        self.dosageHistory = DosageHistory(soup.dosageHistory)

        self.cycleDatas = []
        for cd in soup.cycleDatas.find_all('cycleData'):
            self.cycleDatas.append(CycleData(cd))

        self.targetEvaluations = []
        if soup.targetEvaluations:
            for te in soup.targetEvaluations.find_all('targetEvaluation'):
                self.targetEvaluations.append(TargetEvaluation(te))


class TargetEvaluation:
    def __init__(self, soup):
        self.targetType = soup.targetType.string
        self.unit = soup.unit.string
        self.value = float(soup.value.string)
        self.score = soup.score


class CycleData:
    def __init__(self, soup):
        self.start = str_to_datetime(soup.start.string)
        self.end = str_to_datetime(soup.end.string)
        self.unit = soup.unit.string

        self.parameters = []
        for p in soup.parameters.find_all('parameter'):
            self.parameters.append(Container(p))

        self.covariates = []
        for c in soup.covariates.find_all('covariate'):
            self.covariates.append(Container(c))

        self.times = []
        for time in soup.times.string.split(','):
            self.times.append(float(time))

        self.values = []
        for value in soup.values.string.split(','):
            self.values.append(float(value))

        self.statistics = Statistics(soup.statistics)


class Container:
    def __init__(self, soup):
        self.id = soup.id.string
        self.value = float(soup.value.string)


class Statistics:
    def __init__(self, soup):
        self.mean = float(soup.mean.string)
        self.auc = float(soup.auc.string)
        self.auc24 = float(soup.auc24.string)
        self.cumulativeAuc = float(soup.cumulativeAuc.string)
        self.residual = float(soup.residual.string)
        self.peak = float(soup.peak.string)


class DosageHistory:
    def __init__(self, h):
        self.dosageTimeRanges = []
        for d in h.find_all('dosageTimeRange'):
            self.dosageTimeRanges.append(DosageTimeRange(d))


class DosageTimeRange:
    def __init__(self, d):
        self.start = str_to_datetime(d.start.string)
        self.end = str_to_datetime(d.end.string)

        if d.dosage.dosageLoop:
            dosage = choose_dosage(d.dosage.dosageLoop)
        else:
            dosage = choose_dosage(d.dosage)

        self.dosage = dosage


class DosageRepeatResponse:
    def __init__(self, soup):
        self.iterations = soup.iterations

        if soup.lastingDosage:
            dosage = LastingDosageResponse(soup.lastingDosage)
        elif soup.dailyDosage:
            dosage = DailyDosageResponse(soup.dailyDosage)
        else:
            dosage = WeeklyDosageResponse(soup.weeklyDosage)

        self.dosage = dosage


class DosageSequenceResponse:
    def __init__(self, soup):

        if soup.lastingDosage:
            dosage = LastingDosageResponse(soup.lastingDosage)
        elif soup.dailyDosage:
            dosage = DailyDosageResponse(soup.dailyDosage)
        else:
            dosage = WeeklyDosageResponse(soup.weeklyDosage)

        self.dosage = dosage


def choose_dosage(soup):
    if soup.dosageRepeat:
        dosage = DosageRepeatResponse(soup.dosageRepeat)
    elif soup.dosageSequence:
        dosage = DosageSequenceResponse(soup.dosageSequence)
    elif soup.lastingDosage:
        dosage = LastingDosageResponse(soup.lastingDosage)
    elif soup.dailyDosage:
        dosage = DailyDosageResponse(soup.dailyDosage)
    else:
        dosage = WeeklyDosageResponse(soup.weeklyDosage)
    return dosage


class LastingDosageResponse:
    def __init__(self, soup):
        self.interval = str_to_time(soup.interval.string)
        self.dose = Dose(soup.dose)
        self.formulationAndRoute = FormulationAndRoute(soup.formulationAndRoute)


class DailyDosageResponse:
    def __init__(self, soup):
        self.time = str_to_time(soup.time.string)
        self.dose = Dose(soup.dose)
        self.formulationAndRoute = FormulationAndRoute(soup.formulationAndRoute)


class WeeklyDosageResponse:
    def __init__(self, soup):
        # TODO : create day
        self.day = soup.day.string
        self.time = str_to_time(soup.time.string)
        self.dose = Dose(soup.dose)
        self.formulationAndRoute = FormulationAndRoute(soup.formulationAndRoute)


class FormulationAndRoute:
    def __init__(self, soup):
        self.formulation = soup.formulation.string
        self.administrationName = soup.administrationName.string
        self.administrationRoute = soup.administrationRoute.string
        self.absorptionModel = soup.absorptionModel.string


class Dose:
    def __init__(self, soup):
        self.value = float(soup.value.string)
        self.unit = soup.unit.string
        infusion = soup.infusionTimeInMinutes.string
        self.infusionTimeInMinutes = timedelta(minutes=float(infusion))
