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

        pending_request.patient = PRPatient()
        pending_request.patient.patientId = query.patientId
        pending_request.patient.firstname = query.patient["person"].firstName
        pending_request.patient.lastname = query.patient["person"].lastName
        pending_request.patient.address = query.patient["person"].street
        pending_request.patient.city = query.patient["person"].city
        pending_request.patient.postcode = query.patient["person"].postalCode
        pending_request.patient.state = query.patient["person"].state
        pending_request.patient.country = query.patient["person"].country
        pending_request.patient.email_address = query.patient["person"].emailAddress
        pending_request.patient.email_type = query.patient["person"].emailType
        pending_request.patient.phone_number = query.patient["person"].phoneNumber
        pending_request.patient.phone_type = query.patient["person"].phoneType

        pending_request.patient.institute.instituteId = query.patient["institute"].instituteId
        pending_request.patient.institute.name = query.patient["institute"].name
        pending_request.patient.institute.address = query.patient["institute"].street
        pending_request.patient.institute.city = query.patient["institute"].city
        pending_request.patient.institute.postcode = query.patient["institute"].postalCode
        pending_request.patient.institute.state = query.patient["institute"].state
        pending_request.patient.institute.country = query.patient["institute"].country
        pending_request.patient.institute.email_address = query.patient["institute"].emailAddress
        pending_request.patient.institute.email_type = query.patient["institute"].emailType
        pending_request.patient.institute.phone_number = query.patient["institute"].phoneNumber
        pending_request.patient.institute.phone_type = query.patient["institute"].phoneType

        pending_request.mandator = PRMandator()
        pending_request.mandator.firstname = query.mandator["person"].firstName
        pending_request.mandator.lastname = query.mandator["person"].lastName
        pending_request.mandator.address = query.mandator["person"].street
        pending_request.mandator.city = query.mandator["person"].city
        pending_request.mandator.postcode = query.mandator["person"].postalCode
        pending_request.mandator.state = query.mandator["person"].state
        pending_request.mandator.country = query.mandator["person"].country
        pending_request.mandator.email_address = query.mandator["person"].emailAddress
        pending_request.mandator.email_type = query.mandator["person"].emailType
        pending_request.mandator.phone_number = query.mandator["person"].phoneNumber
        pending_request.mandator.phone_type = query.mandator["person"].phoneType

        pending_request.mandator.institute.instituteId = query.mandator["institute"].instituteId
        pending_request.mandator.institute.name = query.mandator["institute"].name
        pending_request.mandator.institute.address = query.mandator["institute"].street
        pending_request.mandator.institute.city = query.mandator["institute"].city
        pending_request.mandator.institute.postcode = query.mandator["institute"].postalCode
        pending_request.mandator.institute.state = query.mandator["institute"].state
        pending_request.mandator.institute.country = query.mandator["institute"].country
        pending_request.mandator.institute.email_address = query.mandator["institute"].emailAddress
        pending_request.mandator.institute.email_type = query.mandator["institute"].emailType
        pending_request.mandator.institute.phone_number = query.mandator["institute"].phoneNumber
        pending_request.mandator.institute.phone_type = query.mandator["institute"].phoneType

        drug_treatment = PRDrugTreatment()

        drug_treatment.drugId = query.requests[0].drugId
        drug_treatment.activePrinciple = query.drugs[0].activePrinciple
        drug_treatment.brandName = query.drugs[0].brandName

        for covariate in query.covariates:
            new_covariate = PRPatientCovariate.create_patient_covariate(
                covariate.covariateId,
                covariate.date,
                covariate.value,
                covariate.unit,
                covariate.dataType,
                covariate.nature
            )
            drug_treatment.patientCovariates.append(new_covariate)

        for sample in query.drugs[0].samples:
            new_sample = PRSample.create_sample(
                sample.id,
                sample.sampledate,
                sample.analyteId,
                sample.concentration,
                sample.unit,
                sample.sampledate
            )
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
                dose.administrationRoute = dtr.dosage.formulationAndRoute.administrationRoute
                dose.administrationName = dtr.dosage.formulationAndRoute.administrationName
                dose.formulation = dtr.dosage.formulationAndRoute.formulation
                dose.infusionTime = dtr.dosage.dose.infusionTimeInMinutes
                dose.infusionTimeUnit = 'min'

                dosage.dose = dose

                drug_treatment.dosages.append(dosage)

        pending_request.drugTreatment = drug_treatment
        return pending_request
