# Most parts of this text are taken from the mCODE:Minimal Common Oncology Data Elements Data Dictionary.
# The mCODE is made available under the Creative Commons 0 "No Rights Reserved" license
# https://creativecommons.org/share-your-work/public-domain/cc0/

# Portions of this text copyright (c) 2019-2020 the Canadian Centre for Computational Genomics; licensed under the
# GNU Lesser General Public License version 3.

from chord_metadata_service.restapi.description_utils import EXTRA_PROPERTIES


GENOMICS_REPORT = {
    "description": "Genetic Analysis Summary.",
    "properties": {
        "id": "An arbitrary identifier for the genetics report.",
        "code": "An ontology or controlled vocabulary term to identify the laboratory test. "
                     "Accepted value sets: LOINC, GTR.",
        "performing_organization_name": "The name of the organization  producing the genomics report.",
        "issued": "The date/time this report was issued.",
        **EXTRA_PROPERTIES
    }
}

LABS_VITAL = {
    "description": "A description of tests performed on patient.",
    "properties": {
        "id": "An arbitrary identifier for the labs/vital tests.",
        "individual": "The individual who is the subject of the tests.",
        "body_height": "The patient\'s height.",
        "body_weight": "The patient\'s weight.",
        "cbc_with_auto_differential_panel": "Reference to a laboratory observation in the CBC with Auto Differential"
                                            "Panel test.",
        "comprehensive_metabolic_2000": "Reference to a laboratory observation in the CMP 2000 test.",
        "blood_pressure_diastolic": "The blood pressure after the contraction of the heart while the chambers of "
                                    "the heart refill with blood, when the pressure is lowest.",
        "blood_pressure_systolic": "The blood pressure during the contraction of the left ventricle of the heart, "
                                   "when blood pressure is at its highest.",
        "tumor_marker_test": "An ontology or controlled vocabulary term to identify tumor marker test.",
        **EXTRA_PROPERTIES
    }
}

CANCER_CONDITION = {
    "description": "A description of history of primary or secondary cancer conditions.",
    "properties": {
        "id": "An arbitrary identifier for the cancer condition.",
        "condition_type": "Cancer condition type: primary or secondary.",
        "body_site": "Code for the body location, optionally pre-coordinating laterality or direction. "
                              "Accepted ontologies: SNOMED CT, ICD-O-3 and others.",
        "laterality": "Body side of the body location, if needed to distinguish from a similar location "
                      "on the other side of the body.",
        "clinical_status": "A flag indicating whether the condition is active or inactive, recurring, in remission, "
                           "or resolved (as of the last update of the Condition). Accepted code system: "
                           "http://terminology.hl7.org/CodeSystem/condition-clinical",
        "code": "A code describing the type of primary or secondary malignant neoplastic disease.",
        "date_of_diagnosis": "The date the disease was first clinically recognized with sufficient certainty, "
                             "regardless of whether it was fully characterized at that time.",
        "histology_morphology_behavior": "A description of the morphologic and behavioral characteristics of "
                                         "the cancer. Accepted ontologies: SNOMED CT, ICD-O-3 and others.",
        "verification_status": "A flag indicating whether the condition is unconfirmed, provisional, differential, "
                               "confirmed, refuted, or entered-in-error.",
        **EXTRA_PROPERTIES
    }
}

TNM_STAGING = {
    "description": "A description of the cancer spread in a patient's body.",
    "properties": {
        "id": "An arbitrary identifier for the TNM staging.",
        "tnm_type": "TNM type: clinical or pathological.",
        "stage_group": "The extent of the cancer in the body, according to the TNM classification system."
                       "Accepted ontologies: SNOMED CT, AJCC and others.",
        "primary_tumor_category": "Category of the primary tumor, based on its size and extent. "
                                  "Accepted ontologies: SNOMED CT, AJCC and others.",
        "regional_nodes_category": "Category of the presence or absence of metastases in regional lymph nodes. "
                                   "Accepted ontologies: SNOMED CT, AJCC and others.",
        "distant_metastases_category": "Category describing the presence or absence of metastases in remote "
                                       "anatomical locations. Accepted ontologies: SNOMED CT, AJCC and others.",
        "cancer_condition": "Cancer condition.",
        **EXTRA_PROPERTIES
    }
}

CANCER_RELATED_PROCEDURE = {
    "description": "Description of radiological treatment or surgical action addressing a cancer condition.",
    "properties": {
        "id": "An arbitrary identifier for the procedure.",
        "procedure_type": "Type of cancer related procedure: radion or surgical.",
        "code": "Code for the procedure performed.",
        "occurence_time_or_period": "The date/time that a procedure was performed.",
        "target_body_site": "The body location(s) where the procedure was performed.",
        "treatment_intent": "The purpose of a treatment.",
        **EXTRA_PROPERTIES
    }
}

MEDICATION_STATEMENT = {
    "description": "Description of medication use.",
    "properties": {
        "id": "An arbitrary identifier for the medication statement.",
        "medication_code": "A code for medication. Accepted code systems: Medication Clinical Drug (RxNorm) and other.",
        "termination_reason": "A code explaining unplanned or premature termination of a course of medication. "
                              "Accepted ontologies: SNOMED CT.",
        "treatment_intent": "The purpose of a treatment. Accepted ontologies: SNOMED CT.",
        "start_date": "The start date/time of the medication.",
        "end_date": "The end date/time of the medication.",
        "date_time": "The date/time the medication was administered.",
        **EXTRA_PROPERTIES
    }
}

MCODEPACKET = {
    "description": "Collection of cancer related metadata.",
    "properties": {
        "id": "An arbitrary identifier for the mcodepacket.",
        "subject": "An individual who is a subject of mcodepacket.",
        "genomics_report": "A genomics report associated with an Individual.",
        "cancer_condition": "An Individual's cancer condition.",
        "cancer_related_procedures": "A radiological or surgical procedures addressing a cancer condition.",
        "medication_statement": "Medication treatment addressed to an Individual.",
        **EXTRA_PROPERTIES
    }
}
