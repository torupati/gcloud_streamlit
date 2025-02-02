import streamlit as st

st.title("Hello Streamlit!")

st.write("This is a sample Streamlit app running on Cloud Run.")

x = st.slider("Select a value", 0, 100)
st.write(f"You selected: {x}")
