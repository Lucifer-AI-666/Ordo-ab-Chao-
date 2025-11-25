#!/usr/bin/env python3
"""
Backup Account - DibTauroS/Ordo-ab-Chao
Crea un backup completo della configurazione account
Owner: Dib Anouar
License: LUP v1.0 (uso personale e non commerciale)

Usage: python3 backup_account.py
"""

import os
import sys
import json
import shutil
import tarfile
from datetime import datetime, timezone
from pathlib import Path

def print_emoji(emoji, message):
    """Print message with emoji (fallback for systems without emoji support)"""
    try:
        print(f"{emoji} {message}")
    except UnicodeEncodeError:
        print(f"[{emoji}] {message}")

def create_backup():
    """Create comprehensive account backup"""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"backups/account_backup_{timestamp}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print_emoji("💾", f"Creazione backup account: {backup_dir}")
    print()
    
    # Files and directories to backup
    backup_items = {
        "Configuration Files": [
            "copilot-agent/config/.env.copilot",
            "copilot-agent/config/account.json",
            "copilot-agent/config/allowlist.json",
            "copilot-agent/config/modes.json",
            "allowlist.json",
            "allowlist.example.json"
        ],
        "Agent Configurations": [
            "01-tauros/TaurosPrivateAgent.Modelfile",
            "01-tauros/CopilotPrivateAgent.Modelfile",
            "01-tauros/README.md",
            "02-lucy/LucyPrivateAgent.Modelfile",
            "02-lucy/README.md",
            "02-lucy/requirements.txt"
        ],
        "Documentation": [
            "docs/account/README_ACCOUNT.md",
            "README.md",
            "README_PRIVATO_Version4.md"
        ],
        "Scripts": [
            "ricostituzione_account.py",
            "verifica_account.py",
            "backup_account.py",
            "inizia.py",
            "verifica.py"
        ]
    }
    
    backup_manifest = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "owner": "Dib Anouar",
        "framework": "DibTauroS/Ordo-ab-Chao",
        "version": "1.0.0",
        "files": {}
    }
    
    total_files = 0
    total_size = 0
    
    for category, files in backup_items.items():
        print_emoji("📂", category)
        category_dir = backup_dir / category.lower().replace(" ", "_")
        category_dir.mkdir(exist_ok=True)
        
        for file_path in files:
            src = Path(file_path)
            if src.exists():
                # Create destination path preserving directory structure
                rel_path = src.parent
                dest_dir = category_dir / rel_path
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / src.name
                
                # Copy file
                shutil.copy2(src, dest)
                
                # Get file info
                file_size = src.stat().st_size
                total_files += 1
                total_size += file_size
                
                # Add to manifest
                backup_manifest["files"][str(file_path)] = {
                    "size": file_size,
                    "backed_up": datetime.now(timezone.utc).isoformat(),
                    "category": category
                }
                
                print(f"   ✅ {file_path} ({file_size} bytes)")
            else:
                print(f"   ⚠️  {file_path} (non trovato)")
    
    print()
    
    # Create backup manifest
    manifest_file = backup_dir / "backup_manifest.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(backup_manifest, f, indent=2)
    
    print_emoji("📝", f"Manifest creato: {manifest_file}")
    
    # Create README for backup
    readme_content = f"""# Account Backup - DibTauroS/Ordo-ab-Chao

## Informazioni Backup

- **Owner**: Dib Anouar
- **Framework**: DibTauroS/Ordo-ab-Chao
- **Timestamp**: {timestamp}
- **Data/Ora**: {datetime.now(timezone.utc).isoformat()}

## Contenuto Backup

- **File totali**: {total_files}
- **Dimensione totale**: {total_size:,} bytes ({total_size / 1024:.2f} KB)

## Categorie Backup

{chr(10).join(f"- **{cat}**: {len([f for f, info in backup_manifest['files'].items() if info['category'] == cat])} file" for cat in backup_items.keys())}

## Ripristino

Per ripristinare questo backup:

1. Eseguire il backup in una posizione sicura
2. Per ripristinare singoli file, copiarli manualmente
3. Per ripristino completo, eseguire:
   ```bash
   python3 ricostituzione_account.py
   ```
   Poi sostituire i file con quelli del backup

## Sicurezza

⚠️ **IMPORTANTE**: Questo backup contiene token di sicurezza sensibili!

- Conservare in una posizione sicura
- Cifrare se memorizzato su storage esterno
- Non condividere con terze parti
- Eliminare backup obsoleti in modo sicuro

## Verifica Integrità

Vedere `backup_manifest.json` per l'elenco completo dei file e le dimensioni.
"""
    
    readme_file = backup_dir / "README.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print_emoji("📖", f"README creato: {readme_file}")
    print()
    
    # Create compressed archive
    archive_name = f"backups/account_backup_{timestamp}.tar.gz"
    print_emoji("📦", f"Creazione archivio compresso: {archive_name}")
    
    with tarfile.open(archive_name, "w:gz") as tar:
        tar.add(backup_dir, arcname=f"account_backup_{timestamp}")
    
    archive_size = Path(archive_name).stat().st_size
    print(f"   ✅ Archivio creato ({archive_size:,} bytes, {archive_size / 1024:.2f} KB)")
    print()
    
    return backup_dir, archive_name, total_files, total_size, archive_size

def main():
    """Main backup process"""
    print()
    print("=" * 70)
    print_emoji("💾", "BACKUP ACCOUNT - DibTauroS/Ordo-ab-Chao")
    print("=" * 70)
    print()
    print("   Owner: Dib Anouar")
    print("   Framework: DibTauroS/Ordo-ab-Chao")
    print("   License: LUP v1.0 (uso personale e non commerciale)")
    print()
    
    try:
        backup_dir, archive_name, total_files, total_size, archive_size = create_backup()
        
        print("=" * 70)
        print_emoji("✅", "BACKUP COMPLETATO CON SUCCESSO!")
        print("=" * 70)
        print()
        
        print_emoji("📊", "Riepilogo:")
        print(f"   ✅ File backuppati: {total_files}")
        print(f"   ✅ Dimensione totale: {total_size:,} bytes ({total_size / 1024:.2f} KB)")
        print(f"   ✅ Directory backup: {backup_dir}")
        print(f"   ✅ Archivio: {archive_name}")
        print(f"   ✅ Dimensione archivio: {archive_size:,} bytes ({archive_size / 1024:.2f} KB)")
        print()
        
        print_emoji("🔒", "Sicurezza:")
        print("   ⚠️  Il backup contiene token di sicurezza sensibili!")
        print("   🔐 Conservare in una posizione sicura")
        print("   🗑️  Eliminare backup obsoleti in modo sicuro")
        print()
        
        print_emoji("📖", "Prossimi passi:")
        print(f"   1. Verifica integrità: tar -tzf {archive_name}")
        print(f"   2. Sposta in posizione sicura: mv {archive_name} /percorso/sicuro/")
        print(f"   3. (Opzionale) Cifra: gpg -c {archive_name}")
        print()
        
        return 0
        
    except KeyboardInterrupt:
        print()
        print_emoji("❌", "Backup interrotto dall'utente")
        return 1
    except Exception as e:
        print()
        print_emoji("❌", f"Errore durante il backup: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
