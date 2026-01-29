import streamlit as st
from core.upstage_client import UpstageClient
from agents.orchestrator_agent import OrchestratorAgent
from ui.styles import SOLAR_CSS
from ui.components import (
    render_file_uploader,
    render_options,
    render_progress,
    render_error_note
)
from config import APP_NAME, APP_ICON, APP_TAGLINE, APP_SUBTITLE

# 페이지 설정
st.set_page_config(
    page_title=f"{APP_NAME} - {APP_SUBTITLE}",
    page_icon=APP_ICON,
    layout="wide"
)

# Solar CSS 적용
st.markdown(SOLAR_CSS, unsafe_allow_html=True)

# 커스텀 헤더
st.markdown(f"""
<div class="solar-header">
    <div class="solar-logo">{APP_ICON}</div>
    <div class="solar-title">{APP_NAME}</div>
    <div class="solar-tagline">{APP_TAGLINE}</div>
</div>
""", unsafe_allow_html=True)

# 상단: 업로드 | 설정
col1, col2 = st.columns([1, 1])

with col1:
    with st.container(border=True):
        uploaded_file = render_file_uploader()

        if uploaded_file:
            st.markdown("""
            <div class="solar-image-container">
            """, unsafe_allow_html=True)
            st.image(uploaded_file, caption="업로드된 문제", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        options = render_options()

# 생성 버튼 (전체 너비 중앙)
st.markdown("<div style='margin: 1.5rem 0'></div>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    generate_btn = st.button(
        f"{APP_ICON} 오답노트 생성",
        type="primary",
        disabled=not uploaded_file,
        use_container_width=True
    )

# 구분선
st.markdown("<div style='margin: 1rem 0'></div>", unsafe_allow_html=True)

# 하단: 결과 영역
if generate_btn and uploaded_file:
    progress_placeholder = st.empty()

    def update_progress(step, total, message):
        with progress_placeholder.container():
            render_progress(step, total, message)

    try:
        client = UpstageClient()
        orchestrator = OrchestratorAgent(client)
        orchestrator.set_progress_callback(update_progress)

        file_content = uploaded_file.read()
        filename = uploaded_file.name

        result = orchestrator.execute(file_content, filename, options)

        progress_placeholder.empty()

        if result["success"]:
            st.success(f"✅ 오답노트 생성 완료! (유사문제 {result['problems_count']}개)")
            render_error_note(result["note"])
        else:
            st.error(f"❌ {result['error']}")

    except Exception as e:
        st.error(f"❌ 오류가 발생했습니다: {str(e)}")

# Solar 테마 푸터
st.markdown(f"""
<div class="solar-footer">
    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">{APP_ICON} {APP_NAME}</div>
    <div>Powered by <a href="https://www.upstage.ai" target="_blank">Upstage Solar API</a> | Made for 수학 자기주도 학습</div>
</div>
""", unsafe_allow_html=True)
