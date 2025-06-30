#!/usr/bin/python3

from datetime import datetime
from enum import Enum
from typing import List
from abc import ABC
from colorama import Back

from ..tucuxi.utils import str_to_time, str_to_datetime, evaluate_boolean

class XpertRequest:

    drugId: str
    drugModelId: str
    adjDate: str
    output: dict
    adjustmentDate: dict
    options: dict


    def __init__(self, drug_id='', drug_model_id='', adj_date='',
                 loadOption='loadingDoseAllowed',
                 restOption= 'noRestPeriod',
                 targetOption='definitionIfNoIndividualTarget',
                 formulation='lastFormulationAndRoute'):
        self.drugId = drug_id
        self.drugModelId = drug_model_id
        self.output = {"format": "html", "language": "en"}
        self.adjustmentDate = adj_date
        self.options = {"loadingOption": loadOption,
                        "restPeriodOption": restOption,
                        "targetExtractionOption": targetOption,
                        "formulationAndRouteSelectionOption": formulation}

    @staticmethod
    def create_from_soup(soup):
        drug_id = soup.drugId.string
        drug_model_id = soup.drugModelId.string
        adjustmentDate = sout.adjustmentDate.string
        return XpertRequest(drug_id, drug_model_id, adjustmentDate)
