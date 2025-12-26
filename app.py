import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="SaaS Idea Analyzer",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 SaaS Business Idea Analyzer")
st.write("Enter your SaaS idea and get competitors, marketing hooks, and a brutal critique.")

# -----------------------------
# API KEY
# -----------------------------
# Recommended: set this as an environment variable
# export GEMINI_API_KEY="your_api_key_here"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY environment variable not set")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# INPUT
# -----------------------------
idea = st.text_input(
    "💡 SaaS Business Idea",
    placeholder="e.g. AI-powered payroll benchmarking platform for startups"
)

analyze_btn = st.button("Analyze")

# -----------------------------
# ANALYSIS
# -----------------------------
if analyze_btn:
    if not idea.strip():
        st.warning("Please enter a SaaS idea.")
    else:
        with st.spinner("Analyzing your idea brutally... 😈"):
            prompt = f"""
You are a brutally honest SaaS investor.

Analyze the following SaaS idea:

"{idea}"

Return the response STRICTLY in this format:

Competitors:
1. Competitor Name - short reason
2. Competitor Name - short reason
3. Competitor Name - short reason

Marketing Hooks:
1. Hook
2. Hook
3. Hook

Brutal Critique:
A brutally honest critique in 4–6 sentences.
"""

            response = model.generate_content(prompt)
            text = response.text

        # -----------------------------
        # PARSING
        # -----------------------------
        try:
            competitors_section = text.split("Marketing Hooks:")[0].split("Competitors:")[1]
            hooks_section = text.split("Brutal Critique:")[0].split("Marketing Hooks:")[1]
            critique = text.split("Brutal Critique:")[1].strip()

            competitors = [
                c.split(".", 1)[1].strip()
                for c in competitors_section.strip().split("\n") if "." in c
            ]

            hooks = [
                h.split(".", 1)[1].strip()
                for h in hooks_section.strip().split("\n") if "." in h
            ]

            df = pd.DataFrame({
                "Potential Competitors": competitors,
                "Marketing Hooks": hooks
            })

            # -----------------------------
            # OUTPUT
            # -----------------------------
            st.subheader("📊 Competitive & Marketing Analysis")
            st.table(df)

            st.subheader("🔥 Brutal Critique")
            st.write(critique)

        except Exception:
            st.error("Failed to parse Gemini response. Raw output below:")
            st.text(text)
