#!/usr/bin/python3

from datetime import datetime
from enum import Enum
from typing import List
from abc import ABC
from colorama import Back

from ..tucuxi.utils import str_to_time, str_to_datetime, evaluate_boolean


class DateInterval:

    startDate: datetime
    endDate: datetime

    def __init__(self, start, end):
        self.startDate = start
        self.endDate = end

    @staticmethod
    def create_from_soup(soup):
        start_date = str_to_datetime(soup.start.string)
        end_date = str_to_datetime(soup.end.string)
        return DateInterval(start_date, end_date)


class BestCandidatesOption(Enum):
    bestDosage = 'bestDosage'
    allDosages = 'allDosages'
    bestDosagePerInterval = 'bestDosagePerInterval'


class LoadingOption(Enum):
    noLoadingDose = 'noLoadingDose'
    loadingDoseAllowed = 'loadingDoseAllowed'


class RestPeriodOption(Enum):
    noRestPeriod = 'noRestPeriod'
    restPeriodAllowed = 'restPeriodAllowed'


class SteadyStateTargetOption(Enum):
    atSteadyState = 'atSteadyState'
    withinTreatmentTimeRange = 'withinTreatmentTimeRange'


class TargetExtractionOption(Enum):
    populationValues = 'populationValues'
    aprioriValues = 'aprioriValues'
    individualTargets = 'individualTargets'
    individualTargetsIfDefinitionExists = 'individualTargetsIfDefinitionExists'
    definitionIfNoIndividualTarget = 'definitionIfNoIndividualTarget'
    individualTargetsIfDefinitionExistsAndDefinitionIfNoIndividualTarget = \
        'individualTargetsIfDefinitionExistsAndDefinitionIfNoIndividualTarget'


class FormulationAndRouteSelectionOption(Enum):
    lastFormulationAndRoute = 'lastFormulationAndRoute'
    defaultFormulationAndRoute = 'defaultFormulationAndRoute'
    allFormulationAndRoutes = 'allFormulationAndRoutes'


class CompartmentOptionEnum(Enum):
    allActiveMoieties = "allActiveMoieties"
    allAnalytes = "allAnalytes"
    allCompartments = "allCompartments"
    specific = "specific"


class ParametersTypeEnum(Enum):
    population = "population"
    apriori = "apriori"
    aposteriori = "aposteriori"
    best = "best"


class ComputingOption:
    def __init__(self, parameters_type: ParametersTypeEnum, compartment_option: CompartmentOptionEnum,
                 retrieve_statistics: bool, retrieve_parameters: bool, retrieve_covariates: bool):
        self.parametersType = parameters_type
        self.compartmentOption = CompartmentOptionEnum(compartment_option)
        self.retrieveStatistics = retrieve_statistics
        self.retrieveParameters = retrieve_parameters
        self.retrieveCovariates = retrieve_covariates

    @staticmethod
    def create_from_soup(soup):
        # Only tag used in tucuvalidation
        # TODO : Parse correctly the soup object
        parameters_type = choose_parameters_type(soup.parametersType.string)
        compartment_option = soup.compartmentOption.string
        retrieve_statistics = evaluate_boolean(soup.retrieveStatistics.string)
        retrieve_parameters = evaluate_boolean(soup.retrieveParameters.string)
        retrieve_covariates = evaluate_boolean(soup.retrieveCovariates.string)
        return ComputingOption(parameters_type, compartment_option, retrieve_statistics, retrieve_parameters,
                               retrieve_covariates)


