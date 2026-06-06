# Module 3: Fine-Tuning LLMs on Snowflake

This module outlines the pipeline to extract, filter, format, split, and submit custom data to fine-tune a Mistral-7B model natively inside Snowflake Cortex.

## Contents
* `load_support_tickets.ipynb`: Loads telecom customer support tickets from S3 into a Snowflake table `SUPPORT_TICKETS`.
* `finetuning_mistral_7b.ipynb`: Step-by-step pipeline showing:
  1. Classifying support tickets using Cortex `classify_text`.
  2. Filtering high-quality instruction-response pairs based on length requirements.
  3. Formatting training data with prompt structures.
  4. Creating train and evaluation split tables.
  5. Initiating a native model fine-tuning job:
     ```sql
     select snowflake.cortex.finetune('CREATE', 'SUPPORT_MESSAGES_FINETUNED_MISTRAL_7B', ...)
     ```
  6. Inspecting job progress and executing inference.
