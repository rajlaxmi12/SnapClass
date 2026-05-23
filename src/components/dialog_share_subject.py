import streamlit as st
import segno
import io

@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    
    # Dynamically detect the app's base URL
    try:
        base_url = st.secrets.get("BASE_URL", None)
    except Exception:
        base_url = None

    if not base_url:
        # Auto-detect from Streamlit's runtime headers
        session = st.runtime.get_instance()._session_mgr.list_active_sessions()
        try:
            headers = st.context.headers
            host = headers.get("host", "localhost:8501")
            scheme = "https" if "localhost" not in host else "http"
            base_url = f"{scheme}://{host}"
        except Exception:
            base_url = "http://localhost:8501"  # safe fallback

    join_url = f"{base_url}/?join-code={subject_code}"

    st.header("Scan to Join")

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info('Copy this link to share on Whatsapp or Email')

    with col2:
        st.markdown('### Scan to Join')
        st.image(out.getvalue(), caption='QRCODE for class joining')