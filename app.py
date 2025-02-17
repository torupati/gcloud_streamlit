import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# login form
if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "password":  # authentification
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")

if st.session_state.logged_in:
    st.title("Welcome!")
    st.write("This content is only visible to logged-in users.")
    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a demo above.")

    st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
        #st.experimental_rerun was deprecated in version 1.27.0. Use st.rerun instead