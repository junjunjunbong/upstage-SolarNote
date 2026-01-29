"""SolarNote UI 컴포넌트"""
import streamlit as st
from models.schemas import ErrorNote


def render_file_uploader():
    """Solar 스타일 파일 업로더"""
    st.markdown("""
    <div class="solar-subheader">
        <span class="solar-subheader-icon">📤</span>
        <span>문제 업로드</span>
    </div>
    """, unsafe_allow_html=True)

    return st.file_uploader(
        "수학 문제 이미지를 업로드하세요",
        type=["png", "jpg", "jpeg", "pdf"],
        help="PNG, JPG, PDF 형식 지원",
        label_visibility="collapsed"
    )


def render_options():
    """Solar 스타일 옵션 선택"""
    st.markdown("""
    <div class="solar-subheader">
        <span class="solar-subheader-icon">⚙️</span>
        <span>설정</span>
    </div>
    """, unsafe_allow_html=True)

    # 설정 옵션들을 2열로 배치하여 공간 활용도 높임
    col1, col2 = st.columns(2)
    
    with col1:
        # 난이도 선택 (별점 방식)
        st.markdown("**난이도**")
        difficulty = st.radio(
            "난이도",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: "⭐" * x,
            horizontal=False,  # 세로로 배치하거나
            index=2,
            label_visibility="collapsed",
            key="difficulty_radio"
        )

    with col2:
        # 문제 개수 선택
        st.markdown("**유사문제 개수**")
        problem_count = st.radio(
            "유사문제 개수",
            options=[3, 5, 7],
            format_func=lambda x: f"{x}개",
            horizontal=False,
            index=1,
            label_visibility="collapsed",
            key="count_radio"
        )

    return {"difficulty": difficulty, "problem_count": problem_count}


