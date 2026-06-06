# Module 1: Data Preparation & Transcription Analysis

This module walks through setting up the initial Snowflake database environment and loading customer call transcripts.

## Contents
* `call_transcript_analysis.ipynb`: A Snowflake Notebook showing how to set up databases, schemas, stages, copy datasets from S3, and run basic Cortex Complete queries.

## Snowflake Setup
This notebook executes the following actions:
1. Creates an active warehouse `ski_gear_s`.
2. Creates the database `ski_gear_support_db` and schema `ski_gear_support_schema`.
3. Defines a CSV file format and references a public S3 bucket with sample transcripts.
4. Populates the `CALL_TRANSCRIPTS` table via the `COPY INTO` command.
5. Performs pilot testing of Snowflake Cortex's native LLM capabilities.
