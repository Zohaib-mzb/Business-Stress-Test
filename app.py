import streamlit as st
import requests
import json
import time

# ── PAGE CONFIG ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Business Idea Stress Test",
    page_icon="🔥",
    layout="wide"
)

# ── YOUR N8N PRODUCTION WEBHOOK URL ─────────────────────────────
N8N_WEBHOOK_URL = "PASTE_YOUR_PRODUCTION_WEBHOOK_URL_HERE"

# ── CUSTOM CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0F1117; }
    
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 8px;
    }
    .sub-title {
        font-size: 16px;
        color: #9CA3AF;
        text-align: center;
        margin-bottom: 40px;
    }
    .score-box {
        background: linear-gradient(135deg, #1F2937, #111827);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        border: 1px solid #374151;
    }
    .score-number {
        font-size: 72px;
        font-weight: 900;
        line-height: 1;
    }
    .verdict-badge {
        display: inline-block;
        padding: 8px 20px;
        border-radius: 99px;
        font-size: 14px;
        font-weight: 600;
        margin-top: 12px;
    }
    .card {
        background-color: #1F2937;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid #374151;
    }
    .fatal-tag {
        background-color: #7F1D1D;
        color: #FCA5A5;
        padding: 3px 10px;
        border-radius: 99px;
        font-size: 11px;
        font-weight: 600;
    }
    .serious-tag {
        background-color: #78350F;
        color: #FCD34D;
        padding: 3px 10px;
        border-radius: 99px;
        font-size: 11px;
        font-weight: 600;
    }
    .moderate-tag {
        background-color: #1E3A5F;
        color: #93C5FD;
        padding: 3px 10px;
        border-radius: 99px;
        font-size: 11px;
        font-weight: 600;
    }
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #F9FAFB;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #374151;
    }
    .insight-box {
        background: linear-gradient(135deg, #064E3B, #065F46);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #059669;
        margin-bottom: 16px;
    }
    .killer-box {
        background: linear-gradient(135deg, #1E1B4B, #312E81);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #6366F1;
        margin-bottom: 16px;
    }
    .competitor-chip {
        display: inline-block;
        background-color: #374151;
        border-radius: 8px;
        padding: 8px 14px;
        margin: 4px;
        font-size: 13px;
        color: #E5E7EB;
    }
    stTextArea textarea {
        background-color: #1F2937 !important;
        color: #F9FAFB !important;
        border: 1px solid #374151 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────
st.markdown('<div class="main-title">🔥 Business Idea Stress Test</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Drop your startup idea. 4 AI agents will '
    'destroy it — then show you how to fix it.</div>',
    unsafe_allow_html=True
)

# ── INPUT FORM ───────────────────────────────────────────────────
col_left, col_center, col_right = st.columns([1, 3, 1])

with col_center:
    idea = st.text_area(
        "Your startup idea",
        placeholder="Describe your startup idea in 2-3 sentences...",
        height=120,
        label_visibility="collapsed"
    )

    run_button = st.button(
        "🔥 Stress Test This Idea",
        type="primary",
        use_container_width=True
    )

# ── PROCESS AND DISPLAY ──────────────────────────────────────────
if run_button:
    if not idea or len(idea.strip()) < 20:
        st.error("Please describe your idea in at least a few sentences.")
        st.stop()

    # Progress display
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            s1 = st.empty()
            s1.info("🤔 Agent 1\nThe Skeptic\nAnalysing...")
        with col2:
            s2 = st.empty()
            s2.warning("⏳ Agent 2\nThe Researcher\nWaiting...")
        with col3:
            s3 = st.empty()
            s3.warning("⏳ Agent 3\nThe Fixer\nWaiting...")
        with col4:
            s4 = st.empty()
            s4.warning("⏳ Agent 4\nThe Verdict\nWaiting...")

    try:
        # Call n8n webhook
        with st.spinner("Running 4 AI agents on your idea..."):
            response = requests.post(
                N8N_WEBHOOK_URL,
                json={"idea": idea.strip()},
                timeout=120
            )

        if response.status_code != 200:
            st.error(f"Pipeline error: {response.status_code} — {response.text[:200]}")
            st.stop()

        data = response.json()
        
        # Handle if n8n returns a list
        if isinstance(data, list):
            data = data[0]

        # Update progress to all done
        with progress_container.container():
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.success("✅ Agent 1\nThe Skeptic\nDone")
            with col2:
                st.success("✅ Agent 2\nThe Researcher\nDone")
            with col3:
                st.success("✅ Agent 3\nThe Fixer\nDone")
            with col4:
                st.success("✅ Agent 4\nThe Verdict\nDone")

        st.markdown("---")

        # ── VERDICT SECTION ──────────────────────────────────────
        score = data.get('verdict', {}).get('score', 0)
        label = data.get('verdict', {}).get('label', 'Unknown')
        reasoning = data.get('verdict', {}).get('reasoning', '')
        killer = data.get('verdict', {}).get('killer_insight', '')
        best_version = data.get('verdict', {}).get('best_version', '')

        # Score colour
        if score >= 7:
            score_color = "#10B981"
            badge_bg = "#064E3B"
            badge_color = "#6EE7B7"
        elif score >= 4:
            score_color = "#F59E0B"
            badge_bg = "#78350F"
            badge_color = "#FCD34D"
        else:
            score_color = "#EF4444"
            badge_bg = "#7F1D1D"
            badge_color = "#FCA5A5"

        st.markdown(
            f'<div class="section-header">⚖️ Final Verdict</div>',
            unsafe_allow_html=True
        )

        v1, v2 = st.columns([1, 2])

        with v1:
            st.markdown(f"""
            <div class="score-box">
                <div style="color: #9CA3AF; font-size: 13px; 
                     margin-bottom: 8px; text-transform: uppercase; 
                     letter-spacing: 2px;">Viability Score</div>
                <div class="score-number" 
                     style="color: {score_color};">{score}/10</div>
                <div>
                    <span class="verdict-badge" 
                          style="background-color: {badge_bg}; 
                                 color: {badge_color};">
                        {label}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with v2:
            st.markdown(f"""
            <div class="card">
                <div style="color: #9CA3AF; font-size: 12px; 
                     text-transform: uppercase; letter-spacing: 1px; 
                     margin-bottom: 8px;">Assessment</div>
                <div style="color: #F9FAFB; font-size: 15px; 
                     line-height: 1.7;">{reasoning}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="killer-box">
                <div style="color: #A5B4FC; font-size: 12px; 
                     font-weight: 600; text-transform: uppercase; 
                     letter-spacing: 1px; margin-bottom: 8px;">
                    ⚡ The Killer Insight
                </div>
                <div style="color: #E0E7FF; font-size: 15px; 
                     line-height: 1.7;">{killer}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ── THREE COLUMNS: SKEPTIC / RESEARCH / FIXER ────────────
        left_col, right_col = st.columns(2)

        with left_col:
            st.markdown(
                '<div class="section-header">💀 The Skeptic\'s Case</div>',
                unsafe_allow_html=True
            )

            objections = data.get('skeptic', {}).get('objections', [])
            for obj in objections:
                severity = obj.get('severity', 'Moderate')
                tag_class = {
                    'Fatal': 'fatal-tag',
                    'Serious': 'serious-tag',
                    'Moderate': 'moderate-tag'
                }.get(severity, 'moderate-tag')

                st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: 
                         space-between; align-items: center; 
                         margin-bottom: 8px;">
                        <span style="color: #F9FAFB; font-weight: 600; 
                              font-size: 14px;">{obj.get('title','')}</span>
                        <span class="{tag_class}">{severity}</span>
                    </div>
                    <div style="color: #9CA3AF; font-size: 13px; 
                         line-height: 1.6;">
                        {obj.get('detail','')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with right_col:
            st.markdown(
                '<div class="section-header">🛡️ The Fixer\'s Counters</div>',
                unsafe_allow_html=True
            )

            counters = data.get('fixer', {}).get('counters', [])
            for counter in counters:
                st.markdown(f"""
                <div class="card">
                    <div style="color: #10B981; font-weight: 600; 
                         font-size: 14px; margin-bottom: 8px;">
                        ↳ {counter.get('objection_title','')}
                    </div>
                    <div style="color: #D1FAE5; font-size: 13px; 
                         line-height: 1.6; margin-bottom: 10px;">
                        {counter.get('counter_strategy','')}
                    </div>
                    <div style="color: #6EE7B7; font-size: 12px; 
                         border-top: 1px solid #374151; 
                         padding-top: 8px; margin-top: 4px;">
                        📌 Example: {counter.get('example','')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # ── RESEARCH SECTION ─────────────────────────────────────
        st.markdown(
            '<div class="section-header">🔍 Market Research</div>',
            unsafe_allow_html=True
        )

        r1, r2 = st.columns([2, 1])

        with r1:
            market_insight = data.get(
                'research', {}
            ).get('market_insight', '')
            biggest_threat = data.get(
                'research', {}
            ).get('biggest_threat', '')

            st.markdown(f"""
            <div class="insight-box">
                <div style="color: #6EE7B7; font-size: 12px; 
                     font-weight: 600; text-transform: uppercase; 
                     letter-spacing: 1px; margin-bottom: 8px;">
                    Market Insight
                </div>
                <div style="color: #D1FAE5; font-size: 14px; 
                     line-height: 1.7;">{market_insight}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="card">
                <div style="color: #FCA5A5; font-size: 12px; 
                     font-weight: 600; text-transform: uppercase; 
                     letter-spacing: 1px; margin-bottom: 8px;">
                    ⚠️ Biggest Competitive Threat
                </div>
                <div style="color: #FEE2E2; font-size: 14px; 
                     line-height: 1.7;">{biggest_threat}</div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            competitors = data.get(
                'research', {}
            ).get('competitors', [])
            st.markdown(
                '<div style="color: #F9FAFB; font-weight: 600; '
                'margin-bottom: 12px;">Competitors Found</div>',
                unsafe_allow_html=True
            )
            for comp in competitors:
                status = comp.get('status', 'Active')
                status_color = {
                    'Active': '#10B981',
                    'Failed': '#EF4444',
                    'Acquired': '#F59E0B'
                }.get(status, '#9CA3AF')

                st.markdown(f"""
                <div class="card" style="margin-bottom: 10px;">
                    <div style="color: #F9FAFB; font-weight: 600; 
                         font-size: 13px;">{comp.get('name','')}</div>
                    <div style="color: #9CA3AF; font-size: 12px; 
                         margin-top: 4px;">
                        {comp.get('description','')}
                    </div>
                    <div style="color: {status_color}; font-size: 11px; 
                         margin-top: 6px; font-weight: 600;">
                        ● {status}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # ── BEST VERSION ─────────────────────────────────────────
        st.markdown(
            '<div class="section-header">💡 Best Version of This Idea</div>',
            unsafe_allow_html=True
        )
        st.markdown(f"""
        <div class="insight-box">
            <div style="color: #D1FAE5; font-size: 15px; 
                 line-height: 1.8;">{best_version}</div>
        </div>
        """, unsafe_allow_html=True)

    except requests.exceptions.Timeout:
        progress_container.empty()
        st.error(
            "The analysis took too long. n8n is processing — "
            "try again in 30 seconds."
        )
    except Exception as e:
        progress_container.empty()
        st.error(f"Something went wrong: {str(e)}")