import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate("/home/xtkd/torupati/gcloud_streamlit/my-cloud-run01-firebase-adminsdk-fbsvc-3f3ebbd466.json")
firebase_admin.initialize_app(cred)

def authenticate_user(email, password):
    try:
        user = auth.get_user_by_email(email)
        print(f"get user by email: {user=}")
        if user:
            # need to check by ID token
            return user
        else:
            return None
    except auth.UserNotFoundError:
        print(f"User not found")
        return None
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return None

def create_user(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def delete_user(uid):
    try:
        auth.delete_user(uid)
        print(f"Successfully deleted user: {uid}")
        return True
    except auth.UserNotFoundError:
        print(f"User not found: {uid}")
        return False
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False

def test_add_and_delete_authenticate_user():
    email = "newuser@example.com"
    password = "password"
    user = authenticate_user(email, password)

    if user:
        print(f"User authenticated: {user.uid}")
    else:
        print("Invalid email or password")

if __name__ == '__main__':
    _email = "newuser@example.com"
    pswd = "password"    
    print(f"authenticate user{_email=} {pswd=}")
    usr = authenticate_user(email=_email, password=pswd)
    if usr is not None:
        delete_user(usr.uid)
