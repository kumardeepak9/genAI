import streamlit as st
import sys
import json
from pathlib import Path

# Add root directory to system path to enable shared module imports
root_dir = str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from common.connection import get_session
from streamlit_dashboard.styles import apply_custom_css

# Page Configuration
st.set_page_config(
    page_title="Medical Extraction | Snowflake GenAI",
    page_icon="🏥",
    layout="wide"
)

# Apply premium styles
apply_custom_css()

# Ensure we have active session
try:
    session = get_session()
except Exception as e:
    st.error("No active Snowflake connection. Please configure `.env` file or check Snowflake environment.")
    st.stop()

# Page Title
st.markdown('<div class="gradient-title">Clinical Entity Extraction</div>', unsafe_allow_html=True)
st.markdown("##### Extract clinical conditions and interventions from unstructured medical notes using Snowflake Cortex LLMs.")
st.markdown("---")

# Sample Medical Notes
SAMPLE_NOTES = """Patient Name: Barbara Anderson
Date of Visit: July 14, 2025
DOB: August 29, 1999

Chief Complaint:
Follow-up for proteinuria.

History of Present Illness:
29-year-old female with proteinuria (1.2 g/day) confirmed three months ago. He denies hematuria or dysuria. On Losartan potassium 50 mg daily for 6 weeks with partial improvement. Blood pressure remains mildly elevated.

Objective Data:
Vitals:
BP: 132/81 mmHg
HR: 72 bpm

Labs:
Urine protein ratio: 1.1 (improved from 1.5)
Serum creatinine: 1.1 mg/dL (stable)
Potassium: 4.8 mmol/L

Assessment:
Proteinuria: Likely hypertensive nephropathy, improving with Losartan.
Hypertension: Partially controlled.

Plan:
Continue Losartan Potassium 50 mg daily; consider dose increase if needed.
Initiate Comparator: Placebo (Losartan) for monitoring as part of trial.
Evaluate response to Amlodipine Besylate, Placebo (Amlodipine), and potential Enalapril Maleate if ARB response is insufficient.
Recheck labs in 6 weeks, including proteinuria and kidney function.
Provider's Name: Dr. Amanda Clarke"""

# Layout
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown('<div class="gradient-subtitle">Encounter Notes & Prompting</div>', unsafe_allow_html=True)
    
    medical_notes = st.text_area(
        "Physician Encounter Notes", 
        value=SAMPLE_NOTES,
        height=320,
        placeholder="Enter unstructured medical records or practitioner logs here..."
    )
    
    selected_llm = st.selectbox(
        "Select Cortex Model",
        ("llama3.1-405b", "llama3.2-3b", "llama3.2-1b"),
        index=0,
        help="Llama3.1-405b is recommended for complex reasoning and structured schema extraction."
    )
    
    run_extraction = st.button("Extract Entities 🧬", type="primary")

with col_right:
    st.markdown('<div class="gradient-subtitle">Structured Entities Output</div>', unsafe_allow_html=True)
    
    if run_extraction and medical_notes:
        cleaned_notes = medical_notes.replace("'", "\\'")
        
        # Build prompt that requests a strict JSON payload
        prompt = (
            "Your goal is to extract structured information from the patient's medical notes that matches "
            "the JSON schema details below. Extract the following entities if present:\n"
            "- Conditions: Diagnoses, complaints, symptoms, or disease history.\n"
            "- Interventions: Medications, placebos, therapies, or specific medical plans.\n"
            "Format the output strictly as a valid JSON object containing 'conditions' and 'interventions' lists. "
            "Do not output markdown code blocks (like ```json), intro text, or explanation. Output ONLY the raw JSON string.\n\n"
            f"Patient Medical Notes:\n{cleaned_notes}"
        )
        
        cortex_prompt = f"'{prompt}'"
        
        # We can construct messages for models that support it, but since we are doing simple session.sql execution,
        # executing with Snowflake Cortex Complete is cleaner.
        sql = f"select snowflake.cortex.complete('{selected_llm}', {cortex_prompt}) as response"
        
        with st.spinner("Extracting clinical data using Snowflake Cortex..."):
            try:
                cortex_response = session.sql(sql).to_pandas().iloc[0]['RESPONSE']
                
                # Attempt to parse raw response as JSON to render in tables
                # Sometimes models include markdown formatting like ```json even when told not to.
                # Let's clean it just in case.
                cleaned_response = cortex_response.strip()
                if cleaned_response.startswith("```"):
                    # Strip out ```json and ```
                    lines = cleaned_response.splitlines()
                    if lines[0].startswith("```"):
                        lines = lines[1:]
                    if lines[-1].startswith("```"):
                        lines = lines[:-1]
                    cleaned_response = "\n".join(lines).strip()
                
                try:
                    data = json.loads(cleaned_response)
                    
                    # Display as neat columns and tables
                    st.success("Successfully extracted and parsed JSON!")
                    
                    col_cond, col_int = st.columns(2)
                    with col_cond:
                        st.markdown("##### 🩺 Extracted Conditions")
                        conditions = data.get("conditions", [])
                        if conditions:
                            for cond in conditions:
                                st.markdown(f"- {cond}")
                        else:
                            st.write("No conditions identified.")
                            
                    with col_int:
                        st.markdown("##### 🧪 Extracted Interventions")
                        interventions = data.get("interventions", [])
                        if interventions:
                            for intervent in interventions:
                                st.markdown(f"- {intervent}")
                        else:
                            st.write("No interventions identified.")
                            
                    with st.expander("Show Raw JSON Output"):
                        st.json(data)
                        
                except json.JSONDecodeError:
                    # Fallback to displaying raw text if parsing fails
                    st.warning("Response returned, but it could not be parsed as valid JSON.")
                    st.text(cortex_response)
                    
            except Exception as e:
                st.error(f"Error calling Cortex model: {str(e)}")
    elif run_extraction:
        st.warning("Please provide patient notes first.")
    else:
        st.info("Provide clinical notes and click 'Extract Entities' to invoke Snowflake Cortex.")
