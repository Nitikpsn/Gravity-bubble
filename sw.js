// Cache the heavy PyScript/Pyodide/Pygame files so reloads start fast.
// Local game files stay network-first so edits always show up immediately.
const CACHE_NAME = "gravity-bubble-v1";

const CDN_HOSTS = [
    "pyscript.net",
    "cdn.jsdelivr.net",
    "packages.pyscript.net",
    "pyodide.org",
    "files.pythonhosted.org",
    "pypi.org",
];

self.addEventListener("install", function () {
    self.skipWaiting();
});

self.addEventListener("activate", function (event) {
    event.waitUntil(
        (async function () {
            const keys = await caches.keys();
            await Promise.all(
                keys
                    .filter(function (key) {
                        return key.startsWith("gravity-bubble-") && key !== CACHE_NAME;
                    })
                    .map(function (key) {
                        return caches.delete(key);
                    })
            );
            await self.clients.claim();
        })()
    );
});

function isCdnRequest(url) {
    return CDN_HOSTS.some(function (host) {
        return url.hostname === host || url.hostname.endsWith("." + host);
    });
}

async function cacheFirst(request) {
    const cache = await caches.open(CACHE_NAME);
    const cached = await cache.match(request);
    if (cached) {
        return cached;
    }

    const response = await fetch(request);
    if (response.ok && response.status !== 206) {
        await cache.put(request, response.clone());
    }
    return response;
}

async function networkFirst(request) {
    const cache = await caches.open(CACHE_NAME);
    try {
        const response = await fetch(request);
        if (response.ok && response.status !== 206) {
            await cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cached = await cache.match(request);
        if (cached) {
            return cached;
        }
        throw error;
    }
}

self.addEventListener("fetch", function (event) {
    const request = event.request;
    if (request.method !== "GET" || request.headers.has("range")) {
        return;
    }

    const url = new URL(request.url);
    if (url.protocol !== "http:" && url.protocol !== "https:") {
        return;
    }

    if (isCdnRequest(url)) {
        event.respondWith(cacheFirst(request));
    } else if (url.origin === self.location.origin) {
        event.respondWith(networkFirst(request));
    }
});
