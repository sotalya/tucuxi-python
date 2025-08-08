#!/usr/bin/python3


import os
from bs4 import BeautifulSoup
import xml.dom.minidom
from ..data.query import *

from ..data.requests import *
from ..data.xpertrequests import *
from ..tucuxi.utils import timedelta_to_str
# PredictionTraits, PredictionAtTimesTraits, PredictionAtSampleTimesTraits, \
#     PercentilesTraits, AdjustmentTraits


tqf_template = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<query version="1.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="xml_query.xsd">

    <queryId></queryId>
    <clientId></clientId>
    <date></date> <!-- Date the xml has been sent -->
    <language>en</language>

    <!-- Administrative data -->
    <admin>
    </admin>

    <drugTreatment>
        <!-- All the information regarding the patient -->
        <patient>
            <covariates>
            </covariates>
        </patient>
        <!-- List of the drugs informations we have concerning the patient -->
        <drugs>
            <!-- All the information regarding the drug -->
            <drug>
                <drugId></drugId>
                <activePrinciple></activePrinciple>
                <brandName></brandName>
                <atc></atc>
                <!-- All the information regarding the treatment -->
                <treatment>
                    <dosageHistory>
                    </dosageHistory>
                </treatment>
                <!-- Samples history -->
                <samples>
                </samples>
            </drug>
        </drugs>
    </drugTreatment>
    <!-- List of the requests we want the server to take care of -->
    <requests></requests>

