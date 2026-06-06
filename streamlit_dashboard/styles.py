import streamlit as st

def apply_custom_css():
    """
    Applies custom high-end CSS styles to create a dark-themed, 
    premium glassmorphic visual interface for the Streamlit dashboard.
    """
    st.markdown("""
        <style>
        /* Import premium font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
        
        /* Apply font to primary elements */
        html, body, [class*="css"], .stMarkdown, p, div, label {
            font-family: 'Outfit', sans-serif !important;
        }
        
        /* Custom main dashboard layout background */
        .main {
            background: radial-gradient(circle at 10% 20%, rgba(15, 17, 26, 1) 0%, rgba(21, 26, 44, 1) 90.1%);
            color: #e2e8f0;
        }
        
        /* Glassmorphic Container Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 24px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        
        .glass-card:hover {
            transform: translateY(-3px);
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 12px 40px 0 rgba(99, 102, 241, 0.15);
        }
        
        /* Text gradient for headers */
        .gradient-title {
            background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 2.2rem;
            margin-bottom: 8px;
        }
        
        .gradient-subtitle {
            background: linear-gradient(135deg, #a78bfa, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
            font-size: 1.4rem;
            margin-top: 16px;
            margin-bottom: 12px;
        }
        
        /* Status Badges */
        .status-badge {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.85rem;
            font-weight: 600;
            text-align: center;
        }
        .status-connected {
            background-color: rgba(16, 185, 129, 0.12);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.35);
        }
        .status-disconnected {
            background-color: rgba(239, 68, 68, 0.12);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.35);
        }
        
        /* Code blocks */
        code {
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: #f472b6 !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
            font-size: 0.9em !important;
        }
        
        /* Glassmorphic sidebar customization */
        section[data-testid="stSidebar"] {
            background-color: rgba(15, 17, 26, 0.95);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Custom styling for standard input controls to look darker and sleek */
        .stTextArea textarea, .stTextInput input {
            background-color: rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            color: #f8fafc !important;
            border-radius: 10px !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
        }
        
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
        }
        
        /* Modern Select Box styling */
        div[data-baseweb="select"] {
            background-color: rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            color: #f8fafc !important;
        }
        
        /* Premium Buttons */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
            transition: all 0.25s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        }
        
        div.stButton > button:first-child:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
            background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%) !important;
        }
        
        div.stButton > button:first-child:active {
            transform: translateY(1px) !important;
        }
        
        /* Expander customization */
        div[data-testid="stExpander"] {
            background-color: rgba(255, 255, 255, 0.01) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
        }
        
        /* Custom footer style */
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.05);
            text-align: center;
            font-size: 0.8rem;
            color: #64748b;
        }
        </style>
    """, unsafe_allow_html=True)
