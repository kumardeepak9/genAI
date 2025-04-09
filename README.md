# Generative AI with Snowflake 

This module is part of a larger project demonstrating how to build ''AI-powered applications'' using Snowflake’s Snowpark and Cortex APIs. It highlights real-world use cases such as call transcript summarization, support ticket response generation, and fine-tuning LLMs for domain-specific tasks.

The repository is organized into multiple modules, each showcasing a different aspect of integrating Generative AI with the Snowflake Data Cloud. This particular module focuses on applying these capabilities within an interactive Streamlit application.


##  Overview

This module demonstrates:

- Integration of LLMs like Mistral and Llama using Snowflake Cortex APIs.
- Use of Snowpark for processing and transforming structured/unstructured data.
- A Streamlit-based interface for interacting with various AI tasks.
- Examples of custom prompt engineering and pipeline automation.
- Support for domain adaptation and fine-tuning** of language models.


##  Features

-  Call Transcript Analysis: Summarize transcripts into structured JSON objects.
-  LLM-Powered Tasks: Perform text completion, sentiment analysis, and translation via Cortex.
-  Fine-Tuning: Customize LLMs (e.g. Mistral-7B) for domain-specific workflows.
-  Support Ticket Automation: Generate smart, context-aware responses for customer service.
-  Streamlit App: Interactive UI for testing summarization, translation, and feedback generation.


##  Project Structure

module-3/ │ ├── app.py # Streamlit app entry point ├── requirements.txt # Python dependencies ├── utils/ # Utility functions for data handling and prompt building ├── prompts/ # Sample prompt templates for different tasks └── README.md # This file

## Setup Instructions

## Prerequisite

- Python 3.8 or higher
- [Snowflake](https://signup.snowflake.com/) account with Snowpark and Cortex enabled
- `conda` or `venv` for virtual environment management

### Installation Steps

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Configure your environment
      OPENAI_API_KEY=your-openai-key
      SNOWFLAKE_ACCOUNT=your-account-id
      SNOWFLAKE_USER=your-username
      SNOWFLAKE_PASSWORD=your-password
      SNOWFLAKE_WAREHOUSE=your-warehouse
      SNOWFLAKE_DATABASE=your-database
      SNOWFLAKE_SCHEMA=your-schema
5. Streamlit run app.py