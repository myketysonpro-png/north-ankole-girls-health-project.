import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Young Girls' Health Project", page_icon="🌱", layout="wide")
st.title("North Ankole Diocese Mothers' Union Mission Hospital")
st.subheader("Young Girls' Health Project — Indicator Dashboard")
st.warning("Prototype only. Default records are synthetic. Do not upload names, phone numbers, patient identifiers, or identifiable/sensitive personal data.")

DEFAULT_FILE = Path(__file__).parent / "data" / "sample_indicators.csv"

@st.cache_data
def load_default():
    return pd.read_csv(DEFAULT_FILE)

uploaded = st.file_uploader("Upload an aggregate indicator CSV (optional)", type=["csv"])
try:
    df = pd.read_csv(uploaded) if uploaded is not None else load_default()
except Exception as exc:
    st.error(f"Could not read the CSV: {exc}")
    st.stop()

required = {"month", "school_health_sessions", "girls_reached", "counselling_sessions", "referrals"}
if not required.issubset(df.columns):
    st.error("CSV must contain: " + ", ".join(sorted(required)))
    st.stop()

for col in required - {"month"}:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

a, b, c, d = st.columns(4)
a.metric("Girls reached", f"{int(df['girls_reached'].sum()):,}")
b.metric("School health sessions", f"{int(df['school_health_sessions'].sum()):,}")
c.metric("Counselling sessions", f"{int(df['counselling_sessions'].sum()):,}")
d.metric("Referrals recorded", f"{int(df['referrals'].sum()):,}")
st.caption("Default figures are illustrative synthetic data, not actual project results.")

left, right = st.columns(2)
with left:
    st.plotly_chart(px.bar(df, x="month", y="girls_reached", title="Girls reached by month"), use_container_width=True)
with right:
    activity = df.melt(id_vars="month", value_vars=["school_health_sessions", "counselling_sessions", "referrals"], var_name="indicator", value_name="count")
    st.plotly_chart(px.line(activity, x="month", y="count", color="indicator", markers=True, title="Activities and referrals by month"), use_container_width=True)

st.subheader("Indicator data")
st.dataframe(df, use_container_width=True, hide_index=True)
st.download_button("Download current data as CSV", df.to_csv(index=False).encode("utf-8"), "project_indicators.csv", "text/csv")
st.info("Before using real operational data, obtain facility approval, define access controls and retention rules, and use aggregate or properly de-identified information.")