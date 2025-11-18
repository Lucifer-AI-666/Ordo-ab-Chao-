// Ordo ab Chao - Configurazione Autenticazione PUBBLICA
// Questo file è per il deploy pubblico su GitHub Pages
// Password sono hashate con SHA-256 per sicurezza

const AUTH_CONFIG = {
  users: {
    'demo': {
      password: 'demo123',
      role: 'user',
      name: 'Demo User',
      hashed: false
    },
    'lucifer': {
      password: 'fc533a9a46b64cdacee3007349f08749044f2f603b94311c711077b87085a286',
      role: 'admin',
      name: 'Lucifer-AI-666',
      hashed: true
    }
  },

  session: {
    duration: 24 * 60 * 60 * 1000,  // 24 ore
    rememberDuration: 30 * 24 * 60 * 60 * 1000  // 30 giorni
  }
};
