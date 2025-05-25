import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";
import { getMessaging ,getToken} from "https://www.gstatic.com/firebasejs/11.8.1/firebase-messaging.js";

  const firebaseConfig = {

    apiKey: "AIzaSyB724A48gqTILyKzBGiKVk2ansDOKUs2Iw",

    authDomain: "notification-system-ffa63.firebaseapp.com",

    projectId: "notification-system-ffa63",

    storageBucket: "notification-system-ffa63.firebasestorage.app",

    messagingSenderId: "981925890805",

    appId: "1:981925890805:web:374c2d9ccedc9ee31e53bc"

  };
const app = initializeApp(firebaseConfig);
const m = getMessaging(app);
const app_key="BFw3hAzVfTPEFhKRLAKBWtKibvhBhH765FkP4exup209qiQ1FHP5Zyq2-u_qwke5GcxU-JJg8W3tWFmtUIPPYpY"


const subscribeBtn = document.getElementById("subscribe-btn");
const statusMsg = document.getElementById("status-msg");

subscribeBtn.addEventListener("click", () => {
  statusMsg.textContent = "Subscription flow will go here...";
  registerUserFCM()
  
});


function sendTokenToDB(done) {
    getToken({
        vapidKey: app_key
    }).then((currentToken) => {
        if (currentToken) {
            console.log('current token for client: ', currentToken);
            // Track the token -> client mapping, by sending to backend server
            // show on the UI that permission is secured
            // ... add you logic to send token to server
        }
    }).catch((err) => {
        console.log('An error occurred while retrieving token. ', err);
        // catch error while creating client token
    });
}

function onNotification(theNotification) {
    const { title, link_url, ...options } = theNotification;
    notification_options.data.link_url = link_url;

    if ('serviceWorker' in navigator) {
       // this will register the service worker or update it. More on service worker soon
        navigator.serviceWorker.register('./firebase-messaging-sw.js', { scope: './' }).then(function (registration) {
            console.log("Service Worker Registered");
            setTimeout(() => {
                // display the notificaiton
                registration.showNotification(title, { ...notification_options, ...options }).then(done => {
                    console.log("sent notificaiton to user");
                    const audio = new Audio("./util/sound/one_soft_knock.mp3"); // only works on windows chrome
                    audio.play();
                }).catch(err => {
                    console.error("Error sending notificaiton to user", err);
                });
                registration.update();
            }, 100);
        }).catch(function (err) {
            console.log("Service Worker Failed to Register", err);
        });
    }
}

function registerUserFCM() {
    if (!("Notification" in window)) {
        // Check if the browser supports notifications
    } else if (Notification.permission === "granted") {
        // Check whether notification permissions have already been granted;
        // if so, create a token for that user and send to server
        sendTokenToDB(done => {
            console.log("done", done);
            if (done) {
                onNotification({ title: "Successful", body: "Your device has been register", tag: "welcome" });
            }
        });
    } else if (Notification.permission !== "denied") {
        // We need to ask the user for permission
        Notification.requestPermission().then((permission) => {
            // If the user accepts, create a token and send to server
            if (permission === "granted") {
                sendTokenToDB(done => {
                    console.log("done", done);
                    if (done) {
                        onNotification({ title: "Successful", body: "Your device has been register", tag: "welcome" });
                    }
                });
            } else {
                alert("You won't be able to receive important notifications 😥!");
            }
        });
    }
}
