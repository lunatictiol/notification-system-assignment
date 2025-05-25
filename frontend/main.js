// main.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";
import { getMessaging, getToken, onMessage } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-messaging.js";

const firebaseConfig = {
  apiKey: "AIzaSyB724A48gqTILyKzBGiKVk2ansDOKUs2Iw",
  authDomain: "notification-system-ffa63.firebaseapp.com",
  projectId: "notification-system-ffa63",
  storageBucket: "notification-system-ffa63.appspot.com",
  messagingSenderId: "981925890805",
  appId: "1:981925890805:web:374c2d9ccedc9ee31e53bc"
};

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);
const vapidKey = "BFw3hAzVfTPEFhKRLAKBWtKibvhBhH765FkP4exup209qiQ1FHP5Zyq2-u_qwke5GcxU-JJg8W3tWFmtUIPPYpY";

const subscribeBtn = document.getElementById("subscribe-btn");
const statusMsg = document.getElementById("status-msg");

subscribeBtn.addEventListener("click", () => {
  statusMsg.textContent = "Requesting permission...";
  registerUserFCM();
});

async function registerUserFCM() {
  try {
    const permission = await Notification.requestPermission();
    if (permission === "granted") {
      const currentToken = await getToken(messaging, { vapidKey });
      if (currentToken) {
        console.log("FCM Token:", currentToken);
        statusMsg.textContent = "Subscribed! You can now receive notifications.";

       
        await fetch("http://localhost:8000/devices/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            fcm_token: currentToken
          })
        })
        .then(response => {
          if (!response.ok) {
            throw new Error("Failed to register token");
          }
          return response.json();
        })
        .then(data => {
          console.log("Token registered:", data);
        })
        .catch(err => {
          console.error("Error sending token to backend:", err);
        });

      } else {
        statusMsg.textContent = "No registration token available.";
      }
    } else {
      statusMsg.textContent = "Permission not granted for Notification.";
    }
  } catch (err) {
    console.error("An error occurred while getting the token:", err);
    statusMsg.textContent = "Error occurred. See console.";
  }
}


// Listen to messages when app is in foreground
onMessage(messaging, (payload) => {
  console.log("Message received in foreground:", payload);
  const { title, body } = payload.notification;
  new Notification(title, { body });
});
