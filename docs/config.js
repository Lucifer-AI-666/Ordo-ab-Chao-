// Ordo ab Chao - Configurazione Autenticazione
// PRIVATO - NON committare su GitHub!

const AUTH_CONFIG = {
  users: {
    'admin': {
      password: 'ordo2025',
      role: 'admin',
      name: 'Amministratore'
    },
    'lucifer': {
      password: 'chaos666',
      role: 'admin',
      name: 'Lucifer-AI-666'
    },
    'user': {
      password: 'user123',
      role: 'user',
      name: 'Utente Standard'
    }
  },

  session: {
    duration: 24 * 60 * 60 * 1000,  // 24 ore
    rememberDuration: 30 * 24 * 60 * 60 * 1000  // 30 giorni
  }
};
