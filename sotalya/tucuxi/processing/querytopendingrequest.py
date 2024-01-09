# !/usr/bin/python3

from ..data.query import *
from ..data.pendingrequest import *


class QueryToPendingRequest:

    def __init__(self):
        print('create a translator from query to pending request')

    def timeToHours(self, t):
        s = t.split(':')
        t = int(s[0]) + int(s[1])/60 + int(s[2])/3600
        return t

    def translate(self, query):
        pending_request = PendingRequest()

        pending_request.requestId = query.queryId

        pending_request.requestState = 'open'

        pending_request.patient = Patient()
        pending_request.patient.patientId = query.patientId

        drug_treatment = PRDrugTreatment()

        drug_treatment.drugId = query.requests[0].drugId
        drug_treatment.activePrinciple = 'theactiveprinciple'

        for drug in query.drugs:
            for sample in drug.samples:
                drug_treatment.samples.append(sample)

            for dtr in drug.dosageHistory.dosageTimeRanges:
                dosage = LastingDosage()

                dosage.interval = dtr.dosage.interval
                dosage.interval_unit = '-'
                dosage.formulationAndRoute.administrationRoute = 'INFUSION'
                dosage.dose.value = dtr.dosage.dose.value
                dosage.dose.infusionTimeInMinutes = dtr.dosage.dose.infusionTimeInMinutes
                dosage.dose.unit = dtr.dosage.dose.unit

                dosage_time_range = DosageTime.create_dosage_time_range(dtr.start, dosage, dtr.end)
                drug_treatment.dosages.append(dosage_time_range)

        for covariate in query.covariates:
            drug_treatment.patientCovariates.append(covariate)

        # drug_treatment = DrugTreatment()
        # # TODO: Not very good like this. Should be refactored
        # drug_treatment.drugId = query.requests[0].drugId
        # drug_treatment.activePrinciple = 'theactiveprinciple'
        #
        # pending_request.patient = Patient()
        # pending_request.patient.patientId = query.patient_id

        # for covariate in query.covariates:
        #     drug_treatment.patientCovariates.append(covariate)



                # dosage.formulationAndRoute.administrationRoute = 'intravenousDrip'
                # dosage.formulationAndRoute.administrationName = 'foo bar'
                # dosage.formulationAndRoute.formulation = 'parenteralSolution'




                # dosage = DosageRepeat()
                # dosage.startDate = query_dosage.startDate
                # dosage.endDate = query_dosage.endDate
                #
                # dosage.interval = query_dosage.interval
                # dosage.interval_unit = '-'
                #
                # dose = Dose()
                # dose.administrationRoute = 'INFUSION'
                #
                # dose.infusionTimeUnit = query_dosage.dose.dose.infusionTimeUnit
                # dose.infusionTime = query_dosage.dose.dose.infusionTime
                # dose.doseValue = query_dosage.dose.dose.doseValue
                # dose.doseUnit = query_dosage.dose.dose.doseUnit
                # dosage.dose = dose

        pending_request.drugTreatment = drug_treatment
        return pending_request

    def new_translate(self, query: Query):

        pending_request = PendingRequest()

        pending_request.requestId = query.queryId

        pending_request.requestState = 'open'

        pending_request.patient = Patient()
        pending_request.patient.patientId = query.patientId

        drug_treatment = PRDrugTreatment()

        drug_treatment.drugId = query.requests[0].drugId
        drug_treatment.activePrinciple = 'theactiveprinciple'

        for covariate in query.covariates:
            new_covariate = PRPatientCovariate.create_patient_covariate(covariate.covariateId, covariate.date, covariate.value, covariate.unit, covariate.dataType, covariate.nature)
            drug_treatment.patientCovariates.append(new_covariate)

        for sample in query.drugs[0].samples:
            new_sample = PRSample.create_sample(sample.id, sample.sampledate, sample.analyteId, sample.concentration, sample.unit, sample.sampledate)
            drug_treatment.samples.append(new_sample)

        for drug in query.drugs:

            for dtr in drug.dosageHistory.dosageTimeRanges:
                dosage = PRDosageRepeat()
                dosage.startDate = dtr.start
                dosage.endDate = dtr.end
                dosage.interval = dtr.dosage.interval
                dosage.interval_unit = '-'

                dose = PRDose()
                dose.doseUnit = dtr.dosage.dose.unit
                dose.doseValue = dtr.dosage.dose.value
                dose.absorptionModel = dtr.dosage.formulationAndRoute.absorptionModel
                dose.administrationRoute = dtr.dosage.formulationAndRoute.administrationRoute
                dose.administrationName = dtr.dosage.formulationAndRoute.administrationName
                dose.formulation = dtr.dosage.formulationAndRoute.formulation
                dose.infusionTime = dtr.dosage.dose.infusionTimeInMinutes
                dose.infusionTimeUnit = 'min'

                dosage.dose = dose

                drug_treatment.dosages.append(dosage)

        pending_request.drugTreatment = drug_treatment
        return pending_request