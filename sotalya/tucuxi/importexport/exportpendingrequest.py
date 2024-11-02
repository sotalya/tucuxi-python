#!/usr/bin/python3


import os
from bs4 import BeautifulSoup
import copy
import xml.dom.minidom
from ..tucuxi.utils import timedelta_to_str


list_template = '''<?xml version="1.0"?>
<data xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" controlId="1234" errorCondition="OK" lang="fr" type="reply_list" version="0.2" xsi:noNamespaceSchemaLocation="eep.xsd">
  <request>
    <requestId></requestId>
    <requestState></requestState>
    <patient>
      <name>
        <firstName></firstName>
        <middleName/>
        <lastName></lastName>
      </name>
      <institute>
        <instituteId/>
        <name/>
      </institute>
      <patientId></patientId>
      <stayNumber></stayNumber>
      <birthdate></birthdate>
      <gender></gender>
      <comments/>
    </patient>
    <mandator>
      <name>
        <firstName/>
        <middleName/>
        <lastName/>
      </name>
      <contact>
        <address/>
        <city/>
        <postcode/>
        <state/>
        <country/>
        <emails>
          <email type=""/>
        </emails>
        <phones>
          <phone type=""/>
        </phones>
      </contact>
      <institute>
        <instituteId/>
        <name/>
        <contact>
          <address/>
          <city/>
          <postcode/>
          <state/>
          <country/>
          <emails>
          </emails>
          <phones>
          </phones>
        </contact>
      </institute>
      <practicianId/>
      <title/>
      <birthdate/>
      <gender/>
      <comments/>
    </mandator>
    <sample>
      <id></id>
      <sampleDate></sampleDate>
      <arrivalDate></arrivalDate>
      <concentrations>
        <concentration>
          <analyte></analyte>
          <value></value>
          <unit></unit>
        </concentration>
      </concentrations>
      <comments/>
    </sample>
    <drug>
      <drugId></drugId>
      <atc/>
      <brandName></brandName>
      <activePrinciple></activePrinciple>
      <comments/>
    </drug>
  </request>
</data>
'''

pending_request_template = '''<?xml version="1.0"?>
<data xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" controlId="cId" errorCondition="OK" lang="FRA" type="reply_request" version="0.2" xsi:noNamespaceSchemaLocation="eep.xsd">
  <dataset>
    <requestId></requestId>
    <requestState></requestState>
    <drug>
      <drugId></drugId>
      <atc/>
      <brandName></brandName>
      <activePrinciple></activePrinciple>
      <comments/>
    </drug>
    <dosages>
    </dosages>
    <samples>
    </samples>
    <covariates>
    </covariates>
    <clinicals>
    </clinicals>
    <patient>
      <name>
        <firstName></firstName>
        <middleName/>
        <lastName></lastName>
      </name>
      <contact>
        <address/>
        <city/>
        <postcode/>
        <state/>
        <country/>
        <emails>
        </emails>
        <phones>
        </phones>
      </contact>
      <institute>
        <instituteId/>
        <name/>
        <contact>
          <address/>
          <city/>
          <postcode/>
          <state/>
          <country/>
          <emails>
          </emails>
          <phones>
          </phones>
        </contact>
      </institute>
      <patientId></patientId>
      <stayNumber></stayNumber>
      <birthdate></birthdate>
      <gender></gender>
      <comments/>
    </patient>
    <mandator>
      <name>
        <firstName/>
        <middleName/>
        <lastName/>
      </name>
      <contact>
        <address/>
        <city/>
        <postcode/>
        <state/>
        <country/>
        <emails>
          <email type=""/>
        </emails>
        <phones>
          <phone type=""/>
        </phones>
      </contact>
      <institute>
        <instituteId/>
        <name/>
        <contact>
          <address/>
          <city/>
          <postcode/>
          <state/>
          <country/>
          <emails>
          </emails>
          <phones>
          </phones>
        </contact>
      </institute>
      <practicianId/>
      <title/>
      <birthdate/>
      <gender/>
      <comments/>
    </mandator>
  </dataset>
</data>
'''

class ExportPendingRequest:
    def __init__(self):
        print('create a Pending request exporter')
        self.soup = None

    def create_single_node(self, tag_name, tag_value):
        node = self.soup.new_tag(tag_name)
        node.string = tag_value
        return node

    def create_single_node_double(self, tag_name, tag_value):
        node = self.soup.new_tag(tag_name)
        node.string = str(tag_value)
        return node

    def create_single_node_interval(self, tag_name, tag_value):
        node = self.soup.new_tag(tag_name)
        node.string = timedelta_to_str(tag_value)
        return node

    def create_single_node_date(self, tag_name, tag_value):
        node = self.soup.new_tag(tag_name)
        node.string = tag_value.strftime("%Y-%m-%dT%H:%M:%S")
        return node

    def export_list_to_file(self, pending_requests, filename, template_filename:str = ''):

        """
        Export a list of pending requests in XML format.

        :param PendingRequest() pending_requests: The pending requests to export
        :param str filename: The path to the output file
        :param str template_filename: The path to the template file
        """

        print('exporting the list of pending requests')

        if template_filename == '':
            content = list_template
        else:
            content = open(template_filename).read()

        self.soup = BeautifulSoup(content, 'xml')

        requestNode = self.soup.data.request

        firstIteration = True
        for pending_request in pending_requests:
            if not firstIteration:
                node = copy.copy(requestNode)
                requestNode.insert_after(node)
            firstIteration = False

            requestNode.requestId.string = pending_request.requestId
            requestNode.requestState.string = pending_request.requestState

            requestNode.patient.find('name').firstName.string = pending_request.patient.firstname
            requestNode.patient.find('name').lastName.string = pending_request.patient.lastname
            requestNode.patient.patientId.string = pending_request.patient.patientId
            requestNode.patient.stayNumber.string = 'stayNumber'

            drug_treatment = pending_request.drugTreatment

            for covariate in drug_treatment.patientCovariates:
                if covariate.covariateId == 'birthdate':
                    requestNode.patient.birthdate.string = covariate.value
                    continue
                if covariate.covariateId == 'sex':
                    if covariate.value == '1':
                        requestNode.patient.gender.string = 'male'
                    else:
                        requestNode.patient.gender.string = 'female'
                    continue

            if (requestNode.find("sample") is not None):
                requestNode.sample.decompose()
            if (len(drug_treatment.samples) > 0):
                samp = self.create_sample(drug_treatment.samples[0])
                requestNode.mandator.insert_after(samp)

            requestNode.drug.drugId.string = pending_request.drugTreatment.drugId
            requestNode.drug.brandName.string = 'manque'
            requestNode.drug.activePrinciple.string = pending_request.drugTreatment.activePrinciple

        xmlout = str(self.soup)

        xml1 = xml.dom.minidom.parseString(xmlout)
        outputstring = xml1.toprettyxml()
        dom_string = os.linesep.join([s for s in outputstring.splitlines() if s.strip()])

        outputfile = open(filename, 'w')
        outputfile.write(dom_string)
        outputfile.close()
        return True

    def export_to_file(self, pending_request, filename, template_filename:str = ''):

        """
        Export a pending request in XML format.

        :param PendingRequest pending_request: The pending request to export
        :param str filename: The path to the output file
        :param str template_filename: The path to the template file
        """

        print('exporting a pending request')

        if template_filename == '':
            conent = pending_request_template
        else:
            content = open(template_filename).read()

        self.soup = BeautifulSoup(content, 'xml')

        self.soup.data.dataset.requestId.string = pending_request.requestId
        self.soup.data.dataset.requestState.string = pending_request.requestState
        self.soup.data.dataset.drug.drugId.string = pending_request.drugTreatment.drugId
        self.soup.data.dataset.drug.brandName.string = 'manque'
        self.soup.data.dataset.drug.activePrinciple.string = pending_request.drugTreatment.activePrinciple

        drug_treatment = pending_request.drugTreatment

        for dtr in drug_treatment.dosages:
            d = self.create_dosage(dtr)
            self.soup.data.dataset.dosages.append(d)

        for sample in drug_treatment.samples:
            samp = self.create_sample(sample)
            self.soup.data.dataset.samples.append(samp)

        for covariate in drug_treatment.patientCovariates:
            if covariate.covariateId == 'birthdate':
                self.soup.data.dataset.patient.birthdate.string = covariate.value
                continue
            if covariate.covariateId == 'sex':
                if covariate.value == '1':
                    self.soup.data.dataset.patient.gender.string = 'male'
                else:
                    self.soup.data.dataset.patient.gender.string = 'female'
                continue
            cov = self.create_covariate(covariate)
            self.soup.data.dataset.covariates.append(cov)

        for clinical in pending_request.clinicals:
            c = self.create_clinical(clinical)
            self.soup.data.dataset.clinicals.append(c)

        self.soup.data.dataset.patient.find("name").firstName.string = pending_request.patient.firstname
        self.soup.data.dataset.patient.find("name").lastName.string = pending_request.patient.lastname
        self.soup.data.dataset.patient.patientId.string = pending_request.patient.patientId
        self.soup.data.dataset.patient.stayNumber.string = 'stayNumber'

        xmlout = str(self.soup)

        xml1 = xml.dom.minidom.parseString(xmlout)
        outputstring = xml1.toprettyxml()
        dom_string = os.linesep.join([s for s in outputstring.splitlines() if s.strip()])

        outputfile = open(filename, 'w')
        outputfile.write(dom_string)
        outputfile.close()

        return True

    def create_comments(self, comments):
        com = self.soup.new_tag('comments')
        for c in comments:
            com.append(self.create_single_node('comment', c))
        return com

    def create_clinical(self, clinical):
        cl = self.soup.new_tag('clinical')
        cl.append(self.create_single_node('name', clinical.name))
        cl.append(self.create_single_node_date('date', clinical.date))
        cl.append(self.create_single_node('value', clinical.value))
        cl.append(self.create_comments(clinical.comments))
        return cl

    def create_covariate(self, covariate):
        cov = self.soup.new_tag('covariate')
        cov.append(self.create_single_node('name', covariate.covariateId))
        cov.append(self.create_single_node_date('date', covariate.date))

        value = self.soup.new_tag('value')
        cov.append(value)

        value.append(self.create_single_node('value', covariate.value))
        value.append(self.create_single_node('unit', covariate.unit))

        #cov.append(self.create_single_node('dataType', covariate.dataType))
        cov.append(self.create_single_node('nature', covariate.nature))
        cov.append(self.soup.new_tag('comments'))
        return cov

    def create_sample(self, sample):
        sam = self.soup.new_tag('sample')
        sam.append(self.create_single_node('id', sample.id))
        sam.append(self.create_single_node_date('sampleDate', sample.sampledate))

        if hasattr(sample, 'arrivaldate'):
            sam.append(self.create_single_node_date('arrivalDate', sample.arrivaldate))
        else:
            sam.append(self.create_single_node_date('arrivalDate', sample.sampledate))

        conc = self.soup.new_tag('concentrations')
        sam.append(conc)

        c = self.soup.new_tag('concentration')
        conc.append(c)

        c.append(self.create_single_node('analyte', sample.analyteId))
        c.append(self.create_single_node_double('value', sample.concentration))
        c.append(self.create_single_node('unit', sample.unit))

        sam.append(self.soup.new_tag('comments'))

        return sam

    def create_dosage(self, the_dose):

        dosage = self.soup.new_tag('dosage')
        dosage.append(self.create_single_node_date('startDate', the_dose.startDate))
        dosage.append(self.create_single_node_date('lastDate', the_dose.endDate))

        dose = self.soup.new_tag('dose')
        dose.append(self.create_single_node_double('value', the_dose.dose.doseValue))
        dose.append(self.create_single_node_double('unit', the_dose.dose.doseUnit))
        dosage.append(dose)

        tag_interval = self.soup.new_tag('interval')
        tag_interval.append(self.create_single_node_interval('value', the_dose.interval))
        dosage.append(tag_interval)

        infusion = self.soup.new_tag('infusion')
        infusion.append(self.create_single_node_double('value', the_dose.dose.infusionTime))
        infusion.append(self.create_single_node_double('unit', 'min'))
        dosage.append(infusion)

        dosage.append(self.create_single_node('intake', the_dose.dose.administrationRoute))

        dosage.append(self.soup.new_tag('comments'))

        return dosage
