// index.js
console.log("import.meta.env", import.meta.env)

const firebaseConfig = {
  apiKey: import.meta.env.VITE_API_KEY,
  authDomain: "my-cloud-run01.firebaseapp.com",
  projectId: "my-cloud-run01",
  storageBucket: "my-cloud-run01.firebasestorage.app",
  messagingSenderId: "809639188470",
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