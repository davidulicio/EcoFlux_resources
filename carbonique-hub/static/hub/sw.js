/* Only cache the neutral application shell and local assets. Never cache API replies. */
const CACHE = "carbonique-shell-v2";
const ASSETS = ["/static/hub/app.js", "/static/hub/storage.js", "/static/hub/style.css", "/static/hub/logo.svg", "/static/hub/icon.svg", "/manifest.webmanifest"];
self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith("carbonique-shell-") && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("message", event => {
  if (event.data === "CACHE_SHELL") event.waitUntil(caches.open(CACHE).then(async cache => {
    const response = await fetch("/", {credentials: "same-origin"});
    if (!response.ok || new URL(response.url).pathname !== "/") throw new Error("Sign in again before preparing the app for offline use.");
    await cache.put("/", response);
    event.ports[0]?.postMessage({ok:true});
  }).catch(error => event.ports[0]?.postMessage({ok:false,error:error.message})));
  if (event.data === "CLEAR_SHELL") event.waitUntil(caches.open(CACHE).then(cache => cache.delete("/")));
});
self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin) return;
  if (url.pathname === "/" && event.request.mode === "navigate") {
    event.respondWith(fetch(event.request).then(async response => {
      if (response.ok && new URL(response.url).pathname === "/") (await caches.open(CACHE)).put("/", response.clone());
      return response;
    }).catch(async () => (await caches.match("/")) || new Response("Open Carbonique online and prepare your sites before going offline.", {status: 503, headers: {"Content-Type": "text/plain"}})));
  } else if (ASSETS.includes(url.pathname)) {
    event.respondWith(fetch(event.request).then(async response => {
      if (response.ok) await (await caches.open(CACHE)).put(event.request, response.clone());
      return response;
    }).catch(() => caches.match(event.request)));
  }
});
