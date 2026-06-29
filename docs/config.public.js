// Ordo ab Chao - Configurazione Autenticazione PUBBLICA
// Password in chiaro per semplicità

const AUTH_CONFIG = {
  users: {
    'demo': {
      password: 'demo123',
      role: 'user',
      name: 'Demo User',
      hashed: false
    },
    'lucifer': {
      password: 'chaos666',
      role: 'admin',
      name: 'Lucifer-AI-666',
      hashed: false
    }
  },

  session: {
    duration: 24 * 60 * 60 * 1000,  // 24 ore
    rememberDuration: 30 * 24 * 60 * 60 * 1000  // 30 giorni
  }
};
