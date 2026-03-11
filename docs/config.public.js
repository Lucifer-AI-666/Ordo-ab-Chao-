// Ordo ab Chao - Configurazione Autenticazione PUBBLICA
// Solo credenziali demo - NON usare password reali in questo file!

const AUTH_CONFIG = {
  users: {
    'demo': {
      password: 'demo123',
      role: 'user',
      name: 'Demo User',
      hashed: false
    }
  },

  session: {
    duration: 24 * 60 * 60 * 1000,  // 24 ore
    rememberDuration: 30 * 24 * 60 * 60 * 1000  // 30 giorni
  }
};
