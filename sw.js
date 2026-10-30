// VYRON AI Explainer — Secure Production Service Worker
const CACHE_NAME = 'vyron-cache-v2';
const STATIC_ASSETS = [
    './',
    './index.html',
    './css/style.css',
    './js/app.js',
    './manifest.json',
    './logo.jpg'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(STATIC_ASSETS).catch(() => {
                // Non-fatal if specific assets fail to cache immediately
            });
        }).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((key) => {
                    if (key !== CACHE_NAME) {
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    const req = event.request;
    const url = new URL(req.url);

    // 1. NEVER intercept non-GET requests (e.g. POST to /api/process-document)
    if (req.method !== 'GET') {
        return;
    }

    // 2. NEVER intercept API routes or cross-origin AI inference calls
    if (url.pathname.startsWith('/api/') || url.hostname.includes('groq.com') || url.hostname.includes('googleapis.com')) {
        return;
    }

    // 3. Stale-while-revalidate for local static assets
    event.respondWith(
        caches.match(req).then((cachedResponse) => {
            const fetchPromise = fetch(req).then((networkResponse) => {
                if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
                    const responseToCache = networkResponse.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(req, responseToCache);
                    });
                }
                return networkResponse;
            }).catch(() => cachedResponse);

            return cachedResponse || fetchPromise;
        })
    );
});