class AdjustementOptions:

    bestCandidatesOption: BestCandidatesOption
    loadingOption: LoadingOption
    restPeriodOption: RestPeriodOption
    steadyStateTargetOption: SteadyStateTargetOption
    targetExtractionOption: TargetExtractionOption
    formulationAndRouteSelectionOption: FormulationAndRouteSelectionOption

    def __init__(self, best_candidates_option, loading_option, rest_period_option,
                 steady_state_target_option, target_extraction_option, formulation_and_route_selection_option):
        self.bestCandidatesOption = BestCandidatesOption(best_candidates_option)
        self.loadingOption = LoadingOption(loading_option)
        self.restPeriodOption = RestPeriodOption(rest_period_option)
        self.steadyStateTargetOption = SteadyStateTargetOption(steady_state_target_option)
        self.targetExtractionOption = TargetExtractionOption(target_extraction_option)
        self.formulationAndRouteSelectionOption = FormulationAndRouteSelectionOption(
            formulation_and_route_selection_option)


class Request:

    requestId: str
    drugId: str
    drugModelId: str

    def __init__(self, request_id='', drug_id='', drug_model_id='', computing_traits=None):
        self.requestId = request_id
        self.drugId = drug_id
        self.drugModelId = drug_model_id
        self.computingTraits = computing_traits

    @staticmethod
    def create_from_soup(soup):
        request_id = soup.requestId.string
        drug_id = soup.drugId.string
        drug_model_id = soup.drugModelId.string
        computing_traits = ComputingTraits.create_from_soup(soup)
        return Request(request_id, drug_id, drug_model_id, computing_traits)

    def get_id(self):
        return self.requestId


class ComputingTrait(ABC):
    pass


class ComputingTraits:
    computingTraits: ComputingTrait

    def __init__(self, traits):
        self.computingTraits = traits

    @staticmethod
    def create_from_soup(soup):
        computing_traits = None
        if soup.predictionTraits:
            computing_traits = PredictionTraits.create_from_soup(soup.predictionTraits)
        elif soup.predictionAtTimesTraits:
            computing_traits = PredictionAtTimesTraits.create_from_soup(soup.predictionAtTimesTraits)
        elif soup.predictionAtSampleTimesTraits:
            computing_traits = PredictionAtSampleTimesTraits.create_from_soup(soup.predictionAtSampleTimesTraits)
        elif soup.percentilesTraits:
            computing_traits = PercentilesTraits.create_from_soup(soup.percentilesTraits)
        elif soup.adjustmentTraits:
            computing_traits = AdjustementTraits.create_from_soup(soup.adjustmentTraits)
        else:
            print('Error, invalid requested computing trait')
        return ComputingTraits(computing_traits)


class PredictionTraits(ComputingTrait):
    def __init__(self, computing_option, nb_points_per_hour, dateinterval):
        self.computingOption = computing_option
        self.nbPointPerHour = nb_points_per_hour
        self.dateInterval = dateinterval
        self.requestType = RequestType('prediction')
    @staticmethod
    def create_from_soup(soup):
        computing_option = ComputingOption.create_from_soup(soup.computingOption)
        nb_points_per_hour = int(soup.nbPointsPerHour.string)
        date_interval = DateInterval.create_from_soup(soup.dateInterval)
        return PredictionTraits(computing_option, nb_points_per_hour, date_interval)

    @staticmethod
    def create_prediction_traits(nb_point_per_hour, start_date, end_date, computing_option):
        predictiontraits = PredictionTraits(computing_option, nb_point_per_hour, DateInterval(start_date, end_date))
        return predictiontraits


class PredictionAtTimesTraits(ComputingTrait):

    def __init__(self, computing_option, dates):
        self.dates = dates
        self.computingOption = computing_option
        self.requestType = RequestType('singlePoints')

    @staticmethod
    def create_from_soup(soup):
        computing_option = ComputingOption.create_from_soup(soup.computingOption)


        dates = soup.dates

        d = 0
        while(d < len(dates.contents)):
            if (hasattr(dates.contents[d], "date") == False):
                dates.contents.remove(dates.contents[d])
            else:
                d=d+1


        return PredictionAtTimesTraits(computing_option, dates)

    @staticmethod
    def create_prediction_at_time_traits(date, computing_option):
        dates = []
        dates.append(date)
        predictionattimestraits = PredictionAtTimesTraits(computing_option, dates)
        return predictionattimestraits

    @staticmethod
    def create_prediction_at_times_traits(dates, computing_option):
        predictionattimestraits = PredictionAtTimesTraits(computing_option, dates)
        return predictionattimestraits


