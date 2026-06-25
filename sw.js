/**
 * WooaGosa Service Worker – 오프라인 캐싱
 */
const CACHE_NAME = 'wooagosa-v2';
const PRECACHE = [
  '/',
  '/index.html',
  '/exam.html',
  '/result.html',
  '/wrong-notes.html',
  '/404.html',
  '/css/style.css',
  '/js/db.js',
  '/js/exam.js',
  '/manifest.json',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(PRECACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  // JSON 데이터는 항상 네트워크 우선 (최신 문제 유지)
  if (e.request.url.includes('/data/')) {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE_NAME).then(c => c.put(e.request, clone));
          return res;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }
  // 나머지는 캐시 우선
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request))
  );
});
