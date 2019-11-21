from chord_lib.search import build_search_response, postgres
from datetime import datetime
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Dataset
from chord_metadata_service.phenopackets.models import Phenopacket
from chord_metadata_service.phenopackets.schemas import PHENOPACKET_SCHEMA
from chord_metadata_service.phenopackets.serializers import PhenopacketSerializer

PHENOPACKET_DATA_TYPE_ID = "phenopacket"


@api_view(["GET"])
def data_type_list(_request):
    return Response([{"id": PHENOPACKET_DATA_TYPE_ID, "schema": PHENOPACKET_SCHEMA}])


@api_view(["GET"])
def dataset_list(request):
    if PHENOPACKET_DATA_TYPE_ID not in request.query_params.getlist("data-type"):
        # TODO: Better error
        return Response(status=404)

    return Response([{
        "id": d.dataset_id,
        "name": d.name,
        "metadata": {
            "description": d.description,
            "project_id": d.project_id,
            "created": d.created.isoformat(),
            "updated": d.updated.isoformat()
        },
        "schema": PHENOPACKET_SCHEMA
    } for d in Dataset.objects.all()])


@api_view(["DELETE"])
def dataset_detail(request, dataset_id):
    # TODO: Implement GET, POST
    try:
        dataset = Dataset.objects.get(dataset_id=dataset_id)
    except Dataset.DoesNotExist:
        # TODO: Better error
        return Response(status=404)

    if request.method == "DELETE":
        dataset.delete()
        return Response(status=204)


def search(request, internal_data=False):
    # TODO
    start = datetime.now()

    data_type = request.data["data_type"]
    query = request.data["query"]

    if data_type != PHENOPACKET_DATA_TYPE_ID:
        # TODO: Better error
        return Response(status=404)

    try:
        compiled_query, params = postgres.search_query_to_psycopg2_sql(query, PHENOPACKET_SCHEMA)
    except (SyntaxError, TypeError, ValueError):
        # TODO: Better error
        return Response(status=400)

    if not internal_data:
        def phenopacket_results():
            with connection.cursor() as cursor:
                cursor.execute(compiled_query.as_string(cursor.connection), params)
                return set(dict(zip([col[0] for col in cursor.description], row))["dataset_id"]
                           for row in cursor.fetchall())

        datasets = Dataset.objects.filter(dataset_id__in=phenopacket_results())  # TODO: Maybe can avoid hitting DB here
        return Response(build_search_response([{"id": d.dataset_id, "data_type": PHENOPACKET_DATA_TYPE_ID}
                                               for d in datasets], start))

    def phenopacket_results():
        with connection.cursor() as cursor:
            cursor.execute(compiled_query.as_string(cursor.connection), params)
            return set(dict(zip([col[0] for col in cursor.description], row))["phenopacket_id"]
                       for row in cursor.fetchall())

    phenopackets = Phenopacket.objects.filter(phenopacket_id__in=phenopacket_results())
    phenopackets_by_dataset = {}
    for p in phenopackets:
        if p.dataset_id not in phenopackets_by_dataset:
            phenopackets_by_dataset[p.dataset_id] = []

        serializer = PhenopacketSerializer(p)
        phenopackets_by_dataset[p.dataset_id].append(serializer.data)

    return Response(build_search_response({k: {"data_type": PHENOPACKET_DATA_TYPE_ID, "matches": v}
                                           for k, v in phenopackets_by_dataset.items()}, start))


@api_view(["POST"])
def chord_search(request):
    return search(request, internal_data=False)


@api_view(["POST"])
def chord_private_search(request):
    return search(request, internal_data=True)
