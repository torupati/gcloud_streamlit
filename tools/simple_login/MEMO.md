Vite high speed development server, build tool. Fronend dev.
Based on Node.js
load from file .env 

Install Vite.

npm install vite --save-dev

- Start server. 

```
npx vite
```

Build

npx vite build

# はじめに

Firebase で認証を行うWEBを作ってみたくて方法を調べています。なんとなく一つ動いたのでなんなくの状態ですがメモしておきます。

- Firebase側
- ローカルでfrontend のサーバを動かす

# 内容

## Firebase 

Firebase でプロジェクトを作ります。私の場合は、もともとあったGCPのプロジェクトをそのまま使っています。

契約は
- 無料（月額 0 ドル）Spark プラン
- 従量制Blaze プラン
の２種類ありますが、私は後者で使っています。
違いは、

 >拡張して追加の Google Cloud サービスを使用

で、Google Cloud のストレージやサーバレスなどと結合させたいなーと思っています。今は何をしていませんが。
App Hosting は　5　GB/月までは無料(その後は $0.15/GB)、ストレージも5　GB/月までは無料(その後は $0.10/GB)です。

https://firebase.google.com/pricing?hl=ja

### コンソールで確認できること

https://console.firebase.google.com/

にログインし、プロジェクトを選択します。ここで新規作成できます。私の場合は、既存のGoogle Cloud のprojectを利用しています。

**Authentification のページから「ユーザ」と「ログイン方法」**

画面では、登録してあるユーザが表示されます。存在しないメールアドレスを使用してメール/パスワードを登録することができます。
ログインするための認証ですが、ログインプロバイダにあるものを指定して利用します。

![alt text](image_login_provider.png)

存在しないメールアドレスの場合、メールでパスワードを再設定を行うリンクを送る、ということができまsね。

## ログイン画面

ファイルはこうなっていることを想定しています。

```
├── index.html
├── index.js
├── server.py

### javascript の実装


まずjavascript を呼び出す index.html の実装を用意します。

```HTML: index.httml
<!DOCTYPE html>
<html>
<head>
  <title>Firebase Authentication</title>
  <meta http-equiv="Cross-Origin-Opener-Policy" content="same-origin-allow-top">
  <link rel="icon" href="favicon.ico">
  <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-auth-compat.js"></script>
  <script type="module" src="index.js"></script>
</head>
<body>
  <h1>Firebase Authentication</h1>
  <button id="loginButton">Login with Google</button>
</body>
</html>
```

同じフォルダにこのindex.html が参照するjava script を用意します。

```
// index.js
console.log("import.meta.env", import.meta.env)

const firebaseConfig = {
  apiKey: import.meta.env.VITE_API_KEY,
  authDomain: "myproject.firebaseapp.com",
  projectId: "myproject",
  storageBucket: "myproject.firebasestorage.app",
  messagingSenderId: "999988887777",
  appId: import.meta.env.VITE_APP_ID,
  measurementId: import.meta.env.VITE_MEASUREMENT_ID,
};
firebase.initializeApp(firebaseConfig);
console.log("Firebase initialized in index.js");

const provider = new firebase.auth.GoogleAuthProvider();

// click event listener
function initializeLoginButton() {
  console.log("enter initializeLoginButton");
  const loginButton = document.getElementById("loginButton");
  if (loginButton) {
    loginButton.addEventListener("click", async () => {
      try {
        const result = await firebase.auth().signInWithPopup(provider);
        console.log("call getIdToken()");
        const idToken = await firebase.auth().currentUser.getIdToken();
        console.log("ID Token:", idToken);
        const response = await fetch("http://localhost:8001/verify_token", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ idToken: idToken })
        });
        const data = await response.json();
        console.log("response: ", data);
      } catch (error) {
        console.error(error);
      }
    });
  } else {
    console.error("loginButton not found");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initializeLoginButton();
});
```

このファイルで```firebaseConfig```という変数に設定を書き込んでいますが、書くべき内容は firebase console (WEBページ)から取得できます。ページを下の方にスクロールしていくと、```firebaseConfig```の変数の実装例があるので、それをそのままコピーできます。
ログインボタンを押すとsignInWithPopup(provider)が実行され、新しいwindowが出て、そこに認証が行われます。そこでgmail アドレスの認証がおこなれますが、行われた結果をtoken IDという形で受け取ります。これを

### 実行方法

npm で vite をインストールします。

```
$ npm install vite --save-dev
```

サーバを下記コマンドで立ち上げます。

```
$ npx vite
```


### token IDからユーザ情報を取得する

token IDが有効か確認するためのサーバを立てています。Flaskを利用しています。

```
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from flask import Flask, request, jsonify

from flask_cors import CORS  # Install: pip install Flask-CORS

app = Flask(__name__)
CORS(app)  # Simple usage (allows all origins - USE WITH CAUTION IN PRODUCTION)

cred = credentials.Certificate("/home/....../myproject-firebase-abcdefhi-jklmn-njinjinji.json")
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
```

とりあえず仮想環境を作り、flaskサーバを実行しました。

## 動作確認

npxと　python の両方を同時に実行し、想定通りに動作しました。

# まとめ

Firebase にproject を作り、認証のあるページを作ることができました。
まとまっていませんが、エイやで書いておきます。
(2025/3/10)