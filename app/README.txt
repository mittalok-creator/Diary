ALOK OS — PWA Package (BY ALOK MITTAL)
=======================================

FILES
  index.html            the complete app
  sw.js                 service worker (offline + notifications)
  manifest.webmanifest  install metadata
  icon-192.png / icon-512.png

DEPLOY (2 minutes — PWA needs HTTPS hosting)
  Option A — Netlify Drop (easiest):
    1. Go to  https://app.netlify.com/drop
    2. Drag this whole folder (or the zip, extracted) onto the page
    3. You get a URL like  https://alokos.netlify.app  — that's your app

  Option B — GitHub Pages:
    1. Create a repo, upload these files to its root
    2. Settings → Pages → Deploy from branch (main / root)
    3. Open the published URL

INSTALL
  Android (Chrome):  open URL → menu ⋮ → "Install app"  → opens full-screen like a native app
  iPhone (Safari):   open URL → Share → "Add to Home Screen"
  Laptop/Desktop (Chrome/Edge):  install icon in the address bar → works on Windows/Mac like an app
  Tablet: same as phone — layout adapts automatically

NOTIFICATIONS
  1. In the app: Settings → Notifications → Enable → Allow
  2. Alerts (meeting reminders, task due) now come as SYSTEM notifications —
     they appear even when the app is in the background or the screen is off,
     as long as the app/tab is running (installed PWAs keep running on Android).
  3. iPhone: requires iOS 16.4+ and Home-Screen install for notifications.

  Honest note: alerts when the app is FULLY closed need a push server.
  That is the next upgrade (Supabase + Web Push) whenever you want it.

DATA
  Everything stays on your device (localStorage). Use Settings → Backup
  regularly; the backup file includes all attachments and restores anywhere.
