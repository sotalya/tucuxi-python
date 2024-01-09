#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/chrono.h>

#include "wrapper.h"

#include <fstream>

#ifndef MODULE_NAME
  #define MODULE_NAME mod
#endif

namespace Tucuxi {
namespace PyWrap {

Core::IDrugModelRepository* drugModelRepository = nullptr;

Query::ComputingQueryResponse compute_objects(Query::QueryData& _queryData, const std::vector<std::string> _folders)
{
    Query::ComputingQueryResponse computingQueryResponse;

    if (drugModelRepository == nullptr)
    {
        auto repository = new Core::DrugModelRepository();
        for (const std::string& path : _folders)
        {
            repository->addFolderPath(path);
        }

        drugModelRepository = repository;
    }

    // auto queryData = std::make_unique<Query::QueryData>(std::move(_queryData));
    std::unique_ptr<Query::QueryData> queryData;
    queryData.reset(&_queryData);

    auto computingQuery = std::make_unique<Query::ComputingQuery>(queryData->getQueryID());
    std::vector<std::unique_ptr<Core::DrugTreatment>> drugTreatments;

    Query::QueryStatus queryStatus = createComputingQuery(drugModelRepository, *queryData, *computingQuery, drugTreatments, computingQueryResponse);

    if (queryStatus == Query::QueryStatus::Ok)
    {
        WrapComputer().compute(*computingQuery, computingQueryResponse);
    }
    return computingQueryResponse;
}

Query::ComputingQueryResponse compute_tqf2object(const std::string _queryString, const std::vector<std::string> _folders)
{
    Query::ComputingQueryResponse computingQueryResponse;

    if (drugModelRepository == nullptr)
    {
        auto repository = new Core::DrugModelRepository();
        for (const std::string& path : _folders)
        {
            repository->addFolderPath(path);
        }

        drugModelRepository = repository;
    }

    // generate the query
    std::unique_ptr<Query::QueryData> queryData = nullptr;
    Query::QueryImport importer;

    Query::QueryImport::Status importResult = importer.importFromString(queryData, _queryString);

    if (importResult == Query::QueryImport::Status::Ok)
    {
        auto computingQuery = std::make_unique<Query::ComputingQuery>(queryData->getQueryID());
        std::vector<std::unique_ptr<Core::DrugTreatment>> drugTreatments;

        Query::QueryStatus queryStatus = createComputingQuery(drugModelRepository, *queryData, *computingQuery, drugTreatments, computingQueryResponse);

        if (queryStatus == Query::QueryStatus::Ok)
        {
            WrapComputer().compute(*computingQuery, computingQueryResponse);
        }
    }

    return computingQueryResponse;
}

 std::string compute_tqf(const std::string &_queryString, const std::vector<std::string> _folders)
{
    Query::ComputingQueryResponse computingQueryResponse;

    if (drugModelRepository == nullptr)
    {
        auto repository = new Core::DrugModelRepository();
        for (const std::string& path : _folders)
        {
            repository->addFolderPath(path);
        }

        drugModelRepository = repository;
    }

    // generate the query
    std::unique_ptr<Query::QueryData> queryData = nullptr;
    Query::QueryImport importer;

    Query::QueryImport::Status importResult = importer.importFromString(queryData, _queryString);

    if (importResult == Query::QueryImport::Status::Ok)
    {
        auto computingQuery = std::make_unique<Query::ComputingQuery>(queryData->getQueryID());
        std::vector<std::unique_ptr<Core::DrugTreatment>> drugTreatments;

        Query::QueryStatus queryStatus = createComputingQuery(drugModelRepository, *queryData, *computingQuery, drugTreatments, computingQueryResponse);

        if (queryStatus == Query::QueryStatus::Ok)
        {
            WrapComputer().compute(*computingQuery, computingQueryResponse);
        }
    }
    
    // Export query result as string
    Query::ComputingQueryResponseXmlExport _xmlExporter;
    std::string _queryResponse;
    
    _xmlExporter.exportToString(computingQueryResponse, _queryResponse);

    return _queryResponse;
}

namespace py = pybind11;

PYBIND11_MODULE(MODULE_NAME, handle) {
        handle.doc() = R"pbdoc(
            Tucuxi-core python wrapper
            --------------------------

            .. currentmodule:: sotalya.tucuxi_core.tucucore
            
            Functions
            *********
            
            .. autosummary::
              :toctree: _generate
              
              compute_query_data
              create_request_data
              compute_objects
              compute_tqf2object
              compute_tqf
              str
            
            Classes
            *******
            
            .. autosummary::
              :toctree: _generate
              
              AbsorptionModel
              ActiveMoietyId
              AdjustmentData
              AdministrationRoute
              AnalyteId
              BestCandidatesOption
              CompartmentInfo
              CompartmentType
              CompartmentsOption
              ComputedData
              ComputingOption
              ComputingQueryResponse
              ComputingResponse
              ComputingResponseMetaData
              ComputingStatus
              ComputingTrait
              ComputingTraitAdjustment
              ComputingTraitAtMeasures
              ComputingTraitConcentration
              ComputingTraitPercentiles
              ComputingTraitSinglePoints
              ComputingTraitStandard
              ConcentrationData
              CovariateValue
              CycleData
              DailyDose
              DataType
              DateTime
              Dosage
              DosageAdjustment
              DosageBounded
              DosageHistory
              DosageLoop
              DosageRepeat
              DosageSequence
              DosageSteadyState
              DosageTimeRange
              DosageUnbounded
              Duration
              ForceUgPerLiterOption
              Formulation
              FormulationAndRoute
              FormulationAndRouteSelectionOption
              FullSample
              LastingDose
              LoadingOption
              ParallelDosageSequence
              ParameterValue
              PatientCovariate
              PercentilesData
              PredictionParameterType
              QueryStatus
              RestPeriodOption
              RetrieveCovariatesOption
              RetrieveParametersOption
              RetrieveStatisticsOption
              SingleDose
              SinglePointsData
              SinglePredictionData
              SingleResponseData
              SteadyStateTargetOption
              Target
              TargetEvaluationResult
              TargetExtractionOption
              TargetType
              TimeOfDay
              TucuUnit
              WeeklyDose
        )pbdoc";

        // ===== COMMON ====== //

        // Class DateTime is returned, need to define the methods we want to use
        // Constructor is _date, _format with std::get_time used internally
        py::class_<Common::DateTime>(handle, "DateTime", R"pbdoc(
                  The DateTime class.
                  
                  A class to manage a date and a time. This allows intializing a DateTime object this way: DateTime(\"2018-10-08\", \"%Y-%m-%d\"))pbdoc")
                .def(py::init<std::string, std::string>(), R"pbdoc(
                  *date:*    The string to be parsed.
                  
                  *format:*  The parsing format.)pbdoc", 
                  py::arg("date"), 
                  py::arg("format"));

        handle.def("str", &Common::DateTime::str);

        // Class TucuUnit is a supertype around string, we can use the string return
        py::class_<Common::TucuUnit>(handle, "TucuUnit", R"pbdoc(
                  The TucuUnit class.
                      
                  This class is used to represent any unit used by a quantity.  It is very flexible in the sense that any string can be used to \
                  represent a unit. However, converting a unit to another one requires the use of standard known units.)pbdoc")
                .def(py::init<std::string>(), R"pbdoc(
                  unit_string: The string representing the unit.)pbdoc", 
                  py::arg("unit_string"))
                .def_property_readonly("value", &Common::TucuUnit::toString, R"pbdoc(
                  The string corresponding to the unit)pbdoc");

        py::class_<Common::Duration>(handle, "Duration", R"pbdoc(
                  The Duration class.
                   
                  A class to handle a duration. The class is based on the std::chrono::duration<double> type representing a number of seconds.)pbdoc")
                .def(py::init<std::chrono::seconds>(), R"pbdoc(
                  value: Duration in seconds.)pbdoc", 
                  py::arg("value"));

        // ===== ENUMS ===== //

        // Transparent binding of the ComputingStatus Enum Class
        py::enum_<Core::ComputingStatus>(handle, "ComputingStatus", R"pbdoc(
                  Transparent binding of the ComputingStatus Enum Class)pbdoc")
                .value("undefined", Core::ComputingStatus::Undefined)
                .value("ok", Core::ComputingStatus::Ok)
                .value("too_big", Core::ComputingStatus::TooBig)
                .value("aborted", Core::ComputingStatus::Aborted)
                .value("parameter_extraction_error", Core::ComputingStatus::ParameterExtractionError)
                .value("sample_extraction_error", Core::ComputingStatus::SampleExtractionError)
                .value("target_extraction_error", Core::ComputingStatus::TargetExtractionError)
                .value("invalid_candidate", Core::ComputingStatus::InvalidCandidate)
                .value("target_evaluation_error", Core::ComputingStatus::TargetEvaluationError)
                .value("covariate_extraction_error", Core::ComputingStatus::CovariateExtractionError)
                .value("intake_extraction_error", Core::ComputingStatus::IntakeExtractionError)
                .value("error_model_extraction_error", Core::ComputingStatus::ErrorModelExtractionError)
                .value("unsupported_route", Core::ComputingStatus::UnsupportedRoute)
                .value("analyte_conversion_error", Core::ComputingStatus::AnalyteConversionError)
                .value("aposteriori_percentiles_no_samples_error",
                       Core::ComputingStatus::AposterioriPercentilesNoSamplesError)
                .value("concentration_calculator_no_parameters",
                       Core::ComputingStatus::ConcentrationCalculatorNoParameters)
                .value("bad_parameters", Core::ComputingStatus::BadParameters)
                .value("bad_concentration", Core::ComputingStatus::BadConcentration)
                .value("density_error", Core::ComputingStatus::DensityError)
                .value("aposteriori_etas_calculation_empty_omega",
                       Core::ComputingStatus::AposterioriEtasCalculationEmptyOmega)
                .value("aposteriori_etas_calculation_no_square_omega",
                       Core::ComputingStatus::AposterioriEtasCalculationNoSquareOmega)
                .value("computing_trait_standard_should_not_be_called",
                       Core::ComputingStatus::ComputingTraitStandardShouldNotBeCalled)
                .value("could_not_find_suitable_formulation_and_route",
                       Core::ComputingStatus::CouldNotFindSuitableFormulationAndRoute)
                .value("multiple_formulation_and_routes_not_supported",
                       Core::ComputingStatus::MultipleFormulationAndRoutesNotSupported)
                .value("no_pk_model_error", Core::ComputingStatus::NoPkModelError)
                .value("computing_component_exception_error", Core::ComputingStatus::ComputingComponentExceptionError)
                .value("no_pk_models", Core::ComputingStatus::NoPkModels)
                .value("no_computing_traits", Core::ComputingStatus::NoComputingTraits)
                .value("recorded_intakes_size_error", Core::ComputingStatus::RecordedIntakesSizeError)
                .value("no_percentiles_calculation", Core::ComputingStatus::NoPercentilesCalculation)
                .value("selected_intakes_size_error", Core::ComputingStatus::SelectedIntakesSizeError)
                .value("no_available_dose", Core::ComputingStatus::NoAvailableDose)
                .value("no_available_interval", Core::ComputingStatus::NoAvailableInterval)
                .value("no_available_infusion_time", Core::ComputingStatus::NoAvailableInfusionTime)
                .value("no_formulation_and_route_for_adjustment", Core::ComputingStatus::NoFormulationAndRouteForAdjustment)
                .value("concentration_size_error", Core::ComputingStatus::ConcentrationSizeError)
                .value("active_moiety_calculation_error", Core::ComputingStatus::ActiveMoietyCalculationError)
                .value("no_analytes_group", Core::ComputingStatus::NoAnalytesGroup)
                .value("incompatible_treatment_model", Core::ComputingStatus::IncompatibleTreatmentModel)
                .value("computing_component_not_initialized", Core::ComputingStatus::ComputingComponentNotInitialized)
                .value("uncompatible_drug_domain", Core::ComputingStatus::UncompatibleDrugDomain)
                .value("no_steady_state", Core::ComputingStatus::NoSteadyState)
                .value("aposteriori_percentiles_out_of_scope_samples_error",
                       Core::ComputingStatus::AposterioriPercentilesOutOfScopeSamplesError)
                .value("adjustments_internal_error", Core::ComputingStatus::AdjustmentsInternalError)
                .value("multi_computing_component_exception_error",
                       Core::ComputingStatus::MultiComputingComponentExceptionError)
                .value("multi_computing_component_not_initialized",
                       Core::ComputingStatus::MultiComputingComponentNotInitialized)
                .value("multi_active_moiety_calculation_error", Core::ComputingStatus::MultiActiveMoietyCalculationError)
                .export_values();


        // ===== Everything related to the response ====== //

        // === Everything related to ComputedData and/or Concentration Data === //
        // Worth reading : https://pybind11.readthedocs.io/en/stable/classes.html#inheritance-and-automatic-downcasting

        //TODO -> Check definition
        py::class_<Core::ParameterValue>(handle, "ParameterValue", R"pbdoc(
                  Transparent binding of the ParameterValue Struct)pbdoc")
                .def_readwrite("id", &Core::ParameterValue::m_parameterId)
                .def_readwrite("val", &Core::ParameterValue::m_value);

        py::class_<Core::CovariateValue>(handle, "CovariateValue", R"pbdoc(
                  Transparent binding of the CovariateValue Struct)pbdoc")
                .def_readwrite("id", &Core::CovariateValue::m_covariateId)
                .def_readwrite("val", &Core::CovariateValue::m_value);

        py::class_<Core::CycleData>(handle, "CycleData", R"pbdoc(
                  The CycleData class, meant to embed data about a cycle.
                  
                  It contains concentrations and times for a single cycle (or interval). \
                  Actually it does contains concentrations of one or more compartments, allowing to store analytes and active moieties. The \
                  identification of the analytes and active moieties is not internally stored by the CycleData, it is the responsibility of \
                  the user to know what concentration stands each analyte or active moiety.)pbdoc")
                .def_readwrite("start", &Core::CycleData::m_start, R"pbdoc(Absolute start time of the cycle)pbdoc")
                .def_readwrite("end", &Core::CycleData::m_end, R"pbdoc(Absolute end time of the cycle)pbdoc")
                .def_readwrite("times", &Core::CycleData::m_times, R"pbdoc(A serie of times expressed as offsets in hours to the start of a cycle)pbdoc")
                .def_readwrite("concentrations", &Core::CycleData::m_concentrations, R"pbdoc(A vector of vector of concentrations. Each inner vector contains the  \
                                                                                      concentrations of an analyte or a compartment. The size of each inner  \
                                                                                      vector has to be the same as m_times.)pbdoc")
                .def_readwrite("unit", &Core::CycleData::m_unit, R"pbdoc(Unit of concentrations. The area under curve corresponds to this unit times hours)pbdoc")
                .def_readwrite("parameters", &Core::CycleData::m_parameters, R"pbdoc(Pk parameter values for this cycle. Can be used or not to store the values of the  \
                                                                              Pk parameters used for this cycle)pbdoc")
                .def_readwrite("covariates", &Core::CycleData::m_covariates, R"pbdoc(Covariates values for this cycle. Can be used or not to store the values of the  \
                                                                              covariates used for this cycle)pbdoc")
                .def_readwrite("statistics", &Core::CycleData::m_statistics, R"pbdoc(The statistics about the cycle data. For each compartment or analyte, the statistics.)pbdoc");

        // Base class "ComputedData"
        py::class_<Core::ComputedData>(handle, "ComputedData", R"pbdoc(
                  The ComputedData class.
                  
                  This class is the base class for every response. It contains all the computed data)pbdoc")
                .def_property_readonly("id", &Core::ComputedData::getId);

        
        py::class_<Core::ConcentrationData>(handle, "ConcentrationData", R"pbdoc(
                  The ConcentrationData class.
                  
                  TODO -> Expand description)pbdoc")
                .def_property_readonly("cycle_data", &Core::ConcentrationData::getModifiableData)
                .def_property_readonly("compartment_info", &Core::ConcentrationData::getCompartmentInfos);

        // Class "SinglePointData" extends "ComputedData"
        py::class_<Core::SinglePointsData, Core::ComputedData>(handle, "SinglePointsData", R"pbdoc(
                  The SinglePointsResponse class.
                  
                  This class contains data generated by a ComputingTraitSinglePoints, that is when \
                  values at specific times are asked by a request. It is also the response for ComputingTraitAtMeasures, that \
                  calculates points at the measure times found in the DrugTreatment. Therefore it offers the absolute times corresponding \
                  to the request as well as the calculated concentrations at these points.)pbdoc")
                .def_readwrite("concentrations", &Core::SinglePointsData::m_concentrations) // vector made of vectors of concentrations = value = double
                .def_readwrite("times", &Core::SinglePointsData::m_times)
                .def_readwrite("unit", &Core::SinglePointsData::m_unit);

        // Class "PercentilesData" extends "ComputedData"
        py::class_<Core::PercentilesData, Core::ComputedData>(handle, "PercentilesData", R"pbdoc(
                  The PercentilesResponse class.
                  
                  It shall contain different percentiles, for a certain period of time. \
                  In order to embed all data necessary for correct exploitation, it contains:
                  1. The percentile ranks as a vector of doubles, each one being in [0.0,100.0]
                  2. The concentration of percentiles, as a vector of CycleMultiData, one CycleData per percentile.)pbdoc")
                .def("cycle_data", &Core::PercentilesData::getPercentileData)
                .def_property_readonly("percentile_ranks", &Core::PercentilesData::getRanks)
                .def_property_readonly("nbr_points_per_hour", &Core::PercentilesData::getNbPointsPerHour);

        py::class_<Core::SinglePredictionData, Core::ComputedData, Core::ConcentrationData>(handle, "SinglePredictionData", R"pbdoc(
                  The SinglePredictionResponse class.
                  
                  It contains data of a single prediction, as a vector of CycleData.)pbdoc");

        py::class_<Core::DosageAdjustment, Core::ConcentrationData>(handle, "DosageAdjustment", R"pbdoc(
                  The DosageAdjustment class.
                  
                  This class embeds all information about a potential dosage adjustment: The dosage history, \
                  the score (suitability of the dosage), and concentrations if the concentrations have been calculated.)pbdoc")
                .def_property_readonly("get_score", &Core::DosageAdjustment::getGlobalScore)
                .def_property_readonly("dosage_history",
                    [](const Core::DosageAdjustment &dosage) { return dosage.getDosageHistory(); },
                     py::return_value_policy::reference_internal)
                .def_property_readonly("target_evaluation_results",
                    [](const Core::DosageAdjustment &dosage) { return dosage.m_targetsEvaluation; },
                    py::return_value_policy::reference_internal);

        py::class_<Core::AdjustmentData, Core::SinglePredictionData>(handle, "AdjustmentData", R"pbdoc(
                  The AdjustmentData class.
                  
                  This class embeds a vector of potential adjustments.)pbdoc")
                .def_property_readonly("dosage_adjustements", &Core::AdjustmentData::getAdjustments);

        py::class_<Core::TargetEvaluationResult>(handle, "TargetEvaluationResult", R"pbdoc(
                  The TargetEvaluationResult class.
                  
                  This class is meant to embed information about the evaluation of a specific target. \
                  It is composed of the type of target, the calculated value, and the score.)pbdoc")
                .def_property_readonly("target_type", &Core::TargetEvaluationResult::getTargetType)
                .def_property_readonly("score", &Core::TargetEvaluationResult::getScore)
                .def_property_readonly("value", &Core::TargetEvaluationResult::getValue)
                .def_property_readonly("unit", &Core::TargetEvaluationResult::getUnit);

        // === End of ComputedData === //

        // Enum QueryStatus
        py::enum_<Query::QueryStatus>(handle, "QueryStatus", R"pbdoc(
                  Transparent binding of the QueryStatus Enum Class)pbdoc")
                .value("ok", Query::QueryStatus::Ok)
                .value("partially_ok", Query::QueryStatus::PartiallyOk)
                .value("error", Query::QueryStatus::Error)
                .value("import_error", Query::QueryStatus::ImportError)
                .value("bad_format", Query::QueryStatus::BadFormat)
                .value("undefined", Query::QueryStatus::Undefined)
                .export_values();

        // Class "ComputingResponse"
        py::class_<Core::ComputingResponse>(handle, "ComputingResponse", R"pbdoc(
                  The ComputingResponse class.
                  
                  It is the response to a ComputingRequest object. It has an identifier and a vector of SingleComputingResponse, \
                  and as such can embed various responses, like a prediction, various percentiles, and a dosage adjustment.)pbdoc")
                .def_property_readonly("id", &Core::ComputingResponse::getId)                                    // RequestResponseId = string
                .def_property_readonly("data", &Core::ComputingResponse::getData)                                // ComputedData
                .def_property_readonly("computing_time", &Core::ComputingResponse::getComputingTimeInSeconds)    // duration -> https://pybind11.readthedocs.io/en/stable/advanced/cast/chrono.html
                .def_property_readonly("computing_status", &Core::ComputingResponse::getComputingStatus);        // enum ComputingStatus

        // Class "ComputingResponseMetaData"
        py::class_<Query::ComputingResponseMetaData>(handle, "ComputingResponseMetaData", R"pbdoc(
                  The ComputingResponseMetaData class.
                  
                  This class will embed information such as the drug model ID used for computation, and the computation time, for a single ComputingRequest.)pbdoc")
                .def_property_readonly("drug_model_id", &Query::ComputingResponseMetaData::getDrugModelId);

        // Class "SingleResponseData"
        py::class_<Query::SingleResponseData>(handle, "SingleResponseData", R"pbdoc(
                  The SingleResponseData class.
                  
                  TODO -> Expand description)pbdoc")
                .def_property_readonly("computing_response",
                                       [](const Query::SingleResponseData &query) { return query.m_computingResponse.get(); },
                                       py::return_value_policy::reference_internal)
                .def_property_readonly("metadata",
                                       [](const Query::SingleResponseData &query) { return query.m_metaData.get(); },
                                       py::return_value_policy::reference_internal);


        py::class_<Query::ComputingQueryResponse>(handle, "ComputingQueryResponse", R"pbdoc(
                  The ComputingQueryResponse class.
                  
                  This class contains all the responses of a ComputingQuery. It can take advantage of ComputingResponse class, but should also embed information about the drug model Id used (for instance))pbdoc")
                .def_readonly("query_id", &Query::ComputingQueryResponse::m_queryId)               // RequestResponseId = string
                .def_readonly("query_status", &Query::ComputingQueryResponse::m_queryStatus)       // enum QueryStatus
                .def_readonly("error_message", &Query::ComputingQueryResponse::m_errorMessage)     // string
                .def_readonly("responses", &Query::ComputingQueryResponse::m_requestResponses);     // vector of "SingleResponseData"
                /* .def_property_readonly("metadata", !!! EMPTY !!!
                                       [](const Query::ComputingQueryResponse &query) { return query.m_metaData.get(); },
                                       py::return_value_policy::reference_internal); */

        // ===== Now everything related to the QueryData object ===== //

        // To build a QueryData you need strings and a datetime
        // Then behind unique_ptr there is a vector of RequestData and one DrugTreatmentData

        // A DrugTreatmentData is composed of a vector of DrugData and a PatientData object
        // PatientData is simply made of a vector of PatientCovariate
        // DrugData objects need vectors of Samples, Targets and a Treatment
        // Treatment is basically made of DosageHistory objects
        // So we need to be able to create/define PatientCovariate, DosageHistory, Samples and Targets from Core
        // Dosage history is a vector of DosageTimeRange, which contains a Dosage (abstract class)
        // So we need to define all the dosage variants that must be supported from the abstract class
        // (
        // And first we define some necessary subtypes (AnalyteId, ActiveMoietyId, TargetType, DosageTimeRange)
        // Some subtypes are ready from earlier (TucuUnit, DateTime)
        // TODO -> Add parameter definition
        py::class_<Core::AnalyteId>(handle, "AnalyteId", R"pbdoc(
                  The AnalyteId class.
                  
                  This class is simply a std::string. The rationale is that it makes it mandatory to use AnalyteId wherever needed, and as such not to mix things with AnalyteGroupId.)pbdoc")
                .def(py::init<const std::string &>(), R"pbdoc(
                      analyte_id: )pbdoc", 
                      py::arg("analyte_id"));
                      
        // TODO -> Add parameter definition
        py::class_<Core::ActiveMoietyId>(handle, "ActiveMoietyId", R"pbdoc(
                  The ActiveMoietyId class.
                  
                  This class is simply a std::string. The rationale is that it makes it mandatory to use ActiveMoietyId wherever needed, and as such not to mix things with AnalyteGroupId or AnalyteId.)pbdoc")
                .def(py::init<const std::string &>(), R"pbdoc(
                      active_moiety_id: )pbdoc", 
                      py::arg("active_moiety_id"));

        py::enum_<Core::TargetType>(handle, "TargetType", R"pbdoc(
                  Transparent binding of the TargetType Enum Class)pbdoc")
                .value("auc", Core::TargetType::Auc)
                .value("auc24", Core::TargetType::Auc24)
                .value("auc24_divided_by_mic", Core::TargetType::Auc24DividedByMic)
                .value("auc24_over_mic", Core::TargetType::Auc24OverMic)
                .value("auc_divided_by_mic", Core::TargetType::AucDividedByMic)
                .value("auc_over_mic", Core::TargetType::AucOverMic)
                .value("cumulative_auc", Core::TargetType::CumulativeAuc)
                .value("mean", Core::TargetType::Mean)
                .value("peak", Core::TargetType::Peak)
                .value("peak_divided_by_mic", Core::TargetType::PeakDividedByMic)
                .value("residual", Core::TargetType::Residual)
                .value("residual_divided_by_mic", Core::TargetType::ResidualDividedByMic)
                .value("time_over_mic", Core::TargetType::TimeOverMic)
                .value("unknown_target", Core::TargetType::UnknownTarget)
                .export_values();

        py::enum_<Core::DataType>(handle, "DataType", R"pbdoc(
                  Transparent binding of the DataType Enum Class)pbdoc")
                .value("int", Core::DataType::Int)
                .value("double", Core::DataType::Double)
                .value("bool", Core::DataType::Bool)
                .value("date", Core::DataType::Date)
                .export_values();

        py::enum_<Core::AbsorptionModel>(handle, "AbsorptionModel", R"pbdoc(
                  Transparent binding of the AbsorptionModel Enum Class)pbdoc")
                .value("undefined", Core::AbsorptionModel::Undefined)
                .value("intravascular", Core::AbsorptionModel::Intravascular)
                .value("extravascular", Core::AbsorptionModel::Extravascular)
                .value("infusion", Core::AbsorptionModel::Infusion)
                .value("extravascular_lag", Core::AbsorptionModel::ExtravascularLag)
                .export_values();

        py::enum_<Core::Formulation>(handle, "Formulation", R"pbdoc(
                  Transparent binding of the Formulation Enum Class)pbdoc")
                .value("undefined", Core::Formulation::Undefined)
                .value("parenteral_solution", Core::Formulation::ParenteralSolution)
                .value("oral_solution", Core::Formulation::OralSolution)
                .value("test", Core::Formulation::Test)
                .export_values();

        py::enum_<Core::AdministrationRoute>(handle, "AdministrationRoute", R"pbdoc(
                  Transparent binding of the AdministrationRoute Enum Class)pbdoc")
                .value("undefined", Core::AdministrationRoute::Undefined)
                .value("intramuscular", Core::AdministrationRoute::Intramuscular)
                .value("intravenous_bolus", Core::AdministrationRoute::IntravenousBolus)
                .value("intravenous_drip", Core::AdministrationRoute::IntravenousDrip)
                .value("nasal", Core::AdministrationRoute::Nasal)
                .value("oral", Core::AdministrationRoute::Oral)
                .value("rectal", Core::AdministrationRoute::Rectal)
                .value("subcutaneous", Core::AdministrationRoute::Subcutaneous)
                .value("sublingual", Core::AdministrationRoute::Sublingual)
                .value("transdermal", Core::AdministrationRoute::Transdermal)
                .value("vaginal", Core::AdministrationRoute::Vaginal)
                .export_values();
        
        // TODO -> Add parameter description and class description
        py::class_<Core::FormulationAndRoute>(handle, "FormulationAndRoute", R"pbdoc(
                  TODO -> Description)pbdoc")
                .def(py::init<Core::Formulation, Core::AdministrationRoute, Core::AbsorptionModel, std::string>(), R"pbdoc(
                      formulation:
                      route:
                      absorption_model:
                      administration_name: )pbdoc", 
                      py::arg("formulation"), 
                      py::arg("route"), 
                      py::arg("absorption_model"), 
                      py::arg("administration_name"));

        py::class_<Common::TimeOfDay>(handle, "TimeOfDay", R"pbdoc(
                  The TimeOfDay class.
                  
                  A class to manage the time within a day.)pbdoc")
                .def(py::init<std::chrono::seconds &>(), R"pbdoc(
                      time: Duration in seconds.)pbdoc", 
                      py::arg("time"));

        // Everything regarde abstract class Dosage

        py::class_<Core::Dosage>(handle, "Dosage", R"pbdoc(
                  The Dosage class.
                  
                  Abstract class at the base of the dosage class hierarchy. Dosages are implemented as either bounded or unbounded dosages.)pbdoc");

        py::class_<Core::DosageUnbounded, Core::Dosage>(handle, "DosageUnbounded", R"pbdoc(
                  The DosageUnbounded class.
                  
                  Pure virtual class upon which dosage loops are based.)pbdoc");

        py::class_<Core::DosageBounded, Core::Dosage>(handle, "DosageBounded", R"pbdoc(
                  The DosageBounded class.
                  
                  Pure virtual class upon which all implemented dosages are based.)pbdoc");

        py::class_<Core::DosageLoop, Core::DosageUnbounded>(handle, "DosageLoop", R"pbdoc(
                  The DosageLoop class.
                  
                  List of bounded dosages that are repeated in time. The bounds are imposed by the time range embedding the dosage loop. This class  \
                  is created to ensure that no unbounded history is part of another dosage loop (creating an infinite loop).)pbdoc")
                .def(py::init<Core::DosageBounded &>(), R"pbdoc(
                      Construct a dosage loop from a bounded dosage.
                      
                      dosage: Dosage to add to the loop.)pbdoc", 
                      py::arg("dosage"))
                .def(py::init<Core::DosageLoop &>(), R"pbdoc(
                      Copy-construct a dosage loop.
                      
                      dosage_loop: Dosage loop to clone.)pbdoc", 
                      py::arg("dosage_loop"))
                .def_property_readonly("get_dosage", &Core::DosageLoop::getDosage);

        // TODO -> Check description
        py::class_<Core::DosageSteadyState, Core::DosageLoop>(handle, "DosageSteadyState", R"pbdoc(
                  The DosageSteadyState class.
                  
                  A single dosage at steady state. In addition to the dose, this object stores the time of the last dose. While it could be considered  \
                  to be purely the last one, actually any dose is OK. So, there is no real restriction on what dose to choose. The time range pointing to  \
                  a steady state dosage does not need to have a start and an end time. It can, however, have an end time, in case it is followed by another  \
                  dosage. Therefore, a DosageSteadyState needs to be the first dosage in a DosageHistory, but can be followed by other dosages.)pbdoc")
                .def(py::init<Core::DosageBounded &, Common::DateTime>(), R"pbdoc(
                      Construct a dosage loop from a bounded dosage.
                      
                      dosage:          Dosage to add to the loop.
                      last_dose_time:  Time of the last dosage.)pbdoc", 
                      py::arg("dosage"),
                      py::arg("last_dose_time"))
                .def(py::init<Core::DosageSteadyState &>(), R"pbdoc(
                      Copy-construct a dosage loop.
                      
                      dosage_stady_state: Dosage Steady State to clone.)pbdoc", 
                      py::arg("dosage_stady_state"))
                .def_property_readonly("last_dose_time", &Core::DosageSteadyState::getLastDoseTime);

        // Basically takes a dosage (bounded) and the number of time it has to be repeated
        // _dosage, _nbTimes
        py::class_<Core::DosageRepeat, Core::DosageBounded>(handle, "DosageRepeat", R"pbdoc(
                  The DosageRepeat class.
                  
                  Dosage that is administered a given number of times.)pbdoc")
                .def(py::init<Core::DosageBounded &, unsigned int>(), R"pbdoc(
                      Construct a repeated dosage starting from a dosage and the number of times it is repeated.
                      
                      dosage:        Dosage to repeat.
                      nbr_of_times:  Number of times the dosage has to be repeated.)pbdoc", 
                      py::arg("dosage"),
                      py::arg("nbr_of_times"))
                .def(py::init<Core::DosageRepeat &>(), R"pbdoc(
                      Copy-construct a dosage repetition.
                      dosage_repeat: Dosage Repeat to clone.)pbdoc", 
                      py::arg("dosage_repeat"))
                .def_property_readonly("nbr_times", &Core::DosageRepeat::getNbTimes)
                .def_property_readonly("dosage", &Core::DosageRepeat::getDosage);

        // This class allows to have multiple dosage (bounded) without specific restrictions
        // For example, a sequence of three daily doses on different days
        // It's created with the first of them _dosage, then we need to call the add method
        py::class_<Core::DosageSequence, Core::DosageBounded>(handle, "DosageSequence", R"pbdoc(
                  The DosageSequence class.
                  
                  Unordered sequence of dosages that is administered in a bounded interval. This class can be used, for instance, to represent a sequence  \
                  of three daily doses in three different days.)pbdoc")
                .def(py::init<Core::DosageBounded &>(), R"pbdoc(
                      Create a dosage sequence taking at least a dosage (this prevents having an empty sequence)
                      
                      dosage: Dosage to add.)pbdoc", 
                      py::arg("dosage"))
                .def(py::init<Core::DosageSequence &>(), R"pbdoc(
                      Copy-construct a dosage sequence.
                      
                      dosage_sequence: Dosage Sequence to clone.)pbdoc", 
                      py::arg("dosage_sequence"))
                .def("add_dosage", &Core::DosageSequence::addDosage, R"pbdoc(
                      Add a dosage to the sequence.
                      
                      dosage: Dosage to add.)pbdoc", 
                      py::arg("dosage"))
                .def("get_dosage_at_index", &Core::DosageSequence::getDosageAtIndex, R"pbdoc(
                      Get the dosage at a specific index.
                      
                      index: Index of the dosage.)pbdoc", 
                      py::arg("index"))
                .def_property_readonly("get_nbr_of_dosages", &Core::DosageSequence::getNumberOfDosages);

        // Unordered sequence of dosages, with a common starting point and an absolute offset, that evolve in parallel.
        ///// This class can be used, for instance, to represent a sequence of three different doses that have to be administered
        ///// in the same day, at different moments, but with a daily periodicization (that is, at XX:XX dose A, at YY:YY dose B,
        ///// and at ZZ:ZZ dose C, and this every day).
        // It's created with the first of them _dosage, then we need to call the add method
        py::class_<Core::ParallelDosageSequence, Core::DosageBounded>(handle, "ParallelDosageSequence", R"pbdoc(
                  The ParallelDosageSequence class.
                  
                  Unordered sequence of dosages, with a common starting point and an absolute offset, that evolve in parallel. This class can be used, for  \
                  instance, to represent a sequence of three different doses that have to be administered in the same day, at different moments, but with a  \
                  daily periodicization (that is, at XX:XX dose A, at YY:YY dose B, and at ZZ:ZZ dose C, and this every day).)pbdoc")
                .def(py::init<Core::DosageBounded &, Common::Duration &>(), R"pbdoc(
                      Create a dosage sequence taking at least a dosage and an absolute offset (this prevents having an empty sequence).
                
                      dosage: Dosage to add.
                      offset: Offset of the dosage in seconds.)pbdoc", 
                      py::arg("dosage"),
                      py::arg("offset"))
                .def(py::init<Core::ParallelDosageSequence &>(), R"pbdoc(
                      Copy-construct a parallel dosage sequence.
                      
                      parallel_dosage_sequence: Parallel Dosage Sequence to clone.)pbdoc", 
                      py::arg("parallel_dosage_sequence"))
                .def("add_dosage", &Core::ParallelDosageSequence::addDosage, R"pbdoc(
                      Add a dosage to the sequence, along with its offset with respect to the beginnning of the sequence.
                      
                      dosage: Dosage to add.
                      offset: Offset of the dosage.)pbdoc", 
                      py::arg("dosage"),
                      py::arg("offset"))
                .def("get_dosage_at_index", &Core::ParallelDosageSequence::getDosageAtIndex, R"pbdoc(
                      Get the dosage at a specific index.
                      
                      index: Index of the dosage.)pbdoc", 
                      py::arg("index"))
                .def("get_offset_at_index", &Core::ParallelDosageSequence::getOffsetAtIndex, R"pbdoc(
                      Get the offset at a specific index.
                      
                      index: Index of the offset.)pbdoc",
                      py::arg("index"))
                .def_property_readonly("nbr_of_dosages", &Core::ParallelDosageSequence::getNumberOfDosages);

        // This class has a constructor but is an abstract class, so I'll not add the binding atm
        // _dose, _doseUnit, _routeOfAdministration, _infustionTime
        py::class_<Core::SingleDose, Core::DosageBounded>(handle, "SingleDose", R"pbdoc(
                  The SingleDose class.
                  
                  Abstract class specifying a specific intake.)pbdoc")
                .def_property_readonly("infusion_time", &Core::SingleDose::getInfusionTime)
                .def_property_readonly("dose", &Core::SingleDose::getDose)
                .def_property_readonly("dose_unit", &Core::SingleDose::getDoseUnit)
                .def_property_readonly("last_formulation_and_route", &Core::SingleDose::getLastFormulationAndRoute);
                // .def(py::init<Core::DoseValue &, Common::TucuUnit &, Core::FormulationAndRoute &, Common::Duration &>());

        py::class_<Core::LastingDose, Core::SingleDose>(handle, "LastingDose", R"pbdoc(
                  The LastingDose class.
                  
                  Dose supposed to last for a certain, specified time interval. When used in a DosageLoop, a LastingDose object allows to represent a dosage history with fixed intervals.)pbdoc")
                .def(py::init<double, Common::TucuUnit &, Core::FormulationAndRoute &, Common::Duration &, Common::Duration &>(), R"pbdoc(
                      dose:          Quantity of drug administered.
                      dose_unit:     Unit of the dose.
                      route:         Route of administration.
                      infusion_time: Duration in case of an infusion.
                      interval:      Interval between two doses.)pbdoc", 
                      py::arg("dose"), 
                      py::arg("dose_unit"), 
                      py::arg("route"), 
                      py::arg("infusion_time"), 
                      py::arg("interval"))
                .def_property_readonly("time_step", &Core::LastingDose::getTimeStep, R"pbdoc(
                      Interval between two doses.)pbdoc");

        // _dose, _doseUnit, _routeOfAdministration, _infusionTime, _timeOfDay
        py::class_<Core::DailyDose, Core::SingleDose>(handle, "DailyDose", R"pbdoc(
                  The DailyDose class.
                  
                  Dose taken every day at the same time.)pbdoc")
                .def(py::init<double, Common::TucuUnit &, Core::FormulationAndRoute &, Common::Duration &, Common::TimeOfDay &>(), R"pbdoc(
                      dose:          Quantity of drug administered.
                      dose_unit:     Unit of the dose.
                      route:         Route of administration.
                      infusion_time: Duration in case of an infusion.
                      time_of_day:   Time of the day when the dose is administered.)pbdoc", 
                      py::arg("dose"), 
                      py::arg("dose_unit"), 
                      py::arg("route"), 
                      py::arg("infusion_time"), 
                      py::arg("time_of_day"))
                .def_property_readonly("time_of_day", &Core::DailyDose::getTimeOfDay);

        // _dose, _doseUnit, _routeOfAdministration, _infusionTime, _timeOfDay, _dayOfWeek (=date::weekday)
        py::class_<Core::WeeklyDose, Core::DailyDose>(handle, "WeeklyDose", R"pbdoc(
                  The WeeklyDose class.
                  
                  Dose taken every week on a specific day of the week.)pbdoc")
                .def(py::init<double, Common::TucuUnit &, Core::FormulationAndRoute &, Common::Duration &, Common::TimeOfDay &, date::weekday &>(), R"pbdoc(
                      dose:          Quantity of drug administered.
                      dose_unit:     Unit of the dose.
                      route:         Route of administration.
                      infusion_time: Duration in case of an infusion.
                      time_of_day:   Time of the day when the dose is administered.
                      day_of_week:   Day of the week the dose has to be administered.)pbdoc", 
                      py::arg("dose"), 
                      py::arg("dose_unit"), 
                      py::arg("route"), 
                      py::arg("infusion_time"), 
                      py::arg("time_of_day"), 
                      py::arg("day_of_week"))
                .def_property_readonly("day_of_week", &Core::WeeklyDose::getDayOfWeek);



        // And now the 4 classes we wanted

        //
        py::class_<Query::FullSample>(handle, "FullSample", R"pbdoc(
                  The FullSample class.
                  
                  Subclass of Sample that is more administration-oriented because it includes the sample identifier.)pbdoc")
                .def(py::init<std::string, Common::DateTime, Core::AnalyteId, double, Common::TucuUnit, double>(), R"pbdoc(
                      id:         Unique identifier.
                      date:       Date of measures.
                      analyte_id: ID of the measured analyte.
                      value:      Value of concentration.
                      unit:       Unit of the value.
                      weight:     The sample weight.)pbdoc", 
                      py::arg("id"),
                      py::arg("date"), 
                      py::arg("analyte_id"), 
                      py::arg("value"), 
                      py::arg("unit"),
                      py::arg("weight") = 1);


        // TODO -> Add explanations on the different parameters
        // 1. _activeMoietyId, _type, _min, _best, _max
        // 2. _activeMoietyId, _type, _min, _best, _max, _inefficacyAlarm, _toxicityAlarm
        // 3. _activeMoietyId, _type, _unit, _min, _best, _max, _inefficacyAlarm, _toxicityAlarm
        // 4. _activeMoietyId, _type, _min, _best, _max, _mic
        // 5. _activeMoietyId, _type, _unit, _vmin, _vbest, _vmax, _mic, _micUnit, _tmin, _tbest, _tmax
        // 6. _activeMoietyId, _type, _unit, _vmin, _vbest, _vmax, _inefficacyAlarm, _toxicityAlarm, _mic, _micUnit
        // 7. _activeMoietyId, _type, _unit, _vmin, _vbest, _vmax, _inefficacyAlarm, _toxicityAlarm, _mic, _micUnit, _tmin, _tbest, _tmax
        py::class_<Core::Target>(handle, "Target", R"pbdoc(
                  The Target class.
                  
                  A target defined within a DrugTreatment, it should be used to override the default DrugModel targets.)pbdoc")
                .def(py::init<Core::ActiveMoietyId, Core::TargetType, double, double, double>(), R"pbdoc(
                      active_moiety_id:
                      type:
                      min:
                      best:
                      max:)pbdoc", 
                      py::arg("active_moiety_id"), 
                      py::arg("type"), 
                      py::arg("min"), 
                      py::arg("best"),
                      py::arg("max")) // [1]
                .def(py::init<Core::ActiveMoietyId, Core::TargetType, double, double, double, double, double>(), R"pbdoc(
                      active_moiety_id:
                      type:
                      min:
                      best:
                      max:
                      inefficacy_alarm:
                      toxicity_alarm:)pbdoc", 
                      py::arg("active_moiety_id"), 
                      py::arg("type"), 
                      py::arg("min"), 
                      py::arg("best"),
                      py::arg("max"),
                      py::arg("inefficacy_alarm"),
                      py::arg("toxicity_alarm")) // [2]
                .def(py::init<Core::ActiveMoietyId, Core::TargetType, Common::TucuUnit, double, double, double, double, double>(), R"pbdoc(
                      active_moiety_id:
                      type:
                      unit:
                      min:
                      best:
                      max:
                      inefficacy_alarm:
                      toxicity_alarm:)pbdoc", 
                      py::arg("active_moiety_id"), 
                      py::arg("type"), 
                      py::arg("unit"), 
                      py::arg("min"), 
                      py::arg("best"),
                      py::arg("max"),
                      py::arg("inefficacy_alarm"),
                      py::arg("toxicity_alarm")) // [3]
                .def(py::init<Core::ActiveMoietyId, Core::TargetType, double, double, double, double>(), R"pbdoc(
                      active_moiety_id:
                      type:
                      min:
                      best:
                      max:
                      mic:)pbdoc", 
                      py::arg("active_moiety_id"), 
                      py::arg("type"), 
                      py::arg("min"), 
                      py::arg("best"),
                      py::arg("max"),
                      py::arg("mic")) // [4]
                .def(py::init<Core::ActiveMoietyId, Core::TargetType, Common::TucuUnit, double, double, double, double, Common::TucuUnit, Common::Duration, Common::Duration, Common::Duration>(), R"pbdoc(
                      active_moiety_id:
                      type:
                      unit:
                      v_min:
                      v_best:
                      v_max:
                      mic:
                      mic_unit:
                      t_min:
                      t_best:
                      t_max:)pbdoc", 
                      py::arg("active_moiety_id"), 
                      py::arg("type"), 
                      py::arg("unit"), 
                      py::arg("v_min"),
                      py::arg("v_best"),
                      py::arg("v_max"), 
                      py::arg("mic"),
                      py::arg("mic_unit"),
                      py::arg("t_min"),
                      py::arg("t_best"),
                      py::arg("t_max")) // [5]
                .def(py::init<Core::ActiveMoietyId, Core::TargetType, Common::TucuUnit, double, double, double, double, double, double, Common::TucuUnit>(), R"pbdoc(
                      active_moiety_id:
                      type:
                      unit:
                      v_min:
                      v_best:
                      v_max:
                      inefficacy_alarm:
                      toxicity_alarm:
                      mic:
                      mic_unit:)pbdoc", 
                      py::arg("active_moiety_id"), 
                      py::arg("type"), 
                      py::arg("unit"), 
                      py::arg("v_min"),
                      py::arg("v_best"),
                      py::arg("v_max"), 
                      py::arg("inefficacy_alarm"),
                      py::arg("toxicity_alarm"),
                      py::arg("mic"),
                      py::arg("mic_unit")) // [6]
                .def(py::init<Core::ActiveMoietyId, Core::TargetType, Common::TucuUnit, double, double, double, double, double, double, Common::TucuUnit, Common::Duration, Common::Duration, Common::Duration>(), R"pbdoc(
                      active_moiety_id:
                      type:
                      unit:
                      v_min:
                      v_best:
                      v_max:
                      inefficacy_alarm:
                      toxicity_alarm:
                      mic:
                      mic_unit:
                      t_min:
                      t_best:
                      t_max:)pbdoc", 
                      py::arg("active_moiety_id"), 
                      py::arg("type"), 
                      py::arg("unit"), 
                      py::arg("v_min"),
                      py::arg("v_best"),
                      py::arg("v_max"), 
                      py::arg("inefficacy_alarm"),
                      py::arg("toxicity_alarm"),
                      py::arg("mic"),
                      py::arg("mic_unit"),
                      py::arg("t_min"),
                      py::arg("t_best"),
                      py::arg("t_max")); // [7]

        // _id, _value, _dataType, _unit, _date
        py::class_<Core::PatientCovariate>(handle, "PatientCovariate", R"pbdoc(
                  The PatientCovariate class.
                  
                  Change of a covariate value for a patient. The value is saved as a string, as it can be any type (int, double, bool, Date). \
                  Specifically the Date type requires such a special way of storing it. It is then the responsibility of the user to cast and \
                  transform the covariate into something meaningfull.)pbdoc")
                .def(py::init<std::string, std::string, Core::DataType, Common::TucuUnit, Common::DateTime>(), R"pbdoc(
                      Create a change of a covariate value for a patient.
                      
                      id:        Identifier of the original covariate for which the change applies.
                      value:     Recorded value expressed in string form.
                      data_type: Type of the data stored in the value variable.
                      unit:      Unit of measure of the value.
                      date:      Time when the change happened.)pbdoc", 
                      py::arg("id"), 
                      py::arg("value"), 
                      py::arg("data_type"), 
                      py::arg("unit"),
                      py::arg("date"));

        // _startDate, _dosage
        py::class_<Core::DosageTimeRange>(handle, "DosageTimeRange", R"pbdoc(
                  The DosageTimeRange class.
                  
                  Doses administered in a given time interval (which might have no upper bound).)pbdoc")
                .def(py::init<Common::DateTime, Core::Dosage &>(), R"pbdoc(
                      Initialize an open-ended list of doses (the end date is not specified).
                      
                      start_date:  Interval's starting date.
                      dosage:      Administered dosage.)pbdoc", 
                      py::arg("start_date"), 
                      py::arg("dosage"))  // start - dosage
                .def(py::init<Common::DateTime, Common::DateTime, Core::Dosage &>(), R"pbdoc(
                      Initialize an list of doses (the end date is specified, though it could be unset).
                      
                      start_date:  Interval's starting date.
                      end_date:    Interval's ending date.
                      dosage:      Administered dosage.)pbdoc", 
                      py::arg("start_date"), 
                      py::arg("end_date"), 
                      py::arg("dosage")) // start - end - dosage
                .def_property_readonly("start_date", &Core::DosageTimeRange::getStartDate)
                .def_property_readonly("end_date", &Core::DosageTimeRange::getEndDate)
                .def_property_readonly("dosage", &Core::DosageTimeRange::getDosage);

        py::class_<Core::DosageHistory>(handle, "DosageHistory", R"pbdoc(
                  The DosageHistory class.
                  
                  Represents a dosage history. A dosage history represents every intake of a drug treatment, dealing with multiple intake scenarios.)pbdoc")
                .def("get_dosage_time_range_at_index", &Core::DosageHistory::getDosageTimeRangeAtIndex, R"pbdoc(
                      Get the DosageTimeRange at a specific index.
                      
                      index: Index of the DosageTimeRange.)pbdoc", 
                      py::arg("index"))
                .def_property_readonly("get_nbr_of_time_ranges", &Core::DosageHistory::getNumberOfTimeRanges)
                .def_property_readonly("formulation_and_route_list", &Core::DosageHistory::getFormulationAndRouteList);
                /* .def_property_readonly("dosage_time_range_list",
                [](const Core::DosageHistory &dosage) { return dosage.getDosageTimeRanges(); },
                py::return_value_policy::reference_internal); */


        // Now about RequestData
        // It contains 3 strings (easy) and a unique_pointer to a computing trait
        py::class_<Core::ComputingTrait>(handle, "ComputingTrait", R"pbdoc(
                  The ComputingTrait class.
                  
                  This is the base class for all traits. It only has an identifier.)pbdoc");

        py::enum_<Core::BestCandidatesOption>(handle, "BestCandidatesOption", R"pbdoc(
                  Transparent binding of the BestCandidatesOption Enum Class)pbdoc")
                .value("best_dosage", Core::BestCandidatesOption::BestDosage)
                .value("all_dosages", Core::BestCandidatesOption::AllDosages)
                .value("best_dosage_per_interval", Core::BestCandidatesOption::BestDosagePerInterval)
                .export_values();

        py::enum_<Core::LoadingOption>(handle, "LoadingOption", R"pbdoc(
                  Transparent binding of the LoadingOption Enum Class)pbdoc")
                .value("no_loading_dose", Core::LoadingOption::NoLoadingDose)
                .value("loading_dose_allowed", Core::LoadingOption::LoadingDoseAllowed)
                .export_values();

        py::enum_<Core::RestPeriodOption>(handle, "RestPeriodOption", R"pbdoc(
                  Transparent binding of the RestPeriodOption Enum Class)pbdoc")
                .value("no_rest_period", Core::RestPeriodOption::NoRestPeriod)
                .value("rest_period_allowed", Core::RestPeriodOption::RestPeriodAllowed)
                .export_values();

        py::enum_<Core::SteadyStateTargetOption>(handle, "SteadyStateTargetOption", R"pbdoc(
                  Transparent binding of the SteadyStateTargetOption Enum Class)pbdoc")
                .value("at_steady_state", Core::SteadyStateTargetOption::AtSteadyState)
                .value("within_treatment_time_range", Core::SteadyStateTargetOption::WithinTreatmentTimeRange)
                .export_values();

        py::enum_<Core::TargetExtractionOption>(handle, "TargetExtractionOption", R"pbdoc(
                  Transparent binding of the TargetExtractionOption Enum Class)pbdoc")
                .value("population_values", Core::TargetExtractionOption::PopulationValues)
                .value("apriori_values", Core::TargetExtractionOption::AprioriValues)
                .value("individual_targets", Core::TargetExtractionOption::IndividualTargets)
                .value("individual_targets_if_definition_exists", Core::TargetExtractionOption::IndividualTargetsIfDefinitionExists)
                .value("definition_if_no_individual_target", Core::TargetExtractionOption::DefinitionIfNoIndividualTarget)
                .value("individual_targets_if_definition_exists_and_definition_if_no_individual_target", Core::TargetExtractionOption::IndividualTargetsIfDefinitionExistsAndDefinitionIfNoIndividualTarget)
                .export_values();

        py::enum_<Core::FormulationAndRouteSelectionOption>(handle, "FormulationAndRouteSelectionOption", R"pbdoc(
                  Transparent binding of the FormulationAndRouteSelectionOption Enum Class)pbdoc")
                .value("last_formulation_and_route", Core::FormulationAndRouteSelectionOption::LastFormulationAndRoute)
                .value("default_formulation_and_route", Core::FormulationAndRouteSelectionOption::DefaultFormulationAndRoute)
                .value("all_formulation_and_routes", Core::FormulationAndRouteSelectionOption::AllFormulationAndRoutes)
                .export_values();

        py::enum_<Core::PredictionParameterType>(handle, "PredictionParameterType", R"pbdoc(
                  Transparent binding of the PredictionParameterType Enum Class)pbdoc")
                .value("population", Core::PredictionParameterType::Population)
                .value("apriori", Core::PredictionParameterType::Apriori)
                .value("aposteriori", Core::PredictionParameterType::Aposteriori)
                .export_values();

        py::enum_<Core::CompartmentsOption>(handle, "CompartmentsOption", R"pbdoc(
                  Transparent binding of the CompartmentsOption Enum Class)pbdoc")
                .value("all_active_moieties", Core::CompartmentsOption::AllActiveMoieties)
                .value("all_analytes", Core::CompartmentsOption::AllAnalytes)
                .value("all_compartments", Core::CompartmentsOption::AllCompartments)
                .value("specific", Core::CompartmentsOption::Specific)
                .value("main_compartment", Core::CompartmentsOption::MainCompartment)
                .export_values();

        py::enum_<Core::RetrieveStatisticsOption>(handle, "RetrieveStatisticsOption", R"pbdoc(
                  Transparent binding of the RetrieveStatisticsOption Enum Class)pbdoc")
                .value("retrieve_statistics", Core::RetrieveStatisticsOption::RetrieveStatistics)
                .value("do_not_retrieve_statistics", Core::RetrieveStatisticsOption::DoNotRetrieveStatistics)
                .export_values();

        py::enum_<Core::RetrieveParametersOption>(handle, "RetrieveParametersOption", R"pbdoc(
                  Transparent binding of the RetrieveParametersOption Enum Class)pbdoc")
                .value("retrieve_parameters", Core::RetrieveParametersOption::RetrieveParameters)
                .value("do_not_retrieve_parameters", Core::RetrieveParametersOption::DoNotRetrieveParameters)
                .export_values();

        py::enum_<Core::RetrieveCovariatesOption>(handle, "RetrieveCovariatesOption", R"pbdoc(
                  Transparent binding of the RetrieveCovariatesOption Enum Class)pbdoc")
                .value("retrieve_covariates", Core::RetrieveCovariatesOption::RetrieveCovariates)
                .value("do_not_retrieve_covariates", Core::RetrieveCovariatesOption::DoNotRetrieveCovariates)
                .export_values();

        py::enum_<Core::ForceUgPerLiterOption>(handle, "ForceUgPerLiterOption", R"pbdoc(
                  Transparent binding of the ForceUgPerLiterOption Enum Class)pbdoc")
                .value("force", Core::ForceUgPerLiterOption::Force)
                .value("do_not_force", Core::ForceUgPerLiterOption::DoNotForce)
                .export_values();

        py::class_<Core::ComputingOption>(handle, "ComputingOption", R"pbdoc(
                  The ComputingOption class.
                  
                  This class embeds some general options for computation. It is used by all requests. Currently it offers  \
                  choice for the type of parameters and which compartment we are interested in.)pbdoc")
                .def(py::init<Core::PredictionParameterType, Core::CompartmentsOption, Core::RetrieveStatisticsOption, Core::RetrieveParametersOption,
                              Core::RetrieveCovariatesOption, Core::ForceUgPerLiterOption>(), R"pbdoc(
                      ComputingOption Simple constructor.
                              
                      parameter_type:      Type of parameters (population, aPriori, aPosteriori).
                      compartments_option: What compartments are of interest (main or all).
                      retrieve_statistics: Indicates if statistics have to be computed.
                      retrieve_parameters: Indicates if parameter values have to be retrieved.
                      retrieve_covariates: Indicates if covariate values have to be retrieved.
                      force_ug_per_liter:  Indicates if the results should be forced in ug/l.)pbdoc", 
                      py::arg("parameter_type"), 
                      py::arg("compartments_option"), 
                      py::arg("retrieve_statistics"), 
                      py::arg("retrieve_parameters"), 
                      py::arg("retrieve_covariates"), 
                      py::arg("force_ug_per_liter"));

        py::class_<Core::ComputingTraitStandard, Core::ComputingTrait, std::unique_ptr<Core::ComputingTraitStandard, py::nodelete>>(handle, "ComputingTraitStandard", R"pbdoc(
                  The ComputingTraitStandard class.
                  
                  This is a base class for other Traits. It embeds information about:
                    1. Start date of prediction calculation
                    2. End date of prediction calculation
                    3. Number of points for the calculation.
                    4. Some processing options (type of parameters, what compartments))pbdoc")
                .def(py::init<std::string, Common::DateTime, Common::DateTime, double, Core::ComputingOption>(), R"pbdoc(
                      ComputingTraitStandard A simple constructor.
                      
                      id:                  Id of the request.
                      start:               Start date of prediction calculation.
                      end:                 End date of prediction calculation.
                      nbr_points_per_hour: Requested number of points per hour.
                      computing_option:    Some processing options (type of parameters, what compartments).)pbdoc",
                      py::arg("id"), 
                      py::arg("start"), 
                      py::arg("end"), 
                      py::arg("nbr_points_per_hour"), 
                      py::arg("computing_option"));

        py::class_<Core::ComputingTraitSinglePoints, Core::ComputingTrait, std::unique_ptr<Core::ComputingTraitSinglePoints, py::nodelete>>(handle, "ComputingTraitSinglePoints", R"pbdoc(
                  The ComputingTraitSinglePoints class.
                  
                  This class embeds the information required to compute concentrations at specific time points.)pbdoc")
                .def(py::init<std::string, std::vector<Common::DateTime>, Core::ComputingOption>(), R"pbdoc(
                      ComputingTraitSinglePoints Simple constructor.
                      
                      id:                  Id of the request.
                      times:               Start date of prediction calculation.
                      computing_option:    Some processing options (type of parameters, what compartments).)pbdoc",
                      py::arg("id"), 
                      py::arg("times"),
                      py::arg("computing_option"));

        py::class_<Core::ComputingTraitAtMeasures, Core::ComputingTrait, std::unique_ptr<Core::ComputingTraitAtMeasures, py::nodelete>>(handle, "ComputingTraitAtMeasures", R"pbdoc(
                  The ComputingTraitAtMeasures class.
                  
                  This class shall be used for computing concentrations at the times of the DrugTreatment measures. Typically used for comparing the measured concentrations with a posteriori predictions.)pbdoc")
                .def(py::init<std::string, Core::ComputingOption>(), R"pbdoc(
                      ComputingTraitAtMeasures Simple constructor.
                      
                      id:                  Id of the request.
                      computing_option:    Some processing options (type of parameters, what compartments).)pbdoc",
                      py::arg("id"), 
                      py::arg("computing_option"));

        py::class_<Core::ComputingTraitAdjustment, Core::ComputingTraitStandard, std::unique_ptr<Core::ComputingTraitAdjustment, py::nodelete>>(handle, "ComputingTraitAdjustment", R"pbdoc(
                  The ComputingTraitAdjustment class.
                  
                  This class embeds all information required for computing adjustments. It can return potential dosages, and future concentration calculations, depending on the options.
                  If nbPoints = 0, then no curve will be returned by the computation, only the dosages)pbdoc")
                .def(py::init<std::string, Common::DateTime, Common::DateTime, double, Core::ComputingOption, Common::DateTime, Core::BestCandidatesOption, 
                              Core::LoadingOption, Core::RestPeriodOption, Core::SteadyStateTargetOption, Core::TargetExtractionOption, Core::FormulationAndRouteSelectionOption>(), R"pbdoc(
                      ComputingTraitAdjustment Simple constructor.
                      
                      id:                                     Id of the request.
                      start:                                  Start time of the range to be calculated.
                      end:                                    End time of the range to be calculated.
                      nbr_points_per_hour:                    Requested number of points per hour.
                      computing_option:                       Some computing options (type of parameters, what compartments).
                      adjustment_time:                        Time at which the adjustment has to be calculated.
                      candidates_option:                      Selection of best candidates options.
                      loading_option:                         Selects if a loading dose can be proposed or not.
                      rest_period_option:                      Selects if a rest period can be proposed or not.
                      steady_state_target_option:             Indicates if the targets have to be evaluated at steady state.
                      target_extraction_option:               Target extraction options.
                      formulation_and_route_selection_option: Selection of the formulation and route options.)pbdoc",
                      py::arg("id"), 
                      py::arg("start"), 
                      py::arg("end"), 
                      py::arg("nbr_points_per_hour"), 
                      py::arg("computing_option"), 
                      py::arg("adjustment_time"), 
                      py::arg("candidates_option"), 
                      py::arg("loading_option"), 
                      py::arg("rest_period_option"), 
                      py::arg("steady_state_target_option"), 
                      py::arg("target_extraction_option"), 
                      py::arg("formulation_and_route_selection_option"));

        py::class_<Core::ComputingTraitConcentration, Core::ComputingTraitStandard, std::unique_ptr<Core::ComputingTraitConcentration, py::nodelete>>(handle, "ComputingTraitConcentration", R"pbdoc(
                  The ComputingTraitConcentration class.
                  
                  This class represents a request for a single prediction)pbdoc")
                .def(py::init<std::string, Common::DateTime, Common::DateTime, double, Core::ComputingOption>(), R"pbdoc(
                      ComputingTraitConcentration Simple constructor.
                      
                      id:                   Id of the request.
                      start:                Start time of the range to be calculated.
                      end:                  End time of the range to be calculated.
                      nbr_points_per_hour:  Requested number of points per hour.
                      computing_option:     Some computing options (type of parameters, what compartments).)pbdoc",
                      py::arg("id"), 
                      py::arg("start"), 
                      py::arg("end"), 
                      py::arg("nbr_points_per_hour"), 
                      py::arg("computing_option"));

        py::class_<Core::ComputingTraitPercentiles, Core::ComputingTraitStandard, std::unique_ptr<Core::ComputingTraitPercentiles, py::nodelete>>(handle, "ComputingTraitPercentiles", R"pbdoc(
                  The ComputingTraitPercentiles class.
                  
                  This class embeds all information for calculating percentiles. Additionnaly to standard single predictions, it requires the list of asked percentiles.
                  This list is a vector of values in [0.0, 100.0])pbdoc")
                .def(py::init<std::string, Common::DateTime, Common::DateTime, std::vector<double>, double, Core::ComputingOption>(), R"pbdoc(
                      ComputingTraitPercentiles Simple constructor.
                      
                      id:                   Id of the request.
                      start:                Start time of the range to be calculated.
                      end:                  End time of the range to be calculated.
                      ranks:                The percentile ranks as a vector of double.
                      nbr_points_per_hour:  Requested number of points per hour.
                      computing_option:     Some computing options (type of parameters, what compartments).
                      aborter:              An aborter objet to to cancel computation.)pbdoc",
                      py::arg("id"), 
                      py::arg("start"), 
                      py::arg("end"), 
                      py::arg("ranks"),
                      py::arg("nbr_points_per_hour"), 
                      py::arg("computing_option"));


        py::enum_<Core::CompartmentInfo::CompartmentType>(handle, "CompartmentType", R"pbdoc(
                  Transparent binding of the CompartmentType Enum Class)pbdoc")
                .value("active_moiety", Core::CompartmentInfo::CompartmentType::ActiveMoiety)
                .value("analyte", Core::CompartmentInfo::CompartmentType::Analyte)
                .value("active_moiety_and_analyte", Core::CompartmentInfo::CompartmentType::ActiveMoietyAndAnalyte)
                .value("compartment", Core::CompartmentInfo::CompartmentType::Compartment)
                .export_values();

        py::class_<Core::CompartmentInfo>(handle, "CompartmentInfo", R"pbdoc(
                  The CompartmentInfo class.
                  
                  This class is meant to represent the organization of prediction curves. As there can be more than one analyte or active moiety, and that there \
                  could be compartments concentration in the results, there is a need to identify what is present in the resulting vectors.
                  For instance, a SinglePredictionData will embed a vector of CompartmentInfo.
                  The id should embed the analyte Id, the activeMoiety Id, or a compartment Id.)pbdoc")
                .def_property_readonly("type", &Core::CompartmentInfo::getType);

        // TODO -> Check function description and variable description
        handle.def("compute_tqf2object", &compute_tqf2object, R"pbdoc(
                    This function is the entry point that will launch the calculation process.
                    
                    query_string:        Query string.
                    drugs_folders_paths: List of paths to the drugsfiles folders.
                    
                    return: XML as object.)pbdoc",
                    py::arg("query_string"),
                    py::arg("drugs_folders_paths"));

        // TODO -> Check function description and variable description
        handle.def("compute_tqf", &compute_tqf, R"pbdoc(
                    This function is the entry point that will launch the calculation process.
                    
                    query_string:        Query string.
                    drugs_folders_paths: List of paths to the drugsfiles folders.
                    
                    return: XML as string.)pbdoc",
                    py::arg("query_string"),
                    py::arg("drugs_folders_paths"));

        // TODO -> Check function description and variable description
        handle.def("compute_objects", &compute_objects, R"pbdoc(
                    This function is the entry point that will launch the calculation process.
                    
                    query_data:          Query data object.
                    drugs_folders_paths: List of paths to the drugsfiles folders.
                    
                    return: XML as object.)pbdoc",
                    py::arg("query_data"),
                    py::arg("drugs_folders_paths"));

        handle.def("create_request_data", &create_request_data, R"pbdoc(
                    This function allow the creation of an object of type RequestData in the C++.
                    
                    request_id:      ID of the request.
                    drug_id:         Unique ID of the drug.
                    drugmodel_id:    Unique ID of the drug model to be used
                    computing_trait: This parameter represents a request for a single prediction.)pbdoc",
                    py::arg("request_id"),
                    py::arg("drug_id"), 
                    py::arg("drugmodel_id"), 
                    py::arg("computing_trait"));

        handle.def("compute_query_data", &compute_query_data, R"pbdoc(
                    This function launch the calculations).
                    
                    query_id:            ID of the query.
                    client_id:           ID of the client.
                    query_date:          Date of the query.
                    language:            Language of the query.
                    drug_id:             Unique ID of the drug.
                    active_principle:    Active principle of the drug.
                    brand_name:          Brand name of the drug.
                    atc:                 Drug atc.
                    covariates:          List of covariates used for this query.
                    samples:             List of samples.
                    targets:             List of targets for the drug used in the query.
                    ranges:              List of dosages ranges.
                    drugs_folders_paths: List of paths to the drugsfiles folders.)pbdoc",
                    py::arg("query_id"),
                    py::arg("client_id"), 
                    py::arg("query_date"), 
                    py::arg("language"), 
                    py::arg("drug_id"), 
                    py::arg("active_principle"), 
                    py::arg("brand_name"), 
                    py::arg("atc"), 
                    py::arg("covariates"), 
                    py::arg("samples"), 
                    py::arg("targets"), 
                    py::arg("ranges"), 
                    py::arg("drugs_folders_paths"));

    }
} // namespace wrapper
} // namespace tucuxi