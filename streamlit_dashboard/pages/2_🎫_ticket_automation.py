import streamlit as st
import sys
import ast
from pathlib import Path

# Add root directory to system path to enable shared module imports
root_dir = str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from common.connection import get_session
from streamlit_dashboard.styles import apply_custom_css

# Page Configuration
st.set_page_config(
    page_title="Ticket Automation | Snowflake GenAI",
    page_icon="🎫",
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
st.markdown('<div class="gradient-title">Support Ticket Automation</div>', unsafe_allow_html=True)
st.markdown("##### Automatically classify customer requests and draft custom, context-aware responses.")
st.markdown("---")

# Data definitions
TICKET_CATEGORIES = ['Roaming fees', 'Slow data speed', 'Lost phone', 'Add new line', 'Closing account']

SAMPLE_TICKETS = {
    "Select a support ticket...": "",
    "Roaming Fee Dispute (Roaming fees)": "I traveled to Japan for two weeks and kept my data usage to a minimum. However, I was charged $90 in international fees. These charges were not communicated to me, and I request a detailed breakdown and a refund. Thank you for your prompt assistance.",
    
    "Slow Internet Speed (Slow data speed)": "My internet speed has been absolutely terrible today. I am trying to work from home, but Zoom calls keep dropping and webpages take several minutes to load. Can you run a test on my line or reset the connection?",
    
    "Stolen Mobile Device (Lost phone)": "My iPhone was stolen while I was at a restaurant yesterday. I need to suspend my phone line immediately to prevent any unauthorized usage, and I'd like to know what options I have to get a replacement device.",
    
    "New Account Line (Add new line)": "Hello, I want to add an additional line to my existing family plan for my daughter. Can you let me know what the current pricing is for a new SIM card and if there are any promotional deals running?",
    
    "Account Termination (Closing account)": "I am writing to request the closure of my telecom account. I have recently moved out of the country and will no longer need your services. Please let me know the final steps to settle the account and stop billing."
}

SYSTEM_PROMPT = """You are a customer support representative at a telecommunications company. 
Suddenly there is a spike in customer support tickets. 
You need to understand and analyze the support requests from customers.
Based on the root cause of the main issue in the support request, craft a response to resolve the customer issue.
Write a text message under 25 words, if the contact_preference field is text message.
Write an email in maximum of 100 words if the contact_preference field is email. 
Focus on alleviating the customer issue and improving customer satisfaction in your response.
Strictly follow the word count limit for the response. 
Write only email or text message response based on the contact_preference for every customer. 
Do not generate both email and text message response.
"""

# Layout Split
col_controls, col_display = st.columns([1, 1])

with col_controls:
    st.markdown('<div class="gradient-subtitle">Configuration</div>', unsafe_allow_html=True)
    
    selected_sample = st.selectbox("Load Sample Support Request", list(SAMPLE_TICKETS.keys()))
    initial_text = SAMPLE_TICKETS[selected_sample] if selected_sample != "Select a support ticket..." else ""
    
    customer_request = st.text_area(
        "Customer Support Request", 
        value=initial_text,
        height=220,
        placeholder="Enter customer support ticket details here..."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        selected_preference = st.selectbox('Contact Preference', ('Email', 'Text message'))
    with col2:
        selected_llm = st.selectbox(
            'Select Model',
            ('llama3-8b', 'mistral-7b', 'mistral-large', 'SUPPORT_MESSAGES_FINETUNED_MISTRAL_7B'),
            index=2, # Default to mistral-large
            help="Select the model to execute the response drafting. Includes custom fine-tuned model (if created)."
        )
        
    generate = st.button("Analyze & Draft Response ⚡", type="primary")

with col_display:
    st.markdown('<div class="gradient-subtitle">Automation Output</div>', unsafe_allow_html=True)
    
    if generate and customer_request:
        cleaned_request = customer_request.replace("'", "\\'")
        
        # 1. Classify Ticket using Cortex Classify Text
        category_sql = f"""
        select snowflake.cortex.classify_text('{cleaned_request}', {TICKET_CATEGORIES}) as ticket_category
        """
        
        with st.spinner("Classifying ticket category..."):
            try:
                df_category = session.sql(category_sql).to_pandas().iloc[0]['TICKET_CATEGORY']
                df_category_dict = ast.literal_eval(df_category)
                detected_label = df_category_dict['label']
            except Exception as e:
                detected_label = "Unknown / Classification Error"
                st.error(f"Failed to classify ticket: {str(e)}")
                
        # 2. Complete draft response using Selected LLM
        message_sql = f"""
        select snowflake.cortex.complete('{selected_llm}', concat('{SYSTEM_PROMPT}', '{cleaned_request}', '{selected_preference}')) as custom_message
        """
        
        with st.spinner(f"Drafting response with {selected_llm}..."):
            try:
                df_message = session.sql(message_sql).to_pandas().iloc[0]['CUSTOM_MESSAGE']
            except Exception as e:
                df_message = f"Error generating message: {str(e)}"
                
        # UI Presentation of the output
        st.markdown(
            f"""
            <div class="glass-card">
                <h4 style="margin-top:0;">Analysis Results</h4>
                <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                    <div style="flex: 1; background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.3); padding: 8px; border-radius: 8px; text-align: center;">
                        <span style="font-size:0.75rem; color: #38bdf8; font-weight:600; display:block;">CLASSIFIED CATEGORY</span>
                        <strong style="font-size:0.95rem; color: #e2e8f0;">{detected_label}</strong>
                    </div>
                    <div style="flex: 1; background: rgba(129, 140, 248, 0.08); border: 1px solid rgba(129, 140, 248, 0.3); padding: 8px; border-radius: 8px; text-align: center;">
                        <span style="font-size:0.75rem; color: #818cf8; font-weight:600; display:block;">CONTACT METHOD</span>
                        <strong style="font-size:0.95rem; color: #e2e8f0;">{selected_preference}</strong>
                    </div>
                </div>
                <h5>Drafted Message ({selected_llm})</h5>
                <div style="background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.06); padding: 15px; border-radius: 10px; font-family: monospace; white-space: pre-wrap; font-size: 0.9rem;">{df_message}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif generate:
        st.warning("Please enter a customer request.")
    else:
        st.info("Provide a customer support ticket and click 'Analyze & Draft Response' to trigger analysis.")
