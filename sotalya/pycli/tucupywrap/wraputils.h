#ifndef WRAPUTILS_H
#define WRAPUTILS_H

#include <tucuquery/computingqueryresponse.h>
#include "tucuquery/querystatus.h"
#include "tucuquery/querydata.h"
#include "tucuquery/computingquery.h"
#include "tucucore/drugtreatment/drugtreatment.h"
#include "tucuquery/querytocoreextractor.h"
#include "tucucore/drugmodelrepository.h"
#include "tucucore/treatmentdrugmodelcompatibilitychecker.h"
#include "tucucommon/xmlimporter.h"
#include "tucucore/computingservice/computingrequest.h"


namespace Tucuxi {
    namespace PyWrap {
        /**
         * This class is derived from QueryToCoreExtractor::extractComputingQuery
         * With a few differences :
         * - drugModelRepository is given, not obtained from the ComponentManager (CM is not used in Tucuxi::PyWrap)
         */
        Query::QueryStatus createComputingQuery(
                Core::IDrugModelRepository* drugModelRepository,
                const Query::QueryData& _queryData,
                Query::ComputingQuery& _computingQuery,
                std::vector<std::unique_ptr<Core::DrugTreatment> >& _drugTreatments,
                Query::ComputingQueryResponse& computingQueryResponse);

        Query::ComputingQueryResponse compute_query_data(std::string _query_id,
                                                         std::string _client_id,
                                                         Common::DateTime _query_date,
                                                         std::string _language,
                                                         std::string _drug_id,
                                                         std::string _activePrinciple,
                                                         std::string _brandName,
                                                         std::string _atc,
                                                         std::vector<Core::PatientCovariate> _covariates,
                                                         std::vector<Query::FullSample> _samples,
                                                         std::vector<Core::Target> _targets,
                                                         std::vector<Core::DosageTimeRange> _ranges,
                                                         std::vector<std::string> _folders);

        void create_request_data(std::string& _request_id,
                                 std::string& _drug_id,
                                 std::string& _drugmodel_id,
                                 Core::ComputingTrait* _computingTrait);
}} // namespace Tucuxi::PyWrap

#endif // WRAPUTILS_H
