import streamlit as st
import google.generativeai as genai

# ── page config 
st.set_page_config(
    page_title="CHORA · ጮራ",
    page_icon="🌅",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ──google generative ai client ─────────────────────────────────────────────────────────────
def ask_chora():
    try:
        return genai.GenerativeModel("gemini-pro")
    except Exception:
        st.error("Add your GOOGLE_API_KEY to .streamlit/secrets.toml")
        st.stop()

def ask_chora(prompt: str, system: str = "") -> str:
    client = ask_chora()
    sys = system or (
        "You are CHORA (ጮራ), an Ethiopian wellness companion. "
        "Give warm, culturally rooted wellness guidance grounded in Ethiopian food, "
        "lifestyle, tradition, and community. Always respond with empathy, keep language simple, "
        "and never diagnose — only raise awareness. Reference local Ethiopian foods "
        "like injera, teff, misir, gomen, ayib when relevant. Respond in 3-5 sentences."
    )
    msg = ask_chora().generate_content(
        model="gemini-pro",
        max_tokens=600,
        system=sys,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.choices[0].message

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.chora-hero {
    background: #1c1a28;
    border-radius: 16px;
    padding: 2rem 1.5rem 1.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.chora-title   { font-size: 2.8rem; font-weight: 600; color: #e8dff4; letter-spacing: 6px; margin: 0; }
.chora-amharic { font-size: 1.4rem; color: #9080c0; letter-spacing: 4px; margin: 4px 0 0; }
.chora-tagline { font-size: 0.78rem; color: #605878; letter-spacing: 2px; margin-top: 8px; }

.signal-response {
    background: #f0f8f0;
    border-left: 3px solid #639922;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #2a3a20;
}
.warn-response {
    background: #fdf4e8;
    border-left: 3px solid #d4881a;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #4a3010;
}
.step-label {
    font-size: 0.72rem;
    letter-spacing: 2px;
    color: #9080b0;
    text-transform: uppercase;
    margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)

# ── session state ─────────────────────────────────────────────────────────────
if "mode" not in st.session_state:
    st.session_state.mode = None

# ── hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chora-hero">
  <div class="chora-title">CHORA</div>
  <div class="chora-amharic">ጮራ</div>
  <div class="chora-tagline">your body is sending signals · let's decode them</div>
</div>
""", unsafe_allow_html=True)

# ── mode selector
if st.session_state.mode is None:
    st.markdown("<div class='step-label'>who are you?</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧒 child (5–12)",      use_container_width=True): st.session_state.mode = "child";   st.rerun()
        if st.button("👔 adult (25–60)",      use_container_width=True): st.session_state.mode = "adult";   st.rerun()
    with col2:
        if st.button("🧑 teenager (13–24)",   use_container_width=True): st.session_state.mode = "teen";    st.rerun()
        if st.button("👴 elderly (60+)",      use_container_width=True): st.session_state.mode = "elderly"; st.rerun()
    st.markdown("---")
    if st.button("🌾 farmer / rural mode", use_container_width=True):
        st.session_state.mode = "farmer"; st.rerun()
    st.stop()

# back button
if st.button("← back to home"):
    st.session_state.mode = None
    st.rerun()

mode = st.session_state.mode


# CHILD MODE
if mode == "child":
    st.markdown("### 🧒 hi there! welcome to CHORA")
    tab1, tab2 = st.tabs(["🩹 where does it hurt?", "🤔 body riddles"])

    with tab1:
        area = st.selectbox("where do you feel pain or discomfort?", [
            "select an area...", "head / headache", "eyes", "ears",
            "throat / neck", "chest", "stomach / tummy", "back",
            "arms or legs", "whole body feels tired",
        ])
        if area != "select an area...":
            duration = st.radio("how long?", ["just today", "a few days", "more than a week"], horizontal=True)
            if st.button("ask chora 🌿", key="child_hurt"):
                with st.spinner("chora is thinking..."):
                    resp = ask_chora(
                        f"A child says they have pain in: {area}, for: {duration}. "
                        "In simple, kind language for a child, explain possible reasons and what to tell a parent. "
                        "Never diagnose. Be warm and reassuring.",
                        system="You are CHORA, a kind Ethiopian wellness guide for children. "
                               "Speak gently and simply. Always recommend telling a parent or trusted adult."
                    )
                st.markdown(f"<div class='signal-response'>🌿 {resp}</div>", unsafe_allow_html=True)
                st.info("💛 always tell a parent or trusted adult when you feel pain!")

    with tab2:
        riddles = [
            ("I pump blood to every part of your body. I beat about 100,000 times a day. What am I?", "heart"),
            ("I help you breathe. You have two of me. I fill with air like a balloon. What am I?", "lungs"),
            ("I am the control center of your body. I help you think, feel, and remember. What am I?", "brain"),
            ("I break down the food you eat. I can make growling sounds when you're hungry. What am I?", "stomach"),
            ("I clean your blood. You have two of me shaped like beans. What am I?", "kidneys"),
        ]
        if "riddle_idx" not in st.session_state:
            st.session_state.riddle_idx = 0
        idx = st.session_state.riddle_idx % len(riddles)
        question, answer = riddles[idx]
        st.markdown(f"**{question}**")
        guess = st.text_input("your answer:", key=f"riddle_{idx}").lower().strip()
        if guess:
            if answer in guess:
                st.success(f"🎉 yes! the answer is **{answer}**!")
            else:
                st.error("not quite — try again!")
        if st.button("next riddle ➡️"):
            st.session_state.riddle_idx += 1
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TEEN MODE
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "teen":
    st.markdown("### 🧑 teen wellness")
    tab1, tab2 = st.tabs(["📡 body signals", "🧠 mental health"])

    with tab1:
        feeling = st.text_area("how are you feeling? describe it:", placeholder="e.g. tired all the time, chest feels heavy, can't focus...")
        if st.button("decode my signal 🔍") and feeling:
            with st.spinner("decoding..."):
                resp = ask_chora(
                    f"A teenager in Ethiopia describes: '{feeling}'. "
                    "Explain possible body or emotional signals — stress, sleep, nutrition, emotional pressure. "
                    "Never diagnose. Give 2-3 possible explanations and 1 practical Ethiopian lifestyle suggestion."
                )
            st.markdown(f"<div class='signal-response'>📡 {resp}</div>", unsafe_allow_html=True)

    with tab2:
        mood = st.select_slider("how are you feeling today?", options=[
            "😔 really struggling", "😟 not great", "😐 okay", "🙂 pretty good", "😊 great!"
        ])
        struggles = st.multiselect("what's weighing on you?", [
            "school pressure", "family stress", "friend drama / loneliness",
            "body image", "sleep problems", "future / career anxiety", "other"
        ])
        if st.button("get my wellness guide 🌿") and struggles:
            with st.spinner("..."):
                resp = ask_chora(
                    f"A teenager in Ethiopia is feeling: {mood}. "
                    f"They are struggling with: {', '.join(struggles)}. "
                    "Give 3 warm, practical, culturally Ethiopian wellness tips. Be like a wise older sibling."
                )
            st.markdown(f"<div class='signal-response'>🌿 {resp}</div>", unsafe_allow_html=True)

        free_text = st.text_area("write anything you're feeling:", placeholder="I've been feeling...")
        if st.button("talk to chora 💬") and free_text:
            with st.spinner("..."):
                resp = ask_chora(free_text,
                    system="You are CHORA, a caring Ethiopian wellness companion for teenagers. "
                           "Respond like a warm, wise older sibling. Be supportive and non-judgmental. 4 sentences."
                )
            st.markdown(f"<div class='signal-response'>💛 {resp}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ADULT MODE
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "adult":
    st.markdown("### 👔 adult wellness")
    tab1, tab2 = st.tabs(["📡 body signals", "🍲 nutrition advisor"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            condition = st.selectbox("known health condition:", [
                "none / general wellness", "diabetes type 2", "hypertension",
                "digestive issues", "chronic fatigue", "heart concerns"
            ])
        with col2:
            age_range = st.selectbox("age range:", ["25–35", "35–45", "45–55", "55–65"])
        symptom = st.text_area("describe your symptoms:", placeholder="e.g. feel heavy after eating, tired easily, afternoon headaches...")
        if st.button("translate my body signal 📡") and symptom:
            with st.spinner("analyzing..."):
                resp = ask_chora(
                    f"An Ethiopian adult aged {age_range} with {condition} describes: '{symptom}'. "
                    "Explain possible body signals. Reference Ethiopian diet and lifestyle. "
                    "Give 2 prevention tips using local foods. Never diagnose. Recommend a doctor if needed."
                )
            st.markdown(f"<div class='signal-response'>📡 {resp}</div>", unsafe_allow_html=True)

    with tab2:
        health_goal = st.selectbox("your health goal:", [
            "general wellness", "manage diabetes", "lower blood pressure",
            "boost immunity", "increase energy", "improve digestion"
        ])
        meal_pref = st.multiselect("your regular meals:", [
            "injera & wot", "fasting food (tsom)", "meat-based", "vegetarian",
            "dairy (ayib, yogurt)", "street food", "mixed"
        ])
        if st.button("build my nutrition plan 🍲") and meal_pref:
            with st.spinner("building your plan..."):
                resp = ask_chora(
                    f"An Ethiopian adult wants to: {health_goal}. "
                    f"They regularly eat: {', '.join(meal_pref)}. "
                    "Create a practical 3-day Ethiopian meal plan using local foods. "
                    "Explain benefits and what to add or reduce."
                )
            st.markdown(f"<div class='signal-response'>🍲 {resp}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ELDERLY MODE
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "elderly":
    st.markdown("### 👴 welcome, elder")
    tab1, tab2 = st.tabs(["🩺 body signals", "💛 emotional care"])

    with tab1:
        pain_area = st.selectbox("where do you feel discomfort?", [
            "select...", "head", "chest", "stomach", "back", "legs / joints",
            "whole body feels weak", "trouble breathing", "dizziness", "other"
        ])
        description = st.text_area("describe in your own words:", placeholder="e.g. my knees hurt when I walk...")
        if st.button("ask chora 🌿") and pain_area != "select...":
            with st.spinner("..."):
                resp = ask_chora(
                    f"An elderly Ethiopian person has discomfort in: {pain_area}. "
                    f"They describe: '{description}'. "
                    "Gently explain possible reasons in simple language. "
                    "Suggest 1-2 gentle home care steps using Ethiopian traditional knowledge. "
                    "Always kindly recommend seeing a doctor if needed.",
                    system="You are CHORA, speaking warmly to an Ethiopian elder. "
                           "Speak slowly, clearly, with great respect. Use simple words. Never cause alarm."
                )
            st.markdown(f"<div class='signal-response'>🌿 {resp}</div>", unsafe_allow_html=True)

    with tab2:
        feeling = st.radio("how are you feeling today?", [
            "😊 content and at peace", "😐 okay, just quiet",
            "😔 feeling lonely", "😟 worried or stressed", "😢 sad today"
        ])
        if st.button("talk to chora 💛"):
            with st.spinner("..."):
                resp = ask_chora(
                    f"An elderly Ethiopian person says they are feeling: {feeling}. "
                    "Respond with warmth, wisdom, and comfort. "
                    "Reference Ethiopian values of community, faith, and family. "
                    "Offer 1 gentle suggestion to feel better.",
                    system="You are CHORA, speaking to an Ethiopian elder with deep respect. "
                           "Be like a caring grandchild. Speak with love and wisdom."
                )
            st.markdown(f"<div class='signal-response'>💛 {resp}</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FARMER MODE
# ══════════════════════════════════════════════════════════════════════════════
elif mode == "farmer":
    st.markdown("### 🌾 ጤና ሙሉ ነው — health is wealth")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌿 local remedies", use_container_width=True):
            with st.spinner("..."):
                resp = ask_chora("What local Ethiopian plants, spices, and foods can farmers use for natural health and immunity? Simple language for rural Ethiopia.")
            st.markdown(f"<div class='signal-response'>{resp}</div>", unsafe_allow_html=True)

        if st.button("🩺 describe a symptom", use_container_width=True):
            st.session_state["farmer_sym_open"] = True

    with col2:
        if st.button("🌾 food guide", use_container_width=True):
            with st.spinner("..."):
                resp = ask_chora("Nutrition advice for Ethiopian farmers. Focus on teff, injera, legumes, local vegetables. Simple daily eating guide for energy and strength.")
            st.markdown(f"<div class='signal-response'>{resp}</div>", unsafe_allow_html=True)

        if st.button("👴 traditional wisdom", use_container_width=True):
            with st.spinner("..."):
                resp = ask_chora("Share Ethiopian cultural wellness wisdom passed through generations. Traditional practices farmers already know.")
            st.markdown(f"<div class='signal-response'>{resp}</div>", unsafe_allow_html=True)

    if st.session_state.get("farmer_sym_open"):
        symptom = st.text_input("describe your symptom:")
        if symptom and st.button("ask chora", key="farmer_ask"):
            with st.spinner("..."):
                resp = ask_chora(f"A farmer in rural Ethiopia has: {symptom}. Simple guidance on what it may be and when to visit a health center.")
            st.markdown(f"<div class='signal-response'>{resp}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🚨 emergency — CPR basics")
    if st.button("show CPR steps", use_container_width=True):
        with st.spinner("..."):
            resp = ask_chora("Simple CPR instructions for someone with no medical training in rural Ethiopia. Step by step. What to do while waiting for help.")
        st.markdown(f"<div class='warn-response'>🚨 {resp}</div>", unsafe_allow_html=True)


# ── footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; font-size:0.75rem; color:#9080b0; line-height:2;'>
    CHORA · ጮራ · 2026<br>
    <span style='opacity:0.5;'>built for ethiopia · accessing information is healing</span>
</div>
""", unsafe_allow_html=True)
