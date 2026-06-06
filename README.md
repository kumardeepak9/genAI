# Generative AI with Snowflake: Quickstart Workspace

This repository showcases how to design, build, and deploy Generative AI applications directly within the **Snowflake Data Cloud** using **Snowpark Python** and **Cortex LLM Services**. 

It serves as a professional reference implementation for extracting business value from unstructured call transcripts, support tickets, and medical logs, as well as running custom LLM fine-tuning pipelines.

---

## Project Structure

```
genAI/
├── .env.template               
├── .gitignore                 
├── README.md                  
├── requirements.txt            
├── common/                     
│   ├── __init__.py
│   └── connection.py           
├── 01_data_preparation/        
│   ├── README.md
│   └── call_transcript_analysis.ipynb
├── 02_cortex_llm_basics/      
│   ├── README.md
│   ├── intro_to_LLM_functions.ipynb
│   └── using_LLM_functions.ipynb
├── 03_llm_fine_tuning/       
│   ├── README.md
│   ├── load_support_tickets.ipynb
│   └── finetuning_mistral_7b.ipynb
├── 04_additional_demos/       
│   ├── README.md
│   └── medical_notes_extraction.ipynb
└── streamlit_dashboard/        
    ├── app.py               
    ├── styles.py              
    └── pages/                  
        ├── 1_📊_transcript_analytics.py
        ├── 2_🎫_ticket_automation.py
        └── 3_🏥_medical_extraction.py
```

---

## Local Development Setup

Follow these steps to run and debug the workspace and Streamlit applications locally.

### 1. Prerequisites
- **Python 3.8 to 3.11** installed.
- A **Snowflake Account** with permissions to create databases, stages, warehouses, and invoke Cortex services (typically requires `ACCOUNTADMIN` or equivalent role during initialization).

### 2. Set Up Virtual Environment
Create a clean environment using Python's native `venv` or `conda`:

```bash
# Using venv
python3 -m venv venv
source venv/bin/activate

# Or using Conda
conda create -n snowflake-genai python=3.10
conda activate snowflake-genai
```

### 3. Install Dependencies
Install the required packages using the unified `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure Local Environment Credentials
The code utilizes a smart connection utility that reads environment parameters to establish a secure local session:
1. Duplicate the template file:
   ```bash
   cp .env.template .env
   ```
2. Open the `.env` file and insert your Snowflake account credentials and target compute/resource parameters.

---

## Running the Streamlit Dashboard

Launch the unified dashboard from the root directory:

```bash
streamlit run streamlit_dashboard/app.py
```

This starts a local web server (usually at `http://localhost:8501`) presenting the premium multi-page interface:
- **Connection Registry**: Real-time status display of your Snowflake connection.
- **Transcript Analytics**: Tabbed views for JSON summarization, translation, and sentiment score analysis.
- **Ticket Automation**: Custom dropdown sample selectors to test zero-shot classification and auto-drafting email/text messages using various LLM architectures.
- **Medical Extraction**: Few-shot schema extractor that transforms physician encounter texts into clean, interactive tables of diagnoses and prescriptions.

---

## Running inside Snowflake (Streamlit in Snowflake - SiS)

The code in `common/connection.py` automatically checks if an active session exists in the execution context:
- If deployed inside **Snowflake** (e.g. as a Streamlit in Snowflake App), it uses the zero-config context session: `get_active_session()`.
- If run **locally**, it securely reads your `.env` parameters to initialize the Snowpark connection.

This enables you to use the exact same code files for both local development/debugging and production cloud deployments.
