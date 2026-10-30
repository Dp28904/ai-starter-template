import json
import pandas as pd
import streamlit as st
from pydantic import BaseModel
from core import is_safe_url, fetch_page
from llm import ask_json
from prompts import SYSTEM, task_prompt

st.set_page_config(page_title="AI Tool", page_icon="🤖", layout="wide")
st.title("🤖 AI Tool")
st.caption("Built for agencies: fast, reliable, white-label ready.")

# ---- 1. Define the output schema (change per problem) ----
class Result(BaseModel):
    score: int
    summary: str
    recommendations: list[str]

# ---- 2. Input ----
mode = st.radio("Input", ["URL", "CSV upload", "Text"], horizontal=True)
if mode == "URL":
    user_input = st.text_input("Website URL", placeholder="https://example.com").strip()
elif mode == "CSV upload":
    user_input = st.file_uploader("Upload CSV", type="csv")
else:
    user_input = st.text_area("Paste text", max_chars=5000).strip()

# ---- 3. Run ----
@st.cache_data(show_spinner=False, ttl=3600)          # caching → saves tokens
def run_one(data: str) -> dict:
    prompt = task_prompt(data, "Analyse this and give recommendations.",
                         '{"score": 0-100, "summary": "...", "recommendations": ["..."]}')
    return ask_json(SYSTEM, prompt, Result).model_dump()

if st.button("Run", type="primary"):
    if not user_input:
        st.warning("Please provide an input first."); st.stop()
    try:
        with st.spinner("Working..."):
            if mode == "URL":
                if not is_safe_url(user_input):
                    st.error("Enter a valid public http(s) URL."); st.stop()
                page = fetch_page(user_input)
                result = run_one(json.dumps(page))
            elif mode == "CSV upload":
                df = pd.read_csv(user_input)
                if df.empty:
                    st.error("The CSV is empty."); st.stop()
                st.dataframe(df.head(50))
                result = run_one(df.head(50).to_csv(index=False))   # limit rows
            else:
                result = run_one(user_input)

        # ---- 4. Output ----
        st.metric("Score", f"{result['score']}/100")
        st.write(result["summary"])
        for r in result["recommendations"]:
            st.write("•", r)
        st.download_button("Download JSON", json.dumps(result, indent=2), "result.json")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