def render_progress(step: int, total: int, message: str):
    """Solar 스타일 진행 상태"""
    steps_info = [
        ("📄", "문서 분석"),
        ("🔍", "문제 추출"),
        ("📚", "개념 정리"),
        ("✏️", "유사문제 생성"),
        ("📝", "풀이 생성"),
        ("📋", "오답노트 완성")
    ]

    st.markdown("""
    <div class="solar-progress-container">
    """, unsafe_allow_html=True)

    for i, (icon, label) in enumerate(steps_info[:total], 1):
        if i < step:
            status = "completed"
            display_icon = "✓"
        elif i == step:
            status = "active"
            display_icon = icon
        else:
            status = ""
            display_icon = icon

        st.markdown(f"""
        <div class="solar-progress-step {status}">
            <div class="solar-progress-icon">{display_icon}</div>
            <span>{label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Streamlit 기본 프로그레스바도 표시
    progress = step / total
    st.progress(progress, text=message)


def render_error_note(note: ErrorNote):
    """탭 기반 오답노트 UI"""
    st.markdown(f"""
    <div class="solar-card" style="background: linear-gradient(135deg, #FFF9F5, #FFFFFF);">
        <h2 style="color: var(--solar-primary, #FF6B35); margin: 0;">
            ☀️ {note.title}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # 탭 기반 UI
    tab1, tab2, tab3, tab4 = st.tabs([
        "📌 원본문제",
        "📚 개념정리",
        "🔄 유사문제",
        "💡 학습조언"
    ])

    with tab1:
        _render_original_problem_tab(note)

    with tab2:
        _render_concept_tab(note)

    with tab3:
        _render_similar_problems_tab(note)

    with tab4:
        _render_study_tips_tab(note)


def _render_original_problem_tab(note: ErrorNote):
    """원본문제 탭 렌더링"""
    st.markdown("""
    <div class="solar-subheader">
        <span class="solar-subheader-icon">📌</span>
        <span>원본 문제</span>
    </div>
    """, unsafe_allow_html=True)

    st.info(note.original_problem)

    if note.original_solution and note.original_solution.steps:
        st.markdown("""
        <div class="solar-subheader">
            <span class="solar-subheader-icon">✏️</span>
            <span>풀이 과정</span>
        </div>
        """, unsafe_allow_html=True)

        # 타임라인 스타일 풀이
        st.markdown('<div class="solar-timeline">', unsafe_allow_html=True)
        for i, step in enumerate(note.original_solution.steps, 1):
            st.markdown(f"""
            <div class="solar-timeline-item">
                <strong>Step {i}</strong><br>
                {step}
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.success(f"**정답:** {note.original_solution.answer}")

        if note.original_solution.key_point:
            st.markdown(f"""
            <div class="solar-hint">
                <span class="solar-hint-icon">💡</span>
                <span>{note.original_solution.key_point}</span>
            </div>
            """, unsafe_allow_html=True)


def _render_concept_tab(note: ErrorNote):
    """개념정리 탭 렌더링"""
    if note.concept_summary:
        st.markdown("""
        <div class="solar-subheader">
            <span class="solar-subheader-icon">📖</span>
            <span>핵심 개념</span>
        </div>
        """, unsafe_allow_html=True)

        st.write(note.concept_summary)

    if note.formula_box:
        st.markdown("""
        <div class="solar-subheader">
            <span class="solar-subheader-icon">📐</span>
            <span>필수 공식</span>
        </div>
        """, unsafe_allow_html=True)

        for formula in note.formula_box:
            st.markdown(f"""
            <div class="solar-formula-box">
            """, unsafe_allow_html=True)
            st.latex(formula)
            st.markdown("</div>", unsafe_allow_html=True)

    if not note.concept_summary and not note.formula_box:
        st.info("이 문제에 대한 개념 정리가 없습니다.")


def _render_similar_problems_tab(note: ErrorNote):
    """유사문제 탭 렌더링"""
    st.markdown("""
    <div class="solar-subheader">
        <span class="solar-subheader-icon">🔄</span>
        <span>유사 문제</span>
    </div>
    """, unsafe_allow_html=True)

    if not note.similar_problems:
        st.info("유사 문제가 없습니다.")
        return

    for i, item in enumerate(note.similar_problems, 1):
        problem = item.get("problem")
        solution = item.get("solution")

        with st.expander(f"문제 {i}: {problem.problem[:50]}..." if hasattr(problem, 'problem') and len(problem.problem) > 50 else f"문제 {i}", expanded=(i == 1)):
            if hasattr(problem, 'problem'):
                st.markdown(f"""
                <div class="solar-problem-card">
                    <div class="solar-problem-header">
                        <div class="solar-problem-number">{i}</div>
                        <div class="solar-problem-meta">
                            <span>📝 {problem.variation_type}</span>
                            <span>{'⭐' * problem.difficulty}</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem;">{problem.problem}</div>
                </div>
                """, unsafe_allow_html=True)

                if problem.hint:
                    st.markdown(f"""
                    <div class="solar-hint">
                        <span class="solar-hint-icon">💡</span>
                        <span><strong>힌트:</strong> {problem.hint}</span>
                    </div>
                    """, unsafe_allow_html=True)

            if solution and hasattr(solution, 'steps') and solution.steps:
                st.markdown("---")
                st.markdown("**📝 풀이**")

                st.markdown('<div class="solar-timeline">', unsafe_allow_html=True)
                for j, step in enumerate(solution.steps, 1):
                    st.markdown(f"""
                    <div class="solar-timeline-item">
                        <strong>Step {j}</strong><br>
                        {step}
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.success(f"**정답:** {solution.answer}")


def _render_study_tips_tab(note: ErrorNote):
    """학습조언 탭 렌더링"""
    if note.study_tips:
        st.markdown("""
        <div class="solar-subheader">
            <span class="solar-subheader-icon">💡</span>
            <span>학습 조언</span>
        </div>
        """, unsafe_allow_html=True)

        st.write(note.study_tips)

    if note.next_topics:
        st.markdown("""
        <div class="solar-subheader">
            <span class="solar-subheader-icon">📖</span>
            <span>다음 학습 추천</span>
        </div>
        """, unsafe_allow_html=True)

        for topic in note.next_topics:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0;">
                <span style="color: var(--solar-primary, #FF6B35);">▸</span>
                <span>{topic}</span>
            </div>
            """, unsafe_allow_html=True)

    if not note.study_tips and not note.next_topics:
        st.info("학습 조언이 없습니다.")
