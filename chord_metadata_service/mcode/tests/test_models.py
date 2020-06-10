import datetime
from django.test import TestCase
from chord_metadata_service.patients.models import Individual
from ..models import *
from .constants import *
from rest_framework import serializers
from django.core.validators import ValidationError


class GenomicsReportTest(TestCase):
    """ Test module for Genomics Report model """

    def setUp(self):
        self.genomics_report = GenomicsReport.objects.create(**valid_genetic_report())

    def test_genomics_report(self):
        genomics_report = GenomicsReport.objects.get(id='genomics_report:01')
        self.assertEqual(genomics_report.code['id'], 'GTR000567625.2')


class LabsVitalTest(TestCase):
    """ Test module for LabsVital model """

    def setUp(self):
        self.individual = Individual.objects.create(**VALID_INDIVIDUAL)
        self.labs_vital = LabsVital.objects.create(**valid_labs_vital(self.individual))

    def test_labs_vital(self):
        labs_vital = LabsVital.objects.get(id='labs_vital:01')
        self.assertEqual(labs_vital.body_height['value'], 1.70)
        self.assertEqual(labs_vital.body_height['unit'], 'm')
        self.assertEqual(labs_vital.body_weight['value'], 60)
        self.assertEqual(labs_vital.blood_pressure_diastolic['value'], 80)
        self.assertEqual(labs_vital.blood_pressure_systolic['value'], 120)
        self.assertIsInstance(labs_vital.tumor_marker_test, dict)
        self.assertIsInstance(labs_vital.tumor_marker_test['code'], dict)
        self.assertEqual(labs_vital.tumor_marker_test['data_value']['value'], 10)

    def test_validation(self):
        invalid_obj = valid_labs_vital(self.individual)
        invalid_obj["id"] = "labs_vital:02"
        invalid_obj["tumor_marker_test"]["code"] = {
            "coding": [
                {
                    "code": "50610-5",
                    "display": "Alpha-1-Fetoprotein",
                    "system": "loinc.org"
                }
            ]
        }
        invalid = LabsVital.objects.create(**invalid_obj)
        with self.assertRaises(serializers.ValidationError):
            invalid.full_clean()


class CancerConditionTest(TestCase):
    """ Test module for CancerCondition model """

    def setUp(self):
        self.cancer_condition = CancerCondition.objects.create(**valid_cancer_condition())

    def test_cancer_condition(self):
        cancer_condition = CancerCondition.objects.get(id='cancer_condition:01')
        self.assertEqual(cancer_condition.condition_type, 'primary')
        self.assertIsInstance(cancer_condition.body_site, list)
        self.assertEqual(cancer_condition.body_site[0]['id'], '442083009')
        self.assertEqual(cancer_condition.clinical_status['id'], 'active')
        code_keys = [key for key in cancer_condition.code.keys()]
        self.assertEqual(code_keys, ['id', 'label'])
        self.assertEqual(cancer_condition.histology_morphology_behavior['id'], '372147008')


class TNMStagingTest(TestCase):
    """ Test module for TNMstaging model """

    # TODO URI syntax examples for tests https://tools.ietf.org/html/rfc3986

    def setUp(self):
        self.cancer_condition = CancerCondition.objects.create(**valid_cancer_condition())
        self.tnm_staging = TNMStaging.objects.create(**invalid_tnm_staging(self.cancer_condition))

    def test_tnm_staging(self):
        tnm_staging = TNMStaging.objects.get(id='tnm_staging:01')
        self.assertEqual(tnm_staging.tnm_type, 'clinical')
        # this should fails in validation below
        self.assertIsInstance(tnm_staging.stage_group['data_value']['coding'], list)

    def test_validation(self):
        invalid_obj = invalid_tnm_staging(self.cancer_condition)
        invalid_obj["id"] = "tnm_staging:02"
        invalid = TNMStaging.objects.create(**invalid_obj)
        with self.assertRaises(serializers.ValidationError):
            invalid.full_clean()


class CancerRelatedProcedureTest(TestCase):
    """ Test module for CancerRelatedProcedure model """

    def setUp(self):
        self.cancer_related_procedure = CancerRelatedProcedure.objects.create(
            **valid_cancer_related_procedure()
        )

    def test_cancer_related_procedure(self):
        cancer_related_procedure = CancerRelatedProcedure.objects.get(id='cancer_related_procedure:01')
        self.assertEqual(cancer_related_procedure.procedure_type, 'radiation')
        self.assertEqual(cancer_related_procedure.code['id'], '33356009')
        self.assertEqual(cancer_related_procedure.occurence_time_or_period['value']['start'], '2018-11-13T20:20:39+00:00')
        self.assertIsInstance(cancer_related_procedure.target_body_site, list)
        self.assertEqual(cancer_related_procedure.treatment_intent['label'], 'Curative - procedure intent')


class MedicationStatementTest(TestCase):
    """ Test module for MedicationStatement model """

    def setUp(self):
        self.cancer_related_procedure = MedicationStatement.objects.create(
            **valid_medication_statement()
        )

    def test_cancer_related_procedure(self):
        medication_statement = MedicationStatement.objects.get(id='medication_statement:01')
        self.assertEqual(medication_statement.medication_code['id'], '92052')
        self.assertIsInstance(medication_statement.termination_reason, list)
        self.assertEqual(medication_statement.treatment_intent['label'], 'Curative - procedure intent')
        for date in [medication_statement.start_date, medication_statement.end_date, medication_statement.date_time]:
            self.assertIsInstance(date, datetime.datetime)
