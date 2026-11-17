const cacheName = "gravity-bubble-v1";

self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    caches.match(event.request).then((saved) => {
      if (saved) return saved;

      return fetch(event.request).then((res) => {
        const copy = res.clone();
        caches.open(cacheName)
          .then((cache) => cache.put(event.request, copy))
          .catch(() => {});
        return res;
      });
    })
  );
});
