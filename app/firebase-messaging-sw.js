/* ALOK OS — Firebase Cloud Messaging service worker (handles closed-app push) */
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js');

firebase.initializeApp({
  apiKey: "AIzaSyDLZY5yMJT4YXj8rqiKI0U9GpYpM1kHS9w",
  authDomain: "alok-os-19787.firebaseapp.com",
  projectId: "alok-os-19787",
  storageBucket: "alok-os-19787.firebasestorage.app",
  messagingSenderId: "774257734126",
  appId: "1:774257734126:web:5846d255032f8540229eff"
});

const messaging = firebase.messaging();

/* Background message → show a system notification */
messaging.onBackgroundMessage(function (payload) {
  const n = (payload && payload.notification) || {};
  const d = (payload && payload.data) || {};
  const title = n.title || d.title || 'ALOK OS';
  const body = n.body || d.body || 'You have a reminder';
  self.registration.showNotification(title, {
    body: body,
    icon: './icon-192.png',
    badge: './icon-192.png',
    tag: d.tag || ('alokos-' + Date.now()),
    data: { url: './' },
    vibrate: [80, 40, 80]
  });
});

/* Tap the notification → focus or open the app */
self.addEventListener('notificationclick', function (e) {
  e.notification.close();
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(function (list) {
      for (const c of list) { if ('focus' in c) return c.focus(); }
      if (clients.openWindow) return clients.openWindow('./');
    })
  );
});
