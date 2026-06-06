import streamlit as st
import sys
from pathlib import Path

# Add root directory to system path to enable shared module imports
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.append(root_dir)

from common.connection import get_session
from streamlit_dashboard.styles import apply_custom_css

# Page Configuration
st.set_page_config(
    page_title="Snowflake GenAI Hub",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply premium styles
apply_custom_css()

# Sidebar branding
with st.sidebar:
    st.markdown("### ❄️ Snowflake GenAI")
    st.markdown("Configure your Snowflake connection details in the `.env` file at the project root for local execution.")
    st.caption("v1.0.0 | Enterprise Edition")

# Main Page Header
st.markdown('<div class="gradient-title">Snowflake Generative AI Hub</div>', unsafe_allow_html=True)
st.markdown("##### Empowering enterprise data applications with native Snowpark and Cortex LLM services.")
st.markdown("---")

# Layout: Split into Main introduction and Connection Status Panel
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        """
        <div class="glass-card">
            <h3>Welcome to the GenAI Workspace</h3>
            <p>This workspace serves as a live, interactive exploration of how to build LLM-powered applications
            natively within the <strong>Snowflake Data Cloud</strong>. By leveraging <strong>Snowpark</strong> for structured 
            data orchestration and <strong>Cortex APIs</strong> for managed LLMs, we bring models directly to the data 
            without moving or exporting sensitive datasets.</p>
            <p>Use the sidebar navigation to explore the available modules:</p>
            <ul>
                <li><strong>📊 Transcript Analytics</strong>: Extract structured JSON summaries, execute language translations, and perform real-time sentiment analysis on customer call records.</li>
                <li><strong>🎫 Ticket Automation</strong>: Automatically categorize support inquiries and draft personalized responses (Emails/Texts) using different LLM models, including fine-tuned models.</li>
                <li><strong>🏥 Medical Extraction</strong>: Apply few-shot clinical instructions to extract medical conditions and interventions from physician notes.</li>
            </ul>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass-card">
            <h3>Architectural Advantages</h3>
            <div style="display: flex; gap: 15px; margin-top: 10px;">
                <div style="flex: 1; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                    <h5 style="color: #38bdf8; margin-bottom: 5px;">🔒 Data Security</h5>
                    <p style="font-size: 0.85rem; margin: 0; color: #94a3b8;">Zero data egress. Your enterprise documents and data remain protected within Snowflake’s secure governance boundary.</p>
                </div>
                <div style="flex: 1; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                    <h5 style="color: #818cf8; margin-bottom: 5px;">⚡ High Performance</h5>
                    <p style="font-size: 0.85rem; margin: 0; color: #94a3b8;">Leverage Snowflake's scalable compute warehouses (Virtual Warehouses) for batch inference and model training pipelines.</p>
                </div>
                <div style="flex: 1; background: rgba(255,255,255,0.02); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                    <h5 style="color: #c084fc; margin-bottom: 5px;">⚙️ Seamless Integration</h5>
                    <p style="font-size: 0.85rem; margin: 0; color: #94a3b8;">No complex pipeline infrastructure. Execute LLM completion, classification, and translation in standard SQL or Python.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("### Connection Registry")
    
    # Establish and report session status
    try:
        session = get_session()
        current_user = session.get_current_user()
        current_warehouse = session.get_current_warehouse()
        current_database = session.get_current_database()
        current_schema = session.get_current_schema()
        
        st.markdown(
            f"""
            <div class="glass-card" style="border-left: 4px solid #34d399;">
                <h4 style="margin-top:0;">Snowflake Session</h4>
                <div style="margin-bottom: 12px;">
                    <span class="status-badge status-connected">Connected</span>
                </div>
                <table style="width: 100%; font-size: 0.85rem; color: #94a3b8; border-collapse: collapse;">
                    <tr>
                        <td style="padding: 4px 0; font-weight: 600;">Active User:</td>
                        <td style="text-align: right; color: #e2e8f0;">{current_user}</td>
                    </tr>
                    <tr>
                        <td style="padding: 4px 0; font-weight: 600;">Warehouse:</td>
                        <td style="text-align: right; color: #e2e8f0;">{current_warehouse}</td>
                    </tr>
                    <tr>
                        <td style="padding: 4px 0; font-weight: 600;">Database:</td>
                        <td style="text-align: right; color: #e2e8f0;">{current_database}</td>
                    </tr>
                    <tr>
                        <td style="padding: 4px 0; font-weight: 600;">Schema:</td>
                        <td style="text-align: right; color: #e2e8f0;">{current_schema}</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.markdown(
            f"""
            <div class="glass-card" style="border-left: 4px solid #f87171;">
                <h4 style="margin-top:0;">Snowflake Session</h4>
                <div style="margin-bottom: 12px;">
                    <span class="status-badge status-disconnected">Disconnected</span>
                </div>
                <p style="font-size: 0.85rem; color: #f87171; background: rgba(239, 68, 68, 0.05); padding: 8px; border-radius: 6px;">
                    <strong>Error details:</strong> {str(e)}
                </p>
                <h5 style="margin-top:15px; margin-bottom:5px;">How to resolve:</h5>
                <ol style="font-size: 0.8rem; padding-left: 15px; color: #94a3b8; margin: 0;">
                    <li>Duplicate <code>.env.template</code> to <code>.env</code> at project root.</li>
                    <li>Open <code>.env</code> and fill in your Snowflake credentials.</li>
                    <li>Ensure your database has Snowpark & Cortex enabled.</li>
                    <li>Refresh this page.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer
st.markdown('<div class="footer">Generative AI with Snowflake Quickstart Dashboard • Antigravity Architectures</div>', unsafe_allow_html=True)
