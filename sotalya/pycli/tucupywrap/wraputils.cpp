#include "wraputils.h"
#include "wrapper.h"
#include <typeinfo>
#include <ostream>


namespace Tucuxi {
    namespace PyWrap {

        std::vector<std::unique_ptr<Query::RequestData>> pendingRequests;

        Query::QueryStatus createComputingQuery(
                Core::IDrugModelRepository* drugModelRepository,
                const Query::QueryData& _queryData,
                Query::ComputingQuery& _computingQuery,
                std::vector<std::unique_ptr<Core::DrugTreatment> >& _drugTreatments,
                Query::ComputingQueryResponse& computingQueryResponse)
        {
            auto queryExtractor = Query::QueryToCoreExtractor();
            Core::TreatmentDrugModelCompatibilityChecker checker;

            for (const std::unique_ptr<Query::RequestData>& requestData : _queryData.getRequests())
            {
                auto drugTreatment = queryExtractor.extractDrugTreatment(_queryData, *requestData);
                if (drugTreatment == nullptr)
                {
                    computingQueryResponse.setQueryStatus(Query::QueryStatus::ImportError, "Unable to import the drug treatment");
                    return computingQueryResponse.getQueryStatus();
                }

                Core::DrugModel *drugModel = nullptr;

                if (drugModelRepository != nullptr)
                {
                    drugModel = drugModelRepository->getDrugModelById(requestData->getDrugModelID());
                }

                if (drugModel == nullptr || !checker.checkCompatibility(drugTreatment.get(), drugModel)) {
                    computingQueryResponse.setQueryStatus(Query::QueryStatus::ImportError, "Unable to import the drug model");
                    return computingQueryResponse.getQueryStatus();
                }

                std::unique_ptr<Core::ComputingRequest> computingRequest =
                        std::make_unique<Core::ComputingRequest>(
                                requestData->getRequestID(),
                                *drugModel,
                                *drugTreatment,
                                std::move(requestData->m_pComputingTrait));
                _computingQuery.addComputingRequest(std::move(computingRequest));

                _drugTreatments.push_back(std::move(drugTreatment));
            }

            return Query::QueryStatus::Ok;
        }

        void create_request_data(std::string& _request_id,
                                               std::string& _drug_id,
                                               std::string& _drugmodel_id,
                                               Core::ComputingTrait* _computingTrait)
        {
            // Dynamic cast attempt - ComputingTraitAdjustment
            auto p = dynamic_cast<Core::ComputingTraitAdjustment*>(_computingTrait);
            if (p != nullptr)
            {
                auto ptr = std::make_unique<Core::ComputingTraitAdjustment>(*p);
                pendingRequests.push_back(
                        std::make_unique<Query::RequestData>(_request_id, _drug_id, _drugmodel_id, std::move(ptr)));
                return;
            }

            // Dynamic cast attempt - ComputingTraitPercentiles
            auto q = dynamic_cast<Core::ComputingTraitPercentiles*>(_computingTrait);
            if (q != nullptr)
            {
                auto ptr = std::make_unique<Core::ComputingTraitPercentiles>(*q);
                pendingRequests.push_back(
                        std::make_unique<Query::RequestData>(_request_id, _drug_id, _drugmodel_id, std::move(ptr)));
                return;
            }

            // Dynamic cast attempt - ComputingTraitConcentration
            auto r = dynamic_cast<Core::ComputingTraitConcentration*>(_computingTrait);
            if (r != nullptr)
            {
                auto ptr = std::make_unique<Core::ComputingTraitConcentration>(*r);
                pendingRequests.push_back(
                        std::make_unique<Query::RequestData>(_request_id, _drug_id, _drugmodel_id, std::move(ptr)));
                return;
            }

            // Dynamic cast attempt - ComputingTraitAtMeasures
            auto s = dynamic_cast<Core::ComputingTraitAtMeasures*>(_computingTrait);
            if (s != nullptr)
            {
                auto ptr = std::make_unique<Core::ComputingTraitAtMeasures>(*s);
                pendingRequests.push_back(
                        std::make_unique<Query::RequestData>(_request_id, _drug_id, _drugmodel_id, std::move(ptr)));
                return;
            }

            // Dynamic cast attempt - ComputingTraitSinglePoints
            auto t = dynamic_cast<Core::ComputingTraitSinglePoints*>(_computingTrait);
            if (t != nullptr)
            {
                auto ptr = std::make_unique<Core::ComputingTraitSinglePoints>(*t);
                pendingRequests.push_back(
                        std::make_unique<Query::RequestData>(_request_id, _drug_id, _drugmodel_id, std::move(ptr)));
                return;
            }

            // THIS IS UNSAFE CODE AND ISN'T SUPPOSED TO EVER HAPPENED
            std::cout << "The unsafe code in \"create_request_data\" was triggered!" << std::endl;
            std::unique_ptr <Core::ComputingTrait> ptr;
            ptr.reset(_computingTrait);
            pendingRequests.push_back(
                    std::make_unique<Query::RequestData>(_request_id, _drug_id, _drugmodel_id, std::move(ptr)));

        }

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
                                           std::vector<std::string> _folders)
        {
            // build the query
            std::vector<std::unique_ptr<Tucuxi::Core::PatientCovariate>> covariates;
            std::vector<std::unique_ptr<Tucuxi::Query::FullSample>> samples;
            std::vector<std::unique_ptr<Tucuxi::Core::Target>> targets;

            for (const auto& covariate : _covariates)
            {
                covariates.push_back(std::make_unique<Core::PatientCovariate>(covariate));
            }

            for (const auto& sample : _samples)
            {
                samples.push_back(std::make_unique<Query::FullSample>(sample));
            }

            for (const auto& target : _targets)
            {
                targets.push_back(std::make_unique<Core::Target>(target));
            }

            auto dosageHistory = std::make_unique<Core::DosageHistory>();

            for (const auto& range : _ranges)
            {
                dosageHistory->addTimeRange(range);
            }

            auto treatment = std::make_unique<Query::Treatment>(std::move(dosageHistory));

            auto patient = std::make_unique<Query::PatientData>(covariates);

            // This doesn't handle properly multi-drug cases with helper function
            // See the report for documentation of that case
            std::vector<std::unique_ptr<Query::DrugData>> drugs;
            drugs.push_back(std::make_unique<Query::DrugData>(_drug_id,
                                                              _activePrinciple,
                                                              _brandName,
                                                              _atc,
                                                              std::move(treatment),
                                                              samples,
                                                              targets));

            auto parameters = std::make_unique<Query::DrugTreatmentData>(std::move(patient), std::move(drugs));

            std::vector<std::unique_ptr<Tucuxi::Query::RequestData>> requests;

            auto queryData = new Query::QueryData(_query_id,
                _client_id,
                _query_date,
                _language,
                std::move(parameters),
                pendingRequests);

            pendingRequests.clear();

            return compute_objects(*queryData, _folders);
        }

}} // namespace Tucuxi::PyWrap