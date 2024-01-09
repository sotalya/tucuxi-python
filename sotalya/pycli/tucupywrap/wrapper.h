//
// Created by sicriss on 08.05.22.
//

#ifndef TUCUPYWRAP_WRAPPER_H
#define TUCUPYWRAP_WRAPPER_H

#include "tucucore/computingservice/computingresult.h"
#include "tucucore/computingservice/computingresponse.h"
#include "tucucore/computingservice/computingrequest.h"
#include "tucuquery/computingqueryresponsexmlexport.h"
#include "tucuquery/computingqueryresponse.h"
#include "tucuquery/computingquery.h"
#include "tucucore/drugmodelrepository.h"
#include "tucuquery/queryimport.h"
#include "tucucommon/xmlimporter.h"
#include "wrapcomputer.h"
#include "wraputils.h"
#include "tucucommon/unit.h"
#include "tucucommon/datetime.h"

namespace Tucuxi {
    namespace PyWrap {

        Query::ComputingQueryResponse
        compute_objects(Query::QueryData &_queryData, std::vector <std::string> _folders);

        Query::ComputingQueryResponse
        compute_tqf2object(std::string _queryString, std::vector <std::string> _folders);
        
        std::string
        compute_tqf(const std::string &_queryString, const std::vector<std::string> _folders);
    }
}

#endif //TUCUPYWRAP_WRAPPER_H
