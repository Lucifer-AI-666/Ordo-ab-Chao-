// Ordo ab Chao - Service Worker
// Privacy-first PWA con cache offline

const STATIC_CACHE_NAME = 'ordo-ab-chao-static-v1.1.0';
const RUNTIME_CACHE_NAME = 'ordo-ab-chao-runtime-v1.1.0';
const APP_SHELL = [
  'index.html',
  'login.html',
  'register.html',
  'reset-password.html',
  'projects.html',
  'admin.html',
  'quick-login.html',
  'manifest.json',
  'config.public.js',
  'icon-72.png',
  'icon-96.png',
  'icon-128.png',
  'icon-144.png',
  'icon-152.png',
  'icon-192.png',
  'icon-384.png',
  'icon-512.png',
  'icon-tauros.png',
  'icon-lucy.png',
  'icon-dashboard.png'
];

function resolveAppUrl(path = '') {
  return new URL(path, self.registration.scope).toString();
}

function shouldCacheResponse(response) {
  // Cache only successful same-origin responses; skip opaque/error responses.
  return response && response.ok && (response.type === 'basic' || response.type === 'default');
}

function getOfflineFallback() {
  return caches.match(resolveAppUrl('index.html'));
}

// Install Event - Cache risorse statiche
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching assets');
        return cache.addAll(APP_SHELL.map((asset) => resolveAppUrl(asset)));
      })
      .then(() => {
        console.log('[Service Worker] Installation complete');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[Service Worker] Installation failed:', error);
      })
  );
});

// Activate Event - Pulizia vecchie cache
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating...');
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cache) => {
            if (![STATIC_CACHE_NAME, RUNTIME_CACHE_NAME].includes(cache)) {
              console.log('[Service Worker] Deleting old cache:', cache);
              return caches.delete(cache);
            }
          })
        );
      })
      .then(() => {
        console.log('[Service Worker] Activation complete');
        return self.clients.claim();
      })
  );
});

// Fetch Event - Strategia Cache-First per risorse statiche, Network-First per API
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') {
    return;
  }

  const url = new URL(event.request.url);

  if (url.origin !== self.location.origin) {
    return;
  }

  // API requests - Network First
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (shouldCacheResponse(response)) {
            const responseClone = response.clone();
            caches.open(RUNTIME_CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          return caches.match(event.request);
        })
    );
    return;
  }

  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (shouldCacheResponse(response)) {
            const responseClone = response.clone();
            caches.open(RUNTIME_CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          return caches.match(event.request, { ignoreSearch: true })
            .then((cachedPage) => cachedPage || getOfflineFallback());
        })
    );
    return;
  }

  // Static assets - Stale While Revalidate
  event.respondWith(
    caches.match(event.request, { ignoreSearch: true })
      .then((cachedResponse) => {
        const fetchPromise = fetch(event.request)
          .then((response) => {
            if (shouldCacheResponse(response)) {
              const responseClone = response.clone();
              caches.open(RUNTIME_CACHE_NAME).then((cache) => {
                cache.put(event.request, responseClone);
              });
            }
            return response;
          })
          .catch(() => null);

        if (cachedResponse) {
          event.waitUntil(fetchPromise);
          return cachedResponse;
        }

        return fetchPromise.then((response) => response || getOfflineFallback());
      })
      .catch(() => getOfflineFallback())
  );
});

// Background Sync - Per operazioni offline
self.addEventListener('sync', (event) => {
  console.log('[Service Worker] Syncing:', event.tag);

  if (event.tag === 'sync-data') {
    event.waitUntil(
      // Implementa logica di sincronizzazione
      syncOfflineData()
    );
  }
});

// Push Notifications (opzionale per future funzionalità)
self.addEventListener('push', (event) => {
  console.log('[Service Worker] Push received');

  const options = {
    body: event.data ? event.data.text() : 'Notifica da Ordo ab Chao',
    icon: resolveAppUrl('icon-192.png'),
    badge: resolveAppUrl('icon-72.png'),
    vibrate: [200, 100, 200],
    tag: 'ordo-notification',
    requireInteraction: false
  };

  event.waitUntil(
    self.registration.showNotification('Ordo ab Chao', options)
  );
});

// Notification Click
self.addEventListener('notificationclick', (event) => {
  console.log('[Service Worker] Notification clicked');
  event.notification.close();

  event.waitUntil(
    clients.openWindow(resolveAppUrl('index.html'))
  );
});

// Funzioni Helper
async function syncOfflineData() {
  try {
    console.log('[Service Worker] Syncing offline data...');
    // Implementa logica di sincronizzazione dati offline
    return Promise.resolve();
  } catch (error) {
    console.error('[Service Worker] Sync failed:', error);
    return Promise.reject(error);
  }
}

// Message Handler - Comunicazione con client
self.addEventListener('message', (event) => {
  console.log('[Service Worker] Message received:', event.data);

  if (event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(RUNTIME_CACHE_NAME).then((cache) => {
        return cache.addAll(event.data.urls.map((url) => resolveAppUrl(url)));
      })
    );
  }

  if (event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cache) => caches.delete(cache))
        );
      })
    );
  }
});
