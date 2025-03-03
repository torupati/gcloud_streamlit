import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

if not firebase_admin._apps:  # Check if the default app exists
    cred = credentials.ApplicationDefault()
    #cred = credentials.Certificate(st.secrets["firebase_credentials"])
    firebase_admin.initialize_app(cred)


def login():
    email = st.text_input("mail address")
    password = st.text_input("password", type="password")
    # Get and verty token in client with Firebase Authentication
    if st.button("Login"):
        try:
            user = auth.get_user_by_email(email) # unsecure
            #decoded_token = auth.verify_id_token(token)
            #uid = decoded_token['uid']
            #user = auth.get_user(uid)
            st.session_state.user = user
            st.success(f"Login Success! {user.uid=}")
        except auth.UserNotFoundError:
            st.error("User Not Found")
        except Exception as e:
            st.error(f"Error{e=}")


def logout():
    if st.button("Logout"):
        st.session_state.pop("user", None)
        st.success("Logout")

def main():
    if "user" not in st.session_state:
        login()
    else:
        st.write(f"Welcom {st.session_state.user.email}")
        logout()
        st.write("Now you are logged in")

if __name__ == "__main__":
    main()
