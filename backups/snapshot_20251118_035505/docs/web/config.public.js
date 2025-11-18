// Ordo ab Chao - Configurazione Autenticazione PUBBLICA
// Questo file è per il deploy pubblico su Vercel
// Contiene SOLO credenziali DEMO (non quelle vere)

const AUTH_CONFIG = {
  users: {
    'demo': {
      password: 'demo123',
      role: 'user',
      name: 'Demo User'
    },
    'guest': {
      password: 'guest123',
      role: 'user',
      name: 'Guest User'
    }
  },

  session: {
    duration: 24 * 60 * 60 * 1000,  // 24 ore
    rememberDuration: 30 * 24 * 60 * 60 * 1000  // 30 giorni
  }
};
