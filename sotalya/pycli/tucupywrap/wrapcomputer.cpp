#include "wrapcomputer.h"

#include "tucucore/computingcomponent.h"
#include "tucucore/computingservice/icomputingservice.h"
#include "tucucore/overloadevaluator.h"
#include "tucuquery/computingresponseexport.h"
#include "tucuquery/querycomputer.h"

namespace Tucuxi {
namespace PyWrap {

    WrapComputer::WrapComputer() = default;

    void WrapComputer::compute(Query::ComputingQuery& computingQuery, Query::ComputingQueryResponse& computingQueryResponse) {
        // Change the settings for the tests
        Core::SingleOverloadEvaluator::getInstance()->setValues(100000, 5000, 10000);

        auto queryComputer = std::make_unique<Query::QueryComputer>();

        queryComputer->compute(computingQuery, computingQueryResponse);
    }
}

}


