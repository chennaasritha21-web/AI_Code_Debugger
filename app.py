import os
import json
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
from langchain_ollama import ChatOllama

st.set_page_config(page_title="Code Explainer & Fixer", page_icon="🧩")
st.title("🐛 DebugMate")

load_dotenv()
API_KEY = os.getenv("OLLAMA_API_KEY")

if not API_KEY:
    st.error("❌ Missing Ollama API key. Add OLLAMA_API_KEY to your .env file.")
    st.stop()

HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

if "history" not in st.session_state:
    st.session_state.history = load_history()

# --- Sidebar: selections are read fresh every rerun ---
with st.sidebar:
    st.header("⚙️ Settings")

    mode = st.radio(
        "What do you want to do?",
        ["Explain working code", "Fix broken code", "Code Converter"],
        key="mode_select"
    )

    detail_level = st.radio(
        "Explanation style",
        ["Detailed", "Short summary", "Explain like I'm a beginner"],
        key="detail_select"
    )

    target_language = None
    if mode == "Code Converter":
        target_language = st.selectbox(
            "Convert to which language?",
            ["Python", "Java", "C", "C++", "JavaScript", "C#"],
            key="lang_select"
        )

    st.subheader("📅 Filter history by date")
    all_dates = sorted(set(e["date"][:10] for e in st.session_state.history), reverse=True)
    selected_date = st.selectbox("Show history from:", ["All"] + all_dates, key="date_select")

    if st.button("Clear history"):
        st.session_state.history = []
        save_history(st.session_state.history)
        st.rerun()

code_input = st.text_area("Paste your code here", height=250, key="code_box")
run_button = st.button("Run")

if run_button:
    if not code_input.strip():
        st.warning("Please paste some code first.")
        st.stop()

    # Read current selections directly from session_state to guarantee freshness
    current_mode = st.session_state.mode_select
    current_detail = st.session_state.detail_select

    if current_detail == "Detailed":
        style_instruction = "Give a detailed, line-by-line explanation, covering every statement thoroughly."
    elif current_detail == "Short summary":
        style_instruction = "Give a SHORT summary in 2-3 sentences maximum. Do not explain line by line."
    else:
        style_instruction = "Explain it very simply, as if teaching a complete beginner with no jargon."

    if current_mode == "Explain working code":
        prompt = f"""You are an expert programmer. Explain the following code.

INSTRUCTION: {style_instruction}

CODE:
{code_input}
"""
    elif current_mode == "Fix broken code":
        prompt = f"""You are an expert programmer. First, carefully check if the following code is actually correct and bug-free.

If the code is correct and works as intended, say so clearly and explain why it's correct. Do not invent a fake problem.

If the code does have a genuine bug or error, respond in exactly these three sections:

### ❌ Problem
Identify what is wrong with the code and explain why it is wrong.

### ✅ Fixed Code
Give the corrected, working version of the code.

### 💡 Why This Works
INSTRUCTION: {style_instruction}
Explain why the fix solves the problem, and why the original approach failed.

CODE:
{code_input}
"""
    else:  # Code Converter
        current_lang = st.session_state.lang_select
        prompt = f"""You are an expert programmer. Convert the following code into {current_lang}.

Respond in exactly these two sections:

### 🔄 Converted Code ({current_lang})
Give the complete, working {current_lang} version of the code.

### 📝 Key Differences
INSTRUCTION: {style_instruction}
Explain the main syntax or language differences between the original code and the {current_lang} version.

CODE:
{code_input}
"""

    llm = ChatOllama(
        model="gpt-oss:120b-cloud",
        base_url="https://ollama.com",
        client_kwargs={"headers": {"Authorization": f"Bearer 964cf50bebb24cebaeed604a32336890._M9Q6aQpXnws1MJXRFd4CTz6"}},
    )

    with st.spinner("Analyzing your code..."):
        try:
            response = llm.invoke(prompt)
        except Exception as e:
            st.error(f"Error calling the model: {e}")
            st.stop()

    result = response.content

    st.session_state.history.append({
        "mode": current_mode,
        "code": code_input,
        "result": result,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    save_history(st.session_state.history)

st.divider()
filtered_history = st.session_state.history
if st.session_state.get("date_select", "All") != "All":
    filtered_history = [e for e in st.session_state.history if e["date"].startswith(st.session_state.date_select)]

for entry in reversed(filtered_history):
    with st.container(border=True):
        st.caption(f"{entry['date']} | Mode: {entry['mode']}")
        st.code(entry["code"], language="python")
        st.markdown(entry["result"])