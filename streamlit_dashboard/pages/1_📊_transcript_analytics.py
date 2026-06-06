import streamlit as st
import sys
from pathlib import Path

# Add root directory to system path to enable shared module imports
root_dir = str(Path(__file__).resolve().parent.parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from common.connection import get_session
from streamlit_dashboard.styles import apply_custom_css

# Page Configuration
st.set_page_config(
    page_title="Transcript Analytics | Snowflake GenAI",
    page_icon="📊",
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
st.markdown('<div class="gradient-title">Customer Transcript Analytics</div>', unsafe_allow_html=True)
st.markdown("##### Execute AI-powered summarization, translation, and sentiment extraction natively on Snowflake.")
st.markdown("---")

# Sample Data Templates
SAMPLE_TRANSCRIPTS = {
    "Select a sample transcript...": "",
    "Vacuum Cleaner Defect (XYZ-2000)": """Agent: Hello, how can I assist you today? 
Customer: Hi, I recently bought the XYZ-2000 vacuum cleaner and it's not working properly. 
Agent: I'm sorry to hear that. Could you please describe the issue? 
Customer: Sure, when I turn it on, it makes a strange noise and doesn't suck up dirt like it should. 
Agent: It sounds like a motor issue. Have you checked if there's any blockage in the vacuum? 
Customer: Yes, I've checked and there's no blockage. 
Agent: Alright, it seems like the motor might be defective. I'll arrange for a replacement motor to be sent to you. 
Customer: Thank you, that would be great. 
Agent: You're welcome. It should arrive within the next few days. If you have any other issues, feel free to contact us. 
Customer: Okay, thanks for your help.""",

    "Broken Helmet Buckles (Mountain Ski Adventures)": """Customer: Hello
Agent: Hi there, I hope you're having a great day! To better assist you, could you please provide your first and last name and the company you are calling from?
Customer: Sure, my name is Jessica Turner and I'm calling from Mountain Ski Adventures.
Agent: Thanks, Jessica. What can I help you with today?
Customer: Well, we recently ordered a batch of XtremeX helmets, and upon inspection, we noticed that the buckles on several helmets are broken and won't secure the helmet properly.
Agent: I apologize for the inconvenience this has caused you. To confirm, is your order number 68910?
Customer: Yes, that's correct.
Agent: Thank you for confirming. I'm going to look into this issue and see what we can do to correct it. Would you prefer a refund or a replacement for the damaged helmets?
Customer: A replacement would be ideal, as we still need the helmets for our customers.
Agent: I understand. I will start the process to send out replacements for the damaged helmets as soon as possible. Can you please specify the quantity of helmets with broken buckles?
Customer: There are ten helmets with broken buckles in total.
Agent: Thank you for providing me with the quantity. We will expedite a new shipment of ten XtremeX helmets with functioning buckles to your location. You should expect them to arrive within 3-5 business days.
Customer: Thank you for your assistance, I appreciate it."""
}

# Supported translation languages
SUPPORTED_LANGUAGES = {
    'German': 'de',
    'French': 'fr',
    'Korean': 'ko',
    'Portuguese': 'pt',
    'English': 'en',
    'Italian': 'it',
    'Russian': 'ru',
    'Swedish': 'sv',
    'Spanish': 'es',
    'Japanese': 'ja',
    'Polish': 'pl'
}

# Create Tabs for different analytical tasks
tab_summary, tab_translation, tab_sentiment = st.tabs([
    "📋 JSON Summarization", 
    "🌐 Language Translation", 
    "🧠 Sentiment Analysis"
])

# ==============================================================================
# TAB 1: JSON SUMMARIZATION
# ==============================================================================
with tab_summary:
    st.markdown('<div class="gradient-subtitle">Structured Summarization</div>', unsafe_allow_html=True)
    st.markdown("Extract key entities (product names, defects, action items) into structured JSON formats automatically.")
    
    col_input, col_output = st.columns([1, 1])
    
    with col_input:
        selected_sample = st.selectbox("Load Sample Transcript", list(SAMPLE_TRANSCRIPTS.keys()), key="summary_sample")
        
        # Determine the initial text
        initial_text = SAMPLE_TRANSCRIPTS[selected_sample] if selected_sample != "Select a sample transcript..." else ""
        
        entered_text = st.text_area(
            "Customer Conversation Transcript", 
            value=initial_text,
            height=300,
            placeholder="Type or copy a call transcript here..."
        )
        
        selected_model = st.selectbox(
            "Select Cortex Model",
            ["mistral-large", "llama3-8b", "mistral-7b"],
            help="Choose the underlying LLM to handle the extraction task."
        )
        
        run_summary = st.button("Generate JSON Summary ⚡", key="btn_summary")
        
    with col_output:
        st.markdown("**Structured JSON Output**")
        if run_summary and entered_text:
            cleaned_text = entered_text.replace("'", "\\'")
            prompt = f"Summarize this transcript in less than 200 words. Put the product name, defect if any, and summary in JSON format: {cleaned_text}"
            cortex_prompt = "'[INST] " + prompt + " [/INST]'"
            
            with st.spinner("Processing in Snowflake Cortex..."):
                try:
                    sql = f"select snowflake.cortex.complete('{selected_model}', {cortex_prompt}) as response"
                    cortex_response = session.sql(sql).to_pandas().iloc[0]['RESPONSE']
                    st.code(cortex_response, language="json")
                except Exception as e:
                    st.error(f"Error executing summarize function: {str(e)}")
        elif run_summary:
            st.warning("Please enter a call transcript first.")
        else:
            st.info("Await analysis... Click the button on the left to begin.")

# ==============================================================================
# TAB 2: LANGUAGE TRANSLATION
# ==============================================================================
with tab_translation:
    st.markdown('<div class="gradient-subtitle">Cortex Translation Service</div>', unsafe_allow_html=True)
    st.markdown("Translate multilingual transcripts natively inside your Snowflake tables or text strings.")
    
    col_trans_input, col_trans_output = st.columns([1, 1])
    
    with col_trans_input:
        col_lang_from, col_lang_to = st.columns(2)
        with col_lang_from:
            from_lang = st.selectbox('From Language', list(sorted(SUPPORTED_LANGUAGES.keys())), index=4)  # Default: English
        with col_lang_to:
            to_lang = st.selectbox('To Language', list(sorted(SUPPORTED_LANGUAGES.keys())), index=8)  # Default: Spanish
            
        selected_trans_sample = st.selectbox("Load Sample Transcript", list(SAMPLE_TRANSCRIPTS.keys()), key="trans_sample")
        initial_trans_text = SAMPLE_TRANSCRIPTS[selected_trans_sample] if selected_trans_sample != "Select a sample transcript..." else ""
        
        trans_text = st.text_area(
            "Text to Translate", 
            value=initial_trans_text,
            height=220,
            placeholder="Enter the text to translate..."
        )
        
        run_translation = st.button("Translate Text 🌐", key="btn_translate")
        
    with col_trans_output:
        st.markdown("**Translated Text Output**")
        if run_translation and trans_text:
            cleaned_trans_text = trans_text.replace("'", "\\'")
            with st.spinner("Translating..."):
                try:
                    sql = f"select snowflake.cortex.translate('{cleaned_trans_text}','{SUPPORTED_LANGUAGES[from_lang]}','{SUPPORTED_LANGUAGES[to_lang]}') as response"
                    cortex_response = session.sql(sql).to_pandas().iloc[0]['RESPONSE']
                    st.write(cortex_response)
                except Exception as e:
                    st.error(f"Error executing translation: {str(e)}")
        elif run_translation:
            st.warning("Please enter some text to translate.")
        else:
            st.info("Await translation...")

# ==============================================================================
# TAB 3: SENTIMENT ANALYSIS
# ==============================================================================
with tab_sentiment:
    st.markdown('<div class="gradient-subtitle">Sentiment Analysis Score</div>', unsafe_allow_html=True)
    st.markdown("Calculate polarity scores for conversational logs using Snowflake Cortex's built-in sentiment analysis tool.")
    
    col_sent_input, col_sent_output = st.columns([1, 1])
    
    with col_sent_input:
        selected_sent_sample = st.selectbox("Load Sample Transcript", list(SAMPLE_TRANSCRIPTS.keys()), key="sent_sample")
        initial_sent_text = SAMPLE_TRANSCRIPTS[selected_sent_sample] if selected_sent_sample != "Select a sample transcript..." else ""
        
        sent_text = st.text_area(
            "Text to Analyze", 
            value=initial_sent_text,
            height=280,
            placeholder="Type customer statements or logs to run sentiment extraction..."
        )
        
        run_sentiment = st.button("Extract Sentiment Score 🧠", key="btn_sentiment")
        
    with col_sent_output:
        st.markdown("**Sentiment Metrics**")
        if run_sentiment and sent_text:
            cleaned_sent_text = sent_text.replace("'", "\\'")
            with st.spinner("Analyzing Sentiment..."):
                try:
                    sql = f"select snowflake.cortex.sentiment('{cleaned_sent_text}') as sentiment"
                    cortex_response = session.sql(sql).to_pandas().iloc[0]['SENTIMENT']
                    
                    # Sentiment Display Card
                    score = float(cortex_response)
                    if score > 0.3:
                        badge = '<span class="status-badge status-connected">Positive</span>'
                        emoji = "🟢 😊"
                    elif score < -0.3:
                        badge = '<span class="status-badge status-disconnected">Negative</span>'
                        emoji = "🔴 😠"
                    else:
                        badge = '<span style="background-color:rgba(255,255,255,0.05); color:#94a3b8; border:1px solid rgba(255,255,255,0.15);" class="status-badge">Neutral</span>'
                        emoji = "⚪ 😐"
                        
                    st.markdown(
                        f"""
                        <div class="glass-card">
                            <h4>Sentiment Verdict: {emoji}</h4>
                            <div style="margin-top: 10px; margin-bottom: 15px;">
                                {badge}
                            </div>
                            <h2 style="margin: 0; color: #f472b6;">{score:+.4f}</h2>
                            <p style="font-size: 0.85rem; color: #64748b; margin-top: 5px;">Polarity score is bounded between -1.0 (extremely negative) and +1.0 (extremely positive).</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"Error calculating sentiment: {str(e)}")
        elif run_sentiment:
            st.warning("Please enter some text to analyze.")
        else:
            st.info("Await sentiment computation...")
