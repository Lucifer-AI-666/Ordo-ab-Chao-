// Ordo ab Chao - Service Worker
// Privacy-first PWA con cache offline

const CACHE_NAME = 'ordo-ab-chao-v1.0.0';
const CACHE_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icon-72.png',
  '/icon-96.png',
  '/icon-128.png',
  '/icon-144.png',
  '/icon-152.png',
  '/icon-192.png',
  '/icon-384.png',
  '/icon-512.png',
  '/icon-tauros.png',
  '/icon-lucy.png',
  '/icon-dashboard.png'
];

// Install Event - Cache risorse statiche
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching assets');
        return cache.addAll(CACHE_ASSETS);
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
            if (cache !== CACHE_NAME) {
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
  const url = new URL(event.request.url);

  // API requests - Network First
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // Clone per salvare in cache
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
          return response;
        })
        .catch(() => {
          // Fallback su cache se offline
          return caches.match(event.request);
        })
    );
    return;
  }

  // Dynamic routes - Network First con fallback
  if (url.pathname.match(/^\/(tauros|lucy|copilot|dashboard|share)/)) {
    event.respondWith(
      fetch(event.request)
        .catch(() => {
          // Fallback su index.html per SPA routing
          return caches.match('/index.html');
        })
    );
    return;
  }

  // Static assets - Cache First
  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        if (cachedResponse) {
          // Ritorna dalla cache e aggiorna in background
          fetch(event.request)
            .then((response) => {
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(event.request, response);
              });
            })
            .catch(() => {
              // Network non disponibile, ignora
            });
          return cachedResponse;
        }

        // Non in cache, fetch dalla rete
        return fetch(event.request)
          .then((response) => {
            // Salva in cache per future richieste
            if (response.status === 200) {
              const responseClone = response.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(event.request, responseClone);
              });
            }
            return response;
          });
      })
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
    icon: '/icon-192.png',
    badge: '/icon-72.png',
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
    clients.openWindow('/')
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
      caches.open(CACHE_NAME).then((cache) => {
        return cache.addAll(event.data.urls);
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