</query>
'''

class ExportTqf:
    def __init__(self):
        self.soup = None

    def export_to_string(self, query: Query, template_filename: str = ''):
        if template_filename == '':
            content = tqf_template
        else:
            content = open(template_filename).read()

        self.soup = BeautifulSoup(content, 'xml')

        self.soup.query.queryId.string = query.queryId
        self.soup.query.clientId.string = query.patientId
        self.soup.query.date.string = str(query.date)
        if query.mandator:
            self.soup.query.admin.append(self.create_mandator_admin(query.mandator))
        if query.patient:
            self.soup.query.admin.append(self.create_patient_admin(query.patient))

        for d in query.drugs:
            self.soup.query.drugs.drug.drugId.string = d.drugId
            self.soup.query.drugs.drug.activePrinciple.string = d.activePrinciple
            self.soup.query.drugs.drug.brandName.string = d.brandName
            self.soup.query.drugs.drug.atc.string = d.ATC

            for sample in d.samples:
                samp = self.create_sample(sample)
                self.soup.query.drugTreatment.drugs.drug.samples.append(samp)

            for dtr in d.dosageHistory.dosageTimeRanges:
                d = self.create_simple_dosage_with_interval(dtr)
                self.soup.query.drugs.drug.dosageHistory.append(d)

        for covariate in query.covariates:
            cov = self.create_covariate(covariate)
            self.soup.query.drugTreatment.patient.covariates.append(cov)

        for request in query.requests:
            req = self.create_request(request)
            self.soup.query.requests.append(req)

        for xpertrequest in query.xpertrequests:
            req = self.create_xpertrequest(xpertrequest)
            self.soup.query.requests.append(req)

        xmlout = str(self.soup)

        xml1 = xml.dom.minidom.parseString(xmlout)
        outputstring = xml1.toprettyxml()
        dom_string = os.linesep.join([s for s in outputstring.splitlines() if s.strip()])

        return dom_string

    def export_to_file(self, query: Query, filename, template_filename: str = ''):

        dom_string = self.export_to_string(query, template_filename)

        outputfile = open(filename, 'w')
        outputfile.write(dom_string)
        outputfile.close()

        return True

    def create_single_boolean_node(self, tag_name, tag_value):
        node = self.soup.new_tag(tag_name)
        if tag_value:
            node.string = "true"
        else:
            node.string = "false"
        return node

    def create_single_node(self, tag_name, tag_value):
        node = self.soup.new_tag(tag_name)
        node.string = tag_value
        return node

    def create_single_node_double(self, tag_name, tag_value):
        node = self.soup.new_tag(tag_name)
        node.string = str(tag_value)
        return node

    def create_single_node_date(self, tag_name, tag_value):
        node = self.soup.new_tag(tag_name)
        if (type(tag_value) is datetime):
            node.string = tag_value.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            node.string = tag_value
        return node

    def create_computing_option(self, request):
        computing_option = self.soup.new_tag('computingOption')
        computing_option.append(self.create_single_node('parametersType',
                                                        request.computingOption.parametersType.value))
        computing_option.append(self.create_single_node('compartmentOption',
                                                        request.computingOption.compartmentOption.value))
        computing_option.append(
            self.create_single_boolean_node('retrieveStatistics',
                                            request.computingOption.retrieveStatistics))
        computing_option.append(
            self.create_single_boolean_node('retrieveParameters',
                                            request.computingOption.retrieveParameters))
        computing_option.append(
            self.create_single_boolean_node('retrieveCovariates',
                                            request.computingOption.retrieveCovariates))
        return computing_option

    def create_options(self, request):
        options = self.soup.new_tag('options')
        options.append(self.create_single_node('bestCandidatesOption',
                                               request.options.bestCandidatesOption.value))
        options.append(self.create_single_node('loadingOption',
                                               request.options.loadingOption.value))
        options.append(self.create_single_node('restPeriodOption',
                                               request.options.restPeriodOption.value))
        options.append(self.create_single_node('steadyStateTargetOption',
                                               request.options.steadyStateTargetOption.value))
        options.append(self.create_single_node('targetExtractionOption',
                                               request.options.targetExtractionOption.value))
        options.append(self.create_single_node('formulationAndRouteSelectionOption',
                                               request.options.formulationAndRouteSelectionOption.value))
        return options

    def create_percentile_ranks_type(self, request: PercentilesTraits):
        ranks = self.soup.new_tag('ranks')
        for percentile in request.ranks:
            ranks.append(self.create_single_node('rank', str(percentile)))
        return ranks

    def create_date_interval(self, request):
        date_interval = self.soup.new_tag('dateInterval')
        date_interval.append(self.create_single_node_date('start',
                                                          request.dateInterval.startDate))
        date_interval.append(self.create_single_node_date('end',
                                                          request.dateInterval.endDate))

        return date_interval

    def create_mandator_admin(self, mandator):
        # Mandator.
        mandatorTag = self.soup.new_tag('mandator')
        mandatorPerson = self.soup.new_tag('person')
        mandatorTag.append(mandatorPerson)
        mandatorInstitute = self.soup.new_tag('institute')
        mandatorTag.append(mandatorInstitute)

        # Mandator - person.
        mandatorPerson.append(
            self.create_single_node_date('id',
                                         mandator["person"].personId)
        )
        mandatorPerson.append(
            self.create_single_node_date('title',
                                         mandator["person"].title)
        )
        mandatorPerson.append(
            self.create_single_node_date('firstName',
                                         mandator["person"].firstName)
        )
        mandatorPerson.append(
            self.create_single_node_date('lastName',
                                         mandator["person"].lastName)
        )

        mandatorPersonAddress = self.soup.new_tag('address')
        mandatorPerson.append(mandatorPersonAddress)
        mandatorPersonAddress.append(
            self.create_single_node_date('street',
                                         mandator["person"].street)
        )
        mandatorPersonAddress.append(
            self.create_single_node_date('postalCode',
                                         mandator["person"].postalCode)
        )
        mandatorPersonAddress.append(
            self.create_single_node_date('city',
                                         mandator["person"].city)
        )
        mandatorPersonAddress.append(
            self.create_single_node_date('state',
                                         mandator["person"].state)
        )
        mandatorPersonAddress.append(
            self.create_single_node_date('country',
                                         mandator["person"].country)
        )

        mandatorPersonPhone = self.soup.new_tag('phone')
        mandatorPerson.append(mandatorPersonPhone)
        mandatorPersonPhone.append(
            self.create_single_node_date('number',
                                         mandator["person"].phoneNumber)
        )
        mandatorPersonPhone.append(
            self.create_single_node_date('type',
                                         mandator["person"].phoneType)
        )

        mandatorPersonEmail = self.soup.new_tag('email')
        mandatorPerson.append(mandatorPersonEmail)
        mandatorPersonEmail.append(
            self.create_single_node_date('address',
                                         mandator["person"].emailAddress)
        )
        mandatorPersonEmail.append(
            self.create_single_node_date('type',
                                         mandator["person"].emailType)
        )

        # Mandator - institute.
        mandatorInstitute.append(
            self.create_single_node_date('id',
                                         mandator["institute"].instituteId)
        )
        mandatorInstitute.append(
            self.create_single_node_date('name',
                                         mandator["institute"].name)
        )

        mandatorInstituteAddress = self.soup.new_tag('address')
        mandatorInstitute.append(mandatorInstituteAddress)
        mandatorInstituteAddress.append(
            self.create_single_node_date('street',
                                         mandator["institute"].street)
        )
        mandatorInstituteAddress.append(
            self.create_single_node_date('postalCode',
                                         mandator["institute"].postalCode)
        )
        mandatorInstituteAddress.append(
            self.create_single_node_date('city',
                                         mandator["institute"].city)
        )
        mandatorInstituteAddress.append(
            self.create_single_node_date('state',
                                         mandator["institute"].state)
        )
        mandatorInstituteAddress.append(
            self.create_single_node_date('country',
                                         mandator["institute"].country)
        )

        mandatorInstitutePhone = self.soup.new_tag('phone')
        mandatorInstitute.append(mandatorInstitutePhone)
        mandatorInstitutePhone.append(
            self.create_single_node_date('number',
                                         mandator["institute"].phoneNumber)
        )
        mandatorInstitutePhone.append(
            self.create_single_node_date('type',
                                         mandator["institute"].phoneType)
        )

        mandatorInstituteEmail = self.soup.new_tag('email')
        mandatorInstitute.append(mandatorInstituteEmail)
        mandatorInstituteEmail.append(
            self.create_single_node_date('address',
                                         mandator["institute"].emailAddress)
        )
        mandatorInstituteEmail.append(
            self.create_single_node_date('type',
                                         mandator["institute"].emailType)
        )

        return mandatorTag

    def create_patient_admin(self, patient):
        # Patient.
        patientTag = self.soup.new_tag('patient')
        patientPerson = self.soup.new_tag('person')
        patientTag.append(patientPerson)
        patientInstitute = self.soup.new_tag('institute')
        patientTag.append(patientInstitute)

        # Patient - person.
        patientPerson.append(
            self.create_single_node_date('id',
                                         patient["person"].personId)
        )
        patientPerson.append(
            self.create_single_node_date('title',
                                         patient["person"].title)
        )
        patientPerson.append(
            self.create_single_node_date('firstName',
                                         patient["person"].firstName)
        )
        patientPerson.append(
            self.create_single_node_date('lastName',
                                         patient["person"].lastName)
        )

        patientPersonAddress = self.soup.new_tag('address')
        patientPerson.append(patientPersonAddress)
        patientPersonAddress.append(
            self.create_single_node_date('street',
                                         patient["person"].street)
        )
        patientPersonAddress.append(
            self.create_single_node_date('postalCode',
                                         patient["person"].postalCode)
        )
        patientPersonAddress.append(
            self.create_single_node_date('city',
                                         patient["person"].city)
        )
        patientPersonAddress.append(
            self.create_single_node_date('state',
                                         patient["person"].state)
        )
        patientPersonAddress.append(
            self.create_single_node_date('country',
                                         patient["person"].country)
        )

        patientPersonPhone = self.soup.new_tag('phone')
        patientPerson.append(patientPersonPhone)
        patientPersonPhone.append(
            self.create_single_node_date('number',
                                         patient["person"].phoneNumber)
        )
        patientPersonPhone.append(
            self.create_single_node_date('type',
                                         patient["person"].phoneType)
        )

        patientPersonEmail = self.soup.new_tag('email')
        patientPerson.append(patientPersonEmail)
        patientPersonEmail.append(
            self.create_single_node_date('address',
                                         patient["person"].emailAddress)
        )
        patientPersonEmail.append(
            self.create_single_node_date('type',
                                         patient["person"].emailType)
        )

        # Patient - institute.
        patientInstitute.append(
            self.create_single_node_date('id',
                                         patient["institute"].instituteId)
        )
        patientInstitute.append(
            self.create_single_node_date('name',
                                         patient["institute"].name)
        )

        patientInstituteAddress = self.soup.new_tag('address')
        patientInstitute.append(patientInstituteAddress)
        patientInstituteAddress.append(
            self.create_single_node_date('street',
                                         patient["institute"].street)
        )
        patientInstituteAddress.append(
            self.create_single_node_date('postalCode',
                                         patient["institute"].postalCode)
        )
        patientInstituteAddress.append(
            self.create_single_node_date('city',
                                         patient["institute"].city)
        )
        patientInstituteAddress.append(
            self.create_single_node_date('state',
                                         patient["institute"].state)
        )
        patientInstituteAddress.append(
            self.create_single_node_date('country',
                                         patient["institute"].country)
        )

        patientInstitutePhone = self.soup.new_tag('phone')
        patientInstitute.append(patientInstitutePhone)
        patientInstitutePhone.append(
            self.create_single_node_date('number',
                                         patient["institute"].phoneNumber)
        )
        patientInstitutePhone.append(
            self.create_single_node_date('type',
                                         patient["institute"].phoneType)
        )

        patientInstituteEmail = self.soup.new_tag('email')
        patientInstitute.append(patientInstituteEmail)
        patientInstituteEmail.append(
            self.create_single_node_date('address',
                                         patient["institute"].emailAddress)
        )
        patientInstituteEmail.append(
            self.create_single_node_date('type',
                                         patient["institute"].emailType)
        )

        return patientTag

    def create_request(self, request):
        req = self.soup.new_tag('request')
        req.append(self.create_single_node('requestId', request.requestId))
        req.append(self.create_single_node('drugId', request.drugId))
        req.append(self.create_single_node('drugModelId', request.drugModelId))

        ###################
        # PREDICTION TRAITS
        if type(request.computingTraits) == PredictionTraits:
            prediction_traits = self.soup.new_tag('predictionTraits')
            req.append(prediction_traits)
            prediction_traits.append(self.create_computing_option(request.computingTraits))
            prediction_traits.append(self.create_single_node_double(
                'nbPointsPerHour', request.computingTraits.nbPointPerHour))
            prediction_traits.append(self.create_date_interval(request.computingTraits))

        ############################
        # PREDICTION AT TIMES TRAITS
        if type(request.computingTraits) == PredictionAtTimesTraits:
            prediction_at_times_traits = self.soup.new_tag('predictionAtTimesTraits')
            req.append(prediction_at_times_traits)
            prediction_at_times_traits.append(self.create_computing_option(request.computingTraits))
            dates = self.soup.new_tag('dates')
            for d in request.computingTraits.dates:
                dates.append(self.create_single_node_date('date', d))
            prediction_at_times_traits.append(dates)

        ###################################
        # PREDICTION AT SAMPLE TIMES TRAITS
        if type(request.computingTraits) == PredictionAtSampleTimesTraits:
            prediction_at_sample_times_traits = self.soup.new_tag('predictionAtSampleTimesTraits')
            req.append(prediction_at_sample_times_traits)
            prediction_at_sample_times_traits.append(self.create_computing_option(request.computingTraits))

        ####################
        # PERCENTILES TRAITS
        if type(request.computingTraits) == PercentilesTraits:
            percentiles_traits = self.soup.new_tag('percentilesTraits')
            req.append(percentiles_traits)
            percentiles_traits.append(self.create_computing_option(request.computingTraits))
            percentiles_traits.append(self.create_single_node_double(
                'nbPointsPerHour', request.computingTraits.nbPointPerHour))
            percentiles_traits.append(self.create_date_interval(request.computingTraits))
            percentiles_traits.append(self.create_percentile_ranks_type(request.computingTraits))

        ###################
        # ADJUSTMENT TRAITS
        if type(request.computingTraits) == AdjustementTraits:
            adjustment_traits = self.soup.new_tag('adjustmentTraits')
            req.append(adjustment_traits)
            adjustment_traits.append(self.create_computing_option(request.computingTraits))
            adjustment_traits.append(self.create_single_node_double(
                'nbPointsPerHour', request.computingTraits.nbPointPerHour))
            adjustment_traits.append(self.create_date_interval(request.computingTraits))
            adjustment_traits.append(self.create_single_node_date(
                'adjustmentDate', request.computingTraits.adjustmentDate))
            adjustment_traits.append(self.create_options(request.computingTraits))

        return req

    def create_xpertrequest(self, xpertrequest):
        req = self.soup.new_tag('xpertRequest')
        req.append(self.create_single_node('drugId', xpertrequest.drugId))
        req.append(self.create_single_node('configId',
                                           xpertrequest.drugModelId))
        out_tag = self.soup.new_tag('output')
        req.append(out_tag)
        out_tag.append(self.create_single_node('format',
                                               xpertrequest.output["format"]))
        out_tag.append(self.create_single_node('language',
                                               xpertrequest.output["language"]))
        req.append(self.create_single_node('adjustmentDate',
                                           xpertrequest.adjustmentDate))
        opt_tag = self.soup.new_tag('options')
        req.append(opt_tag)
        opt_tag.append(self.create_single_node('loadingOption',
                                               xpertrequest.options["loadingOption"]))
        opt_tag.append(self.create_single_node('restPeriodOption',
                                               xpertrequest.options["restPeriodOption"]))
        opt_tag.append(self.create_single_node('targetExtractionOption',
                                               xpertrequest.options["targetExtractionOption"]))
        opt_tag.append(self.create_single_node('formulationAndRouteSelectionOption',
                                               xpertrequest.options["formulationAndRouteSelectionOption"]))

        return req

    def create_covariate(self, covariate):
        cov = self.soup.new_tag('covariate')
        cov.append(self.create_single_node('covariateId', covariate.covariateId))
        cov.append(self.create_single_node_date('date', covariate.date))
        cov.append(self.create_single_node('value', covariate.value))
        cov.append(self.create_single_node('unit', covariate.unit))
        cov.append(self.create_single_node('dataType', covariate.dataType))
        cov.append(self.create_single_node('nature', covariate.nature))
        return cov

    def create_sample(self, sample):
        sam = self.soup.new_tag('sample')
        sam.append(self.create_single_node('sampleId', sample.id))
        sam.append(self.create_single_node_date('sampleDate', sample.sampledate))
        # sam.append(self.create_single_node_date('arrivalDate', sample.arrivaldate))
        conc = self.soup.new_tag('concentrations')
        sam.append(conc)

        c = self.soup.new_tag('concentration')
        conc.append(c)

        c.append(self.create_single_node('analyteId', sample.analyteId))
        c.append(self.create_single_node_double('value', sample.concentration))
        c.append(self.create_single_node('unit', sample.unit))

        return sam

    def create_simple_dosage_with_interval(self, the_dose):
        dosage_time_range = self.soup.new_tag('dosageTimeRange')
        dosage_time_range.append(self.create_single_node_date('start', the_dose.start))
        dosage_time_range.append(self.create_single_node_date('end', the_dose.end))

        if isinstance(the_dose.dosage, SingleDoseAtTimeList):
            singleDoseListTag = self.soup.new_tag('singleDoseAtTimeList')
            for singleDose in the_dose.dosage.doseList:
                singleDoseTag = self.soup.new_tag('singleDoseAtTime')
                singleDoseTag.append(self.create_single_node_date('doseDate',
                                                                  singleDose.doseDate))
                doseTag = self.soup.new_tag('dose')
                doseTag.append(self.create_single_node_double('value',
                                                              singleDose.doseValue))
                doseTag.append(self.create_single_node_double('infusionTimeInMinutes',
                                                              singleDose.infusionTime))
                doseTag.append(self.create_single_node_double('unit',
                                                              singleDose.doseUnit))
                singleDoseTag.append(doseTag)
                formulation_and_route = self.soup.new_tag('formulationAndRoute')
                formulation_and_route.append(
                    self.create_single_node('formulation',
                                            singleDose.formulationAndRoute.formulation)
                )
                formulation_and_route.append(
                    self.create_single_node('administrationName',
                                            singleDose.formulationAndRoute.administrationName)
                )
                formulation_and_route.append(
                    self.create_single_node('administrationRoute',
                                            singleDose.formulationAndRoute.administrationRoute)
                )
                singleDoseTag.append(formulation_and_route)
                singleDoseListTag.append(singleDoseTag)
            dosage = self.soup.new_tag('dosage')
            dosage.append(singleDoseListTag)
            dosage_time_range.append(dosage)

        elif isinstance(the_dose.dosage, SimpleDoseList):
            simpleDoseListTag = self.soup.new_tag('simpleDoseList')
            simpleDoseListTag.append(self.create_single_node_double('unit',
                                                                    the_dose.dosage.doseUnit))
            formulation_and_route = self.soup.new_tag('formulationAndRoute')
            formulation_and_route.append(
                self.create_single_node('formulation',
                                        the_dose.dosage.formulationAndRoute.formulation)
            )
            formulation_and_route.append(
                self.create_single_node('administrationName',
                                        the_dose.dosage.formulationAndRoute.administrationName)
            )
            formulation_and_route.append(
                self.create_single_node('administrationRoute',
                                        the_dose.dosage.formulationAndRoute.administrationRoute)
            )
            simpleDoseListTag.append(formulation_and_route)

            doseListTag = self.soup.new_tag('doseList')
            for doseDateValue in the_dose.dosage.doseDateValues:
                doseDateValueTag = self.soup.new_tag('doseDateValue')
                doseDateValueTag.append(self.create_single_node_date('doseDate',
                                                                     doseDateValue[0]))
                doseDateValueTag.append(self.create_single_node_double('infusionTimeInMinutes',
                                                                       doseDateValue[1]))
                doseDateValueTag.append(self.create_single_node_double('value',
                                                                       doseDateValue[2]))
                doseListTag.append(doseDateValueTag)
            simpleDoseListTag.append(doseListTag)
            dosage = self.soup.new_tag('dosage')
            dosage.append(simpleDoseListTag)
            dosage_time_range.append(dosage)

        else:
            lasting_dosage = self.soup.new_tag('lastingDosage')
            tag_interval = self.soup.new_tag('interval')
            tag_interval.string = timedelta_to_str(the_dose.dosage.interval)
            lasting_dosage.append(tag_interval)
            dose = self.soup.new_tag('dose')
            dose.append(self.create_single_node_double('value', the_dose.dosage.dose.value))
            dose.append(self.create_single_node_double('unit', the_dose.dosage.dose.unit))
            # Todo : manage units for this
            dose.append(self.create_single_node_double('infusionTimeInMinutes',
                                                       the_dose.dosage.dose.get_infusion_time_in_minutes()))
            lasting_dosage.append(dose)

            formulation_and_route = self.soup.new_tag('formulationAndRoute')
            formulation_and_route.append(self.create_single_node('formulation',
                                                                 the_dose.dosage.formulationAndRoute.formulation))
            formulation_and_route.append(self.create_single_node('administrationName',
                                                                 the_dose.dosage.formulationAndRoute.administrationName))
            formulation_and_route.append(self.create_single_node('administrationRoute',
                                                                 the_dose.dosage.formulationAndRoute.administrationRoute))
            lasting_dosage.append(formulation_and_route)

            dosage_loop = self.soup.new_tag('dosageLoop')
            dosage_loop.append(lasting_dosage)
            dosage = self.soup.new_tag('dosage')
            dosage.append(dosage_loop)
            dosage_time_range.append(dosage)

        return dosage_time_range
