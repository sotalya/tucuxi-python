#ifndef WRAPCOMPUTER_H
#define WRAPCOMPUTER_H

#include <tucuquery/computingquery.h>
#include <tucuquery/computingqueryresponse.h>
#include "tucucommon/xmlimporter.h"


namespace Tucuxi {
    namespace PyWrap {
        class WrapComputer
        {
        public:
            WrapComputer();

            ///
            /// \brief computes a full query, and populates the responses
            /// \param _query The query object, embedded all information
            /// \param _response The query response
            /// The list of responses embedded in the query response correspond to the
            /// ComputingRequest embedded in _query
            ///
            void compute(Query::ComputingQuery &computingQuery, Query::ComputingQueryResponse &computingQueryResponse);
        };


    } // namespace PyWrap
} // namespace Tucuxi

#endif // WRAPCOMPUTER_H
