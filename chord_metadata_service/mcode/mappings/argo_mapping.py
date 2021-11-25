ARGO_MAPPING = {
    "individual": {
        "title": "Donor",
        "id": "submitter_donor_id",
        "deceased": "vital_status",
        "sex": "gender"
    },
    "genetic_specimen": {
        "title": "Specimen",
        "id": "submitter_specimen_id",
        "collection_body": "specimen_tissue_source",
        "specimen_type": "specimen_type",
        "laterality": "specimen_laterality",
        "extra_properties": [
            "sample_type"
        ]
    },
    "cancer_condition": {
        "title": "PrimaryDiagnosis",
        "id": "program_id",
        "condition_type": "primary",
        "body_site": "specimen_type",
        "laterality": "laterality",
        "clinical_status": "",
        "code": "cancer_type_code",
        "date_of_diagnosis": "age_at_diagnosis",
        "histology_morphology_behavior": "",
        "verification_status": "",
        "extra_properties": [
            "cancer_type_additional_information",
        ]
    },
}
