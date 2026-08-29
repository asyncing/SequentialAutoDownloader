import streamlit as st
import time

st.title("Streamlit Env Test")

with st.spinner("Testing..."):
    time.sleep(5)

st.success("Done!")
