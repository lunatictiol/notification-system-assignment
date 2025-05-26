# 🔔 Web Notification System

A simple web notification system built with **FastAPI**, **RabbitMQ**, **Firebase Cloud Messaging (FCM)**, and **Docker**. This system allows you to trigger push notifications to multiple devices through a background worker.

## 📦 Tech Stack

- **FastAPI** – REST API for sending messages
- **RabbitMQ** – Message broker to decouple notification sending
- **PostgreSQL** – Stores FCM device tokens
- **Worker (Python)** – Background worker to listen for queue messages and send notifications
- **FCM** – Firebase Cloud Messaging for push notifications
- **Docker Compose** – Service orchestration

---

## 🧠 Architecture

```

\[ FastAPI Producer ]
|
V
\[ RabbitMQ Queue ] ---> \[ Worker ]
|
V
\[ Firebase Notification ]

````

- The FastAPI server receives a request and sends a message to RabbitMQ.
- A worker service consumes messages and sends push notifications to the device tokens stored in PostgreSQL.

---

## How to run

### Prerequisites

* [Docker](https://www.docker.com/)
* A [Firebase project](https://console.firebase.google.com/)

  * Enable **Cloud Messaging**
  * Generate **Web Push Certificate Key Pair** (VAPID key)
  * Create a **Service Account Key** and download the JSON credentials file (`firebase-adminsdk-xxx.json`)

---

### 1. Clone the Repository

```bash
git clone https://github.com/lunatictiol/notification-system-assignment.git
cd notification-system-assignment
```

---

### 2. Add Firebase Credentials

Place your `firebase-adminsdk.json` file inside the `./worker/` directory and rename it to `serverkey.json`.

Update the `worker/consumer.py` :

```python
cred = credentials.Certificate("serverkey.json")
```

---

### 3. Configure Firebase in Frontend

In `frontend/main.js`, add your Firebase project configuration:

```js
// Replace with your actual Firebase config
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID"
};

firebase.initializeApp(firebaseConfig);

// Register service worker
navigator.serviceWorker.register('firebase-messaging-sw.js')
  .then((registration) => {
    const messaging = firebase.messaging();
    messaging.useServiceWorker(registration);
    messaging.getToken({ vapidKey: 'YOUR_WEB_PUSH_CERTIFICATE_KEY_PAIR' })
      .then((currentToken) => {
        // Send this token to your backend
      });
  });
```

In `frontend/firebase-messaging-sw.js`, make sure the file includes:

```js
// Required imports
importScripts('https://www.gstatic.com/firebasejs/10.1.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.1.0/firebase-messaging-compat.js');

// Replace with your actual Firebase config
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

// Handle background messages
messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/icon.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
```

---

### 4. Start the Project

```bash
docker-compose up --build
```

This launches:

* FastAPI backend on [http://localhost:8000](http://localhost:8000)
* Frontend on [http://localhost:80](http://localhost:80)
* RabbitMQ server on port `5672`

---

### 5. Register a Device Token

**Endpoint:** `POST /devices/register`
**URL:** `http://localhost:8000/devices/register`
**Request Body:**

```json
{
  "fcm_token": "your_fcm_token_here"
}
```

---

### 6. Send a Notification

**Endpoint:** `POST /notifications/publish`
**URL:** `http://localhost:8000/notifications/publish`
**Request Body:**

```json
{
  "title": "New Message!",
  "body": "This is a push notification test",
  "data": {
    "url": "https://yourapp.com"
  },
  "image_url": "https://example.com/image.png",
  "action_url": "https://yourapp.com/open"
}
```

---


## 📁 Project Structure

```
notification-system/
│
├── backend/                            # FastAPI backend service
│   ├── app/                            # Application source code
│   │   ├── main.py                     # Entry point to start FastAPI server and include routes
│   │   ├── models.py                   # Database or internal models
│   │   ├── schemas.py                  # Pydantic models for request/response validation
│   │   ├── db.py                       # databse setup and initialization
│   │   ├── dependencies.py             # shared dependencies
│   │   ├── storage.py                  # Token storage mechanism 
│   │   ├── routes/                     # API route handlers
│   │   │   ├── register.py             # Route to register/save FCM token
│   │   │   └── notification.py         # Route to publish/send notifications (push to RabbitMQ)
│   │   └── requirements.txt            # Python dependencies for the backend
│   └── Dockerfile                      # Docker image setup for the backend
│
├── worker/                             # Background worker to consume messages and send push notifications
│   ├── consumer.py                     # RabbitMQ consumer that reads messages and calls FCM API
│   ├── db.py                           # database initialization for the worker
│   ├── serverkey.json                  # Firebase service account credentials
│   └── Dockerfile                      # Docker image setup for the worker
│
├── frontend/                           # Minimal frontend to test push notifications
│   ├── index.html                      # Simple HTML UI for the web client
│   ├── main.js                         # Handles token registration and communication with backend
│   └── firebase-messaging-sw.js        # Firebase service worker for handling background messages
│
├── docker-compose.yml                  # Docker Compose to orchestrate backend, frontend, and RabbitMQ
└── README.md                           # Project documentation and setup instructions


```

---

## 🛠️ Useful Commands

* Rebuild: `docker-compose up --build`
* Stop: `docker-compose down`
* View RabbitMQ UI: [http://localhost:15672](http://localhost:15672) (user: `guest`, pass: `guest`)




