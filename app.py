import streamlit as st

st.title("Hello World!")
st.write("This is a Streamlit app running in Docker.")
st.write("This is a sample Streamlit app running on Cloud Run.")

x = st.slider("Select a value", 0, 100)
st.write(f"You selected: {x}")
