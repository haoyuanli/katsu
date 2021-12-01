import uuid
import os
import json

from rest_framework import status
from django.test import APITestCase

from chord_metadata_service.chord.data_types import DATA_TYPE_PHENOPACKET, DATA_TYPE_MCODEPACKET
from chord_metadata_service.chord.models import Project, Dataset, TableOwnership, Table
from chord_metadata_service.patients.models import Individual
# noinspection PyProtectedMember
from chord_metadata_service.chord.ingest import (
    WORKFLOW_INGEST_FUNCTION_MAP,
    WORKFLOW_MCODE_FHIR_JSON,
    WORKFLOW_MCODE_JSON
)
from chord_metadata_service.chord.tests.constants import VALID_DATA_USE_1

from ..parse_fhir_mcode import parse_bundle, patient_to_individual
from ..models import MCodePacket, CancerCondition, MedicationStatement, CancerRelatedProcedure


with open(os.path.join(os.path.dirname(__file__), "example_mcode_fhir.json"), "r") as pf:
    EXAMPLE_INGEST_MCODE_FHIR = json.load(pf)

EXAMPLE_INGEST_OUTPUTS = {
    "json_document": os.path.join(os.path.dirname(__file__), "example_mcode_fhir.json"),
}

EXAMPLE_INGEST_OUTPUTS_MCODE_JSON = {
    "json_document": os.path.join(os.path.dirname(__file__), "example_mcode_json.json"),
}


class McodeApiTest(APITestCase):

    def setUp(self) -> None:
        p = Project.objects.create(title="Project 1", description="")
        self.d = Dataset.objects.create(title="Dataset 1", description="Some dataset", data_use=VALID_DATA_USE_1,
                                        project=p)
        # TODO: Real service ID
        to = TableOwnership.objects.create(table_id=uuid.uuid4(), service_id=uuid.uuid4(), service_artifact="metadata",
                                           dataset=self.d)
        self.t = Table.objects.create(ownership_record=to, name="Table 1", data_type=DATA_TYPE_PHENOPACKET)

        WORKFLOW_INGEST_FUNCTION_MAP[WORKFLOW_MCODE_JSON](EXAMPLE_INGEST_OUTPUTS_MCODE_JSON, self.t.identifier)

    def test_get_mcodepackets(self):
        """
        Test that we can get a list of mcodepackets without a dataset title
        """
        response = self.client.get('/api/mcodepackets')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data["results"]), 1)

    def test_get_mcodepackets_with_valid_dataset(self):
        """
        Test that we can get a list of mcodepackets with valid dataset titles
        """
        response = self.client.get('/api/mcodepackets?datasets=Dataset+1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data["results"]), 1)

    def test_get_mcodepackets_with_invalid_dataset(self):
        """
        Test that we cannot get mcodepackets with invalid dataset titles
        """
        response = self.client.get('/api/mcodepackets?datasets=notADataset')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data["results"]), 0)
