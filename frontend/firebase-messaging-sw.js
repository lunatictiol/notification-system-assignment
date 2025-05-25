// firebase-messaging-sw.js
importScripts("https://www.gstatic.com/firebasejs/11.8.1/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/11.8.1/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "AIzaSyB724A48gqTILyKzBGiKVk2ansDOKUs2Iw",
  authDomain: "notification-system-ffa63.firebaseapp.com",
  projectId: "notification-system-ffa63",
  storageBucket: "notification-system-ffa63.appspot.com",
  messagingSenderId: "981925890805",
  appId: "1:981925890805:web:374c2d9ccedc9ee31e53bc"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);

  const { title, body,data,image_url,action_url} = payload.notification;
  const notificationOptions = {
    body,
    icon: image_url,
    data:data,
    action_url:action_url
  };

  self.registration.showNotification(title, notificationOptions);
});
