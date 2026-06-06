# Module 4: Clinical Entity Extraction

This module demonstrates advanced few-shot prompting techniques to extract structured entities from unstructured practitioner encounter logs.

## Contents
* `medical_notes_extraction.ipynb`: Instructs LLMs (Llama 3.1 & 3.2 family) to parse patient notes and isolate:
  - Conditions (Diagnoses/Symptoms)
  - Interventions (Medications/Treatments/Placebos)
  
It outputs structured raw JSON strings without transferring clinical data out of Snowflake.
