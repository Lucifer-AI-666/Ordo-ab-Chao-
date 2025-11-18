// Ordo ab Chao - Configurazione Autenticazione
// PRIVATO - NON committare su GitHub!
// Password generate: 2025-11-18 02:14:09

const AUTH_CONFIG = {
  users: {
    'admin': {
      password: 'SSVm_#$_ltDk$V2VbKs*',
      role: 'admin',
      name: 'Amministratore'
    },
    'lucifer': {
      password: 'Dbinra88e14z330a',
      role: 'admin',
      name: 'Lucifer-AI-666'
    },
    'user': {
      password: 'aSOe*s#xsaLzlMA-',
      role: 'user',
      name: 'Utente Standard'
    }
  },

  session: {
    duration: 24 * 60 * 60 * 1000,  // 24 ore
    rememberDuration: 30 * 24 * 60 * 60 * 1000  // 30 giorni
  }
};