class PredictionAtSampleTimesTraits(ComputingTrait):
    def __init__(self, computing_option):
        self.computingOption = computing_option
        self.requestType = RequestType('predictionAtSample')

    @staticmethod
    def create_from_soup(soup):
        computing_option = ComputingOption.create_from_soup(soup.computingOption)
        return PredictionAtSampleTimesTraits(computing_option)

    @staticmethod
    def create_prediction_at_sample_time_traits(computing_option):
        predictionatsampletimetraits = PredictionAtSampleTimesTraits(computing_option)
        return predictionatsampletimetraits


class PercentilesTraits(ComputingTrait):

    computingOption: ComputingOption
    nbPointsPerHour: float
    dataInterval: DateInterval
    ranks: List[float]

    def __init__(self, computing_option, nb_points_per_hour, date_interval, ranks):
        self.computingOption = computing_option
        self.nbPointPerHour = nb_points_per_hour
        self.dateInterval = date_interval
        self.ranks = ranks
        self.requestType = RequestType('percentiles')

    @staticmethod
    def create_from_soup(soup):
        computing_option = ComputingOption.create_from_soup(soup.computingOption)
        nb_point_per_hour = int(soup.nbPointsPerHour.string)
        date_interval = DateInterval.create_from_soup(soup.dateInterval)
        ranks = []
        for r in soup.ranks.find_all('rank'):
            ranks.append(float(r.string))

        return PercentilesTraits(computing_option, nb_point_per_hour, date_interval, ranks)

    @staticmethod
    def create_percentiles_traits(nb_point_per_hour, start_date, end_date, computing_option, ranks):
        percentilestraits = PercentilesTraits(computing_option, nb_point_per_hour, DateInterval(start_date, end_date),
                                              ranks)
        return percentilestraits


class AdjustementTraits(ComputingTrait):
    def __init__(self, computing_option, nb_point_per_hour, date_interval, adjustment_date, options):
        self.computingOption = computing_option
        self.nbPointPerHour = nb_point_per_hour
        self.dateInterval = date_interval
        self.adjustmentDate = adjustment_date
        self.options = options
        self.requestType = RequestType('adjustment')

    @staticmethod
    def create_from_soup(soup):
        computing_option = ComputingOption.create_from_soup(soup.computingOption)
        nb_point_per_hour = int(soup.nbPointsPerHour.string)
        date_interval = DateInterval.create_from_soup(soup.dateInterval)
        # TODO Parse the two fields
        adjustment_date = None
        options = None
        return AdjustementTraits(computing_option, nb_point_per_hour, date_interval, adjustment_date, options)

    @staticmethod
    def create_adjustements_traits(computing_option, nb_point_per_hour, start_date, end_date, adjustment_date, options):
        adjustmenttraits = AdjustementTraits(computing_option, nb_point_per_hour, DateInterval(start_date, end_date),
                                             adjustment_date, options)
        return adjustmenttraits


def choose_parameters_type(choice):
    if choice == 'population':
        return ParametersTypeEnum.population
    elif choice == 'apriori':
        return ParametersTypeEnum.apriori
    elif choice == 'aposteriori':
        return ParametersTypeEnum.aposteriori
    elif choice == 'best':
        return ParametersTypeEnum.best
    else:
        print(Back.RED + 'Parameters type undefined')
        return None


class RequestType(Enum):
    Prediction = 'prediction'
    Percentiles = 'percentiles'
    Adjustment = 'adjustment'
    PredictionAtSampleTime = 'predictionAtSample'
    PredictionAtTimes = 'singlePoints'