# todo : add tests
# From a few query examples, verify the run and the results
# Maybe create a few incomplete/wrong queries and verify the status accordingly

from datetime import timedelta
from utils import display_computing_query_response

import sotalya.pycli as M

DRUGS_FOLDER_PATHS = ["../../tucuxi-drugs/drugfiles"]

DURATION_30_MINUTES = timedelta(minutes=30)
DURATION_24_HOURS = timedelta(hours=24)

### --- Query parameters --- ###
query_id = 'ch.tucuxi.tobramycin.hennig2013-wrapper-example'
client_id = '1'
query_date = M.DateTime("2022-05-05", "%Y-%m-%d")
language = 'en'

### --- Drug parameters --- ###
drug_id = 'tobramycin'
activePrinciple = 'tobramycin'
brandName = 'Empty'
atc = 'Empty'

var = M.CycleData.start

### --- Dates --- ###
start_date = M.DateTime("2018-10-08", "%Y-%m-%d")
sample_date = M.DateTime("2018-10-06 12:00:00", "%Y-%m-%d %H:%M:%S")
dosage_start_date = M.DateTime("2018-10-06 08:00:00", "%Y-%m-%d %H:%M:%S")
dosage_end_date = M.DateTime("2018-10-08 08:00:00", "%Y-%m-%d %H:%M:%S")

### --- Units --- ###
umol_l_unit = M.TucuUnit('umol/l')
kg_unit = M.TucuUnit('kg')
mg_unit = M.TucuUnit('mg')
mg_l_unit = M.TucuUnit('mg/l')
empty_unit = M.TucuUnit('-')

### --- Patient --- ###
cov1 = M.PatientCovariate('bodyweight', '80', M.DataType.double, kg_unit, start_date)
cov2 = M.PatientCovariate('scr', '40.7', M.DataType.double, umol_l_unit, start_date)
cov3 = M.PatientCovariate('sex', '0', M.DataType.double, empty_unit, start_date)
covariates = [cov1, cov2, cov3]

M.TargetEvaluationResult.target_type

### --- Dosage --- ###
form_and_route = M.FormulationAndRoute(M.Formulation.parenteral_solution,
                                       M.AdministrationRoute.intravenous_drip,
                                       M.AbsorptionModel.infusion,
                                       'foo bar')

# Duration default constructor was made in seconds
# infusion_time = M.Duration(DURATION_30_MINUTES) # 30 minutes
# interval = M.Duration(DURATION_24_HOURS)        # 24 hours
infusion_time = M.Duration(DURATION_30_MINUTES)
interval = M.Duration(DURATION_24_HOURS)

lasting = M.LastingDose(560, mg_unit, form_and_route, infusion_time, interval)
dosage_time_range = M.DosageTimeRange(dosage_start_date, dosage_end_date, lasting)
ranges = [dosage_time_range]

### --- Sample --- ###
analyte_id = M.AnalyteId('tobramycin')
sample = M.FullSample("Test", sample_date, analyte_id, 0.7, mg_l_unit, 1)
samples = [sample]

### --- Targets --- ###
targets = []

### --- Requests --- ###
request_id = 'population_1'
drug_id = 'tobramycin'
drugmodel_id = 'ch.tucuxi.tobramycin.hennig2013'
parameters_type = M.PredictionParameterType.population
compartment_option = M.CompartmentsOption.all_active_moieties
retrieve_statistics = M.RetrieveStatisticsOption.retrieve_statistics
retrieve_parameters = M.RetrieveParametersOption.retrieve_parameters
retrieve_covariates = M.RetrieveCovariatesOption.retrieve_covariates
force_option = M.ForceUgPerLiterOption.do_not_force # todo : default value force or not ?
nb_pts = 20
computing_options = M.ComputingOption(parameters_type,
                                      compartment_option,
                                      retrieve_statistics,
                                      retrieve_parameters,
                                      retrieve_covariates,
                                      force_option)
computing_trait = M.ComputingTraitConcentration(request_id, dosage_start_date, dosage_end_date, nb_pts, computing_options)
M.create_request_data(request_id, drug_id, drugmodel_id, computing_trait)



request_id = 'apriori_1'
parameters_type = M.PredictionParameterType.apriori
computing_options = M.ComputingOption(parameters_type,
                                      compartment_option,
                                      retrieve_statistics,
                                      retrieve_parameters,
                                      retrieve_covariates,
                                      force_option)
computing_trait = M.ComputingTraitConcentration(request_id, dosage_start_date, dosage_end_date, nb_pts, computing_options)
M.create_request_data(request_id, drug_id, drugmodel_id, computing_trait)



request_id = 'aposteriori_2'
parameters_type = M.PredictionParameterType.aposteriori
computing_options = M.ComputingOption(parameters_type,
                                      compartment_option,
                                      retrieve_statistics,
                                      retrieve_parameters,
                                      retrieve_covariates,
                                      force_option)
computing_trait = M.ComputingTraitConcentration(request_id, dosage_start_date, dosage_end_date, nb_pts, computing_options)
M.create_request_data(request_id, drug_id, drugmodel_id, computing_trait)


request_id = 'apriori_1_percentiles'
parameters_type = M.PredictionParameterType.apriori
computing_options = M.ComputingOption(parameters_type,
                                      compartment_option,
                                      retrieve_statistics,
                                      retrieve_parameters,
                                      retrieve_covariates,
                                      force_option)
ranks = [5, 10, 25, 50, 75, 90, 95]
computing_trait = M.ComputingTraitPercentiles(request_id, dosage_start_date, dosage_end_date, ranks, nb_pts, computing_options)
M.create_request_data(request_id, drug_id, drugmodel_id, computing_trait)

# requests = [request1, request2, request3, request4]

result = M.compute_query_data(query_id,
                    client_id,
                    query_date,
                    language,
                    drug_id,
                    activePrinciple,
                    brandName,
                    atc,
                    covariates,
                    samples,
                    targets,
                    ranges,
                    DRUGS_FOLDER_PATHS)

print(result)

display_computing_query_response(result)


# DateTime and Duration
DURATION_24_HOURS = timedelta(hours=24)
interval = M.Duration(DURATION_24_HOURS)
sample_date = M.DateTime("2018-10-06", "%Y-%m-%d")
