import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

if not firebase_admin._apps:  # Check if the default app exists
    cred = credentials.ApplicationDefault()
    #cred = credentials.Certificate(st.secrets["firebase_credentials"])
    firebase_admin.initialize_app(cred)

def authenticate_user(email, password):
    # クライアント側で Firebase Authentication を使用して認証し、
    # ID トークンを取得する (ここでは省略)
    # ...

    # ID トークンを検証する (ここでは省略)
    # ...

    print(f"get user by {email=}")
    try:
        user = auth.get_user_by_email(email)
        st.write(f"User: {user.uid}")
        return user
    except auth.UserNotFoundError:
        return None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None


st.title("Firebase Authentication with Streamlit")

if "user" not in st.session_state:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = authenticate_user(email, password)
            if user:
                st.session_state.user = user
                st.success("Login successful!")
            else:
                st.error("Invalid email or password")

    
else:
        st.write(f"Welcome, {st.session_state.user.email}!")
        if st.button("Logout"):
            del st.session_state.user
            st.rerun()
