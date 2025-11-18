# 🔒 CONFIGURAZIONE SICUREZZA

## ⚠️ IMPORTANTE: Configurazione Credenziali

Le credenziali di login **NON** sono incluse nel repository per motivi di sicurezza.

### Setup Iniziale

1. **Copia il file di esempio:**
   ```bash
   cp web/config.js.example web/config.js
   ```

2. **Modifica `web/config.js` con le TUE credenziali:**
   ```javascript
   const AUTH_CONFIG = {
     users: {
       'tuo_username': {
         password: 'tua_password_sicura',
         role: 'admin',
         name: 'Tuo Nome'
       }
     }
   };
   ```

3. **NON committare `config.js` su GitHub!**
   - Il file è già in `.gitignore`
   - Mantieni le credenziali SOLO in locale

### Credenziali Demo

Per **SOLO scopo di testing pubblico**, esiste un utente demo:
- Username: `demo`
- Password: `demo123`
- Ruolo: `user` (limitato)

**⚠️ NON usare in produzione!**

### Best Practices

1. ✅ Usa password forti (min 12 caratteri)
2. ✅ Cambia password regolarmente
3. ✅ Non condividere credenziali
4. ✅ Usa hash SHA-256 in produzione
5. ✅ Implementa rate limiting
6. ✅ Abilita 2FA se possibile

### Migrazione a Database

Per produzione, sostituisci il file `config.js` con:
- Database locale crittografato (SQLite + SQLCipher)
- Hash bcrypt per password
- Salt unico per utente
- Logging accessi
- Rate limiting

### Problemi?

Se `config.js` non esiste, il sistema userà l'utente demo con accesso limitato.

---

**🔐 La sicurezza è importante. Proteggi le tue credenziali!**
