import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from flask import Flask, request, jsonify

from flask_cors import CORS  # Install: pip install Flask-CORS

app = Flask(__name__)
CORS(app)  # Simple usage (allows all origins - USE WITH CAUTION IN PRODUCTION)
# More specific configuration (recommended for production)
# cors = CORS(app, resources={r"/verify_token": {"origins": "http://localhost:8000"}})

# Firebase Admin SDK の初期化
cred = credentials.Certificate("/home/xtkd/torupati/gcloud_streamlit/my-cloud-run01-firebase-adminsdk-fbsvc-3f3ebbd466.json")
firebase_admin.initialize_app(cred)

@app.route('/verify_token', methods=['POST'])
def verify_token():
    print('verify', __file__)
    try:
        #id_token = request.json.get('token')
        id_token = request.get_json().get('idToken')
        print(f"{id_token=}")
        decoded_token = auth.verify_id_token(id_token)
        print(f"{decoded_token=}")
        uid = decoded_token['uid']
        return jsonify({'success': True, 'uid': uid})
    except auth.InvalidIdTokenError:
        print(auth.InvalidIdTokenError)
        return jsonify({'success': False, 'message': 'Invalid ID token'})
    except Exception as e:
        print(f"Exception {e=}")
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=8001)