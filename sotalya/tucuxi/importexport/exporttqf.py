#!/usr/bin/python3


import os
from bs4 import BeautifulSoup
import xml.dom.minidom
from ..data.query import *

from ..data.requests import *
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
        print('create a TQF exporter')
        self.soup = None


    def export_to_string(self, query: Query, template_filename: str = ''):
        print('exporting a TQF')

        if template_filename == '':
            content = tqf_template
        else:
            content = open(template_filename).read()

        self.soup = BeautifulSoup(content, 'xml')

        self.soup.query.queryId.string = query.queryId
        self.soup.query.clientId.string = query.patientId
        self.soup.query.date.string = str(query.date)

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
        computing_option.append(self.create_single_node('parametersType', request.computingOption.parametersType.value))
        computing_option.append(self.create_single_node('compartmentOption',
                                                        request.computingOption.compartmentOption.value))
        computing_option.append(
            self.create_single_boolean_node('retrieveStatistics', request.computingOption.retrieveStatistics))
        computing_option.append(
            self.create_single_boolean_node('retrieveParameters', request.computingOption.retrieveParameters))
        computing_option.append(
            self.create_single_boolean_node('retrieveCovariates', request.computingOption.retrieveCovariates))
        return computing_option

    def create_options(self, request):
        options = self.soup.new_tag('options')
        options.append(self.create_single_node('bestCandidatesOption', request.options.bestCandidatesOption.value))
        options.append(self.create_single_node('loadingOption', request.options.loadingOption.value))
        options.append(self.create_single_node('restPeriodOption', request.options.restPeriodOption.value))
        options.append(self.create_single_node('steadyStateTargetOption',
                                               request.options.steadyStateTargetOption.value))
        options.append(self.create_single_node('targetExtractionOption', request.options.targetExtractionOption.value))
        options.append(self.create_single_node(
            'formulationAndRouteSelectionOption', request.options.formulationAndRouteSelectionOption.value))
        return options

    def create_percentile_ranks_type(self, request: PercentilesTraits):
        ranks = self.soup.new_tag('ranks')
        for percentile in request.ranks:
            ranks.append(self.create_single_node('rank', str(percentile)))
        return ranks

    def create_date_interval(self, request):
        date_interval = self.soup.new_tag('dateInterval')
        date_interval.append(self.create_single_node_date('start', request.dateInterval.startDate))
        date_interval.append(self.create_single_node_date('end', request.dateInterval.endDate))

        return date_interval

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

        lasting_dosage = self.soup.new_tag('lastingDosage')
        tag_interval = self.soup.new_tag('interval')
        tag_interval.string = timedelta_to_str(the_dose.dosage.interval)
        lasting_dosage.append(tag_interval)
        dose = self.soup.new_tag('dose')
        dose.append(self.create_single_node_double('value', the_dose.dosage.dose.value))
        dose.append(self.create_single_node_double('unit', the_dose.dosage.dose.unit))
        # Todo : manage units for this
        dose.append(self.create_single_node_double('infusionTimeInMinutes', the_dose.dosage.dose.get_infusion_time_in_minutes()))
        lasting_dosage.append(dose)

        formulation_and_route = self.soup.new_tag('formulationAndRoute')
        formulation_and_route.append(self.create_single_node('formulation', the_dose.dosage.formulationAndRoute.formulation))
        formulation_and_route.append(self.create_single_node('administrationName',
                                                             the_dose.dosage.formulationAndRoute.administrationName))
        formulation_and_route.append(self.create_single_node('administrationRoute',
                                                             the_dose.dosage.formulationAndRoute.administrationRoute))
        formulation_and_route.append(self.create_single_node('absorptionModel',
                                                             the_dose.dosage.formulationAndRoute.absorptionModel))
        lasting_dosage.append(formulation_and_route)

        dosage_loop = self.soup.new_tag('dosageLoop')
        dosage_loop.append(lasting_dosage)
        dosage = self.soup.new_tag('dosage')
        dosage.append(dosage_loop)
        dosage_time_range.append(dosage)
        return dosage_time_range
