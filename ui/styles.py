"""SolarNote UI 스타일 정의"""

SOLAR_CSS = """
<style>
/* ========== Color Variables ========== */
:root {
    --solar-primary: #FF6B35;
    --solar-gold: #FFB347;
    --solar-light: #FFF4E6;
    --solar-dark: #E85A24;
    --solar-gradient: linear-gradient(135deg, #FF6B35, #FFB347);
    --solar-gradient-hover: linear-gradient(135deg, #E85A24, #FF9F2E);
    --solar-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
    --solar-shadow-hover: 0 8px 25px rgba(255, 107, 53, 0.4);
    --text-primary: #2D3748;
    --text-secondary: #718096;
    --bg-card: #FFFFFF;
    --border-light: #E2E8F0;
}

/* ========== Header Styles ========== */
.solar-header {
    background: var(--solar-gradient);
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: var(--solar-shadow);
    text-align: center;
    position: relative;
    overflow: hidden;
}

.solar-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0%, 100% { transform: translate(-30%, -30%) rotate(0deg); }
    50% { transform: translate(-20%, -20%) rotate(180deg); }
}

.solar-logo {
    font-size: 4rem;
    animation: pulse-glow 2s ease-in-out infinite;
    display: inline-block;
}

@keyframes pulse-glow {
    0%, 100% {
        transform: scale(1);
        filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.6));
    }
    50% {
        transform: scale(1.1);
        filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.9));
    }
}

.solar-title {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0.5rem 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    position: relative;
    z-index: 1;
}

.solar-tagline {
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.1rem;
    margin-top: 0.5rem;
    position: relative;
    z-index: 1;
}

/* ========== Card Styles ========== */
.solar-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05); /* Shadow 강화 */
    border: 1px solid var(--border-light);
    transition: all 0.3s ease;
    margin-bottom: 1rem;
}

.solar-card:hover {
    box-shadow: var(--solar-shadow);
    transform: translateY(-2px);
    border-color: var(--solar-primary);
}

.solar-card-title {
    color: var(--solar-primary);
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ========== Upload Area ========== */
.solar-upload {
    border: 2px dashed var(--solar-primary);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    background: var(--solar-light);
    transition: all 0.3s ease;
    cursor: pointer;
}

.solar-upload:hover {
    border-color: var(--solar-dark);
    background: #FFE8D6;
    box-shadow: var(--solar-shadow);
}

.solar-upload-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

/* ========== Button Styles ========== */
.stButton > button {
    background: var(--solar-gradient) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--solar-shadow) !important;
}

.stButton > button:hover {
    background: var(--solar-gradient-hover) !important;
    box-shadow: var(--solar-shadow-hover) !important;
    transform: translateY(-2px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.stButton > button:disabled {
    background: linear-gradient(135deg, #CBD5E0, #A0AEC0) !important;
    box-shadow: none !important;
}

/* ========== Progress Bar ========== */
.stProgress > div > div {
    background: var(--solar-gradient) !important;
    border-radius: 10px !important;
}

.solar-progress-container {
    background: var(--solar-light);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
}

.solar-progress-step {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0;
    color: var(--text-secondary);
}

.solar-progress-step.active {
    color: var(--solar-primary);
    font-weight: 600;
}

.solar-progress-step.completed {
    color: #38A169;
}

.solar-progress-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    background: var(--border-light);
}

.solar-progress-step.active .solar-progress-icon {
    background: var(--solar-gradient);
    color: white;
    animation: pulse 1.5s infinite;
}

.solar-progress-step.completed .solar-progress-icon {
    background: #38A169;
    color: white;
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255, 107, 53, 0.4); }
    50% { box-shadow: 0 0 0 10px rgba(255, 107, 53, 0); }
}

/* ========== Tab Styles ========== */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: var(--solar-light);
    padding: 0.5rem;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    background: transparent !important;
}

.stTabs [aria-selected="true"] {
    background: var(--solar-gradient) !important;
    color: white !important;
    box-shadow: var(--solar-shadow) !important;
}

/* ========== Expander Styles ========== */
.streamlit-expanderHeader {
    background: var(--solar-light) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-light) !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--solar-primary) !important;
    color: var(--solar-primary) !important;
}

/* ========== Difficulty Stars ========== */
.solar-stars {
    display: flex;
    gap: 4px;
    margin: 0.5rem 0;
}

.solar-star {
    font-size: 1.5rem;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.solar-star:hover {
    transform: scale(1.2);
}

.solar-star.filled {
    color: var(--solar-gold);
    text-shadow: 0 0 5px rgba(255, 179, 71, 0.5);
}

.solar-star.empty {
    color: #E2E8F0;
}

/* ========== Radio Button Group ========== */
.stRadio > div {
    flex-direction: row !important;
    gap: 1rem !important;
    flex-wrap: wrap !important;
}

.stRadio > div > label {
    background: var(--bg-card) !important;
    border: 2px solid var(--border-light) !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.25rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

.stRadio > div > label:hover {
    border-color: var(--solar-primary) !important;
    box-shadow: 0 2px 8px rgba(255, 107, 53, 0.2) !important;
}

.stRadio > div > label[data-checked="true"] {
    background: var(--solar-light) !important;
    border-color: var(--solar-primary) !important;
    color: var(--solar-primary) !important;
}

/* ========== Info/Success/Error Boxes ========== */
.stAlert {
    border-radius: 12px !important;
}

[data-testid="stAlert"][data-baseweb="notification"] {
    border-radius: 12px;
}

/* ========== Timeline Style for Solutions ========== */
.solar-timeline {
    position: relative;
    padding-left: 2rem;
    margin: 1rem 0;
}

.solar-timeline::before {
    content: '';
    position: absolute;
    left: 0.5rem;
    top: 0;
    bottom: 0;
    width: 2px;
    background: var(--solar-gradient);
}

.solar-timeline-item {
    position: relative;
    padding: 0.75rem 0;
    padding-left: 1rem;
}

.solar-timeline-item::before {
    content: '';
    position: absolute;
    left: -1.5rem;
    top: 1rem;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: var(--solar-primary);
    border: 2px solid white;
    box-shadow: 0 0 0 3px var(--solar-light);
}

/* ========== Footer ========== */
.solar-footer {
    text-align: center;
    padding: 1.5rem;
    margin-top: 2rem;
    background: var(--solar-light);
    border-radius: 12px;
    color: var(--text-secondary);
}

.solar-footer a {
    color: var(--solar-primary);
    text-decoration: none;
    font-weight: 500;
}

.solar-footer a:hover {
    text-decoration: underline;
}

/* ========== Scrollbar ========== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--solar-light);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--solar-gradient);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--solar-dark);
}

/* ========== Image Container ========== */
.solar-image-container {
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid var(--border-light);
    transition: all 0.3s ease;
}

.solar-image-container:hover {
    border-color: var(--solar-primary);
    box-shadow: var(--solar-shadow);
}

/* ========== Formula Box ========== */
.solar-formula-box {
    background: linear-gradient(135deg, #FFF9F5, #FFEFE6);
    border-left: 4px solid var(--solar-primary);
    padding: 1rem 1.5rem;
    border-radius: 0 12px 12px 0;
    margin: 0.5rem 0;
}

/* ========== Section Headers ========== */
.solar-subheader {
    color: var(--solar-primary);
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--solar-light);
    margin-top: 0;
}

.solar-subheader-icon {
    font-size: 1.5rem;
}

/* ========== Streamlit Containers as Cards ========== */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: white !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
    border: 1px solid var(--border-light) !important;
    transition: all 0.3s ease;
    margin-bottom: 1rem;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: var(--solar-shadow) !important;
    border-color: var(--solar-primary) !important;
    transform: translateY(-2px);
}

/* 내부 div의 border 제거 */
[data-testid="stVerticalBlockBorderWrapper"] > div {
    border: none !important;
}

/* File Uploader Styling */
[data-testid="stFileUploader"] section {
    background-color: var(--solar-light) !important;
    border: 2px dashed var(--solar-primary) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

[data-testid="stFileUploader"] section:hover {
    background-color: #FFE8D6 !important;
    border-color: var(--solar-dark) !important;
}

[data-testid="stFileUploader"] button {
    border-color: var(--solar-primary) !important;
    color: var(--solar-primary) !important;
}

/* ========== Problem Card ========== */
.solar-problem-card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    border: 1px solid var(--border-light);
    margin-bottom: 0.75rem;
    transition: all 0.3s ease;
}

.solar-problem-card:hover {
    border-color: var(--solar-primary);
    box-shadow: 0 4px 12px rgba(255, 107, 53, 0.15);
}

.solar-problem-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}

.solar-problem-number {
    background: var(--solar-gradient);
    color: white;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.9rem;
}

.solar-problem-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.85rem;
    color: var(--text-secondary);
}

/* ========== Hint Box ========== */
.solar-hint {
    background: linear-gradient(135deg, #FFF9E6, #FFF3D6);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-top: 0.75rem;
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
}

.solar-hint-icon {
    color: var(--solar-gold);
}
</style>
"""
