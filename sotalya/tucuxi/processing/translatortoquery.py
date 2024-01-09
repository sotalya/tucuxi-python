
# !/usr/bin/python3

import sys
import os
sys.path.append(os.path.abspath(".."))

from ..data.query import *


class TranslatorToQuery:

    def __init__(self):
        print('create a translator to query')

    def translate_to_query(self, pending_request):
        query = Query()
        query.queryId = 'theQueryId'
        query.patientId = 'themodelid'
        query.drugs[0].drugId = pending_request.drugTreatment.drugId
        query.drugs[0].activePrinciple = pending_request.drugTreatment.activePrinciple

        for covariate in pending_request.drugTreatment.patientCovariates:
            query.covariates.append(covariate)

        for sample in pending_request.drugTreatment.samples:
            query.drugs[0].samples.append(sample)

        for target in pending_request.drugTreatment.targets:
            query.drugs[0].targets.append(target)

        for dosage in pending_request.drugTreatment.dosages:
            query.drugs[0].dosageHistory[0].append(dosage)

        return query
