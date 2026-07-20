#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ordo ab Chao - Scatola Nera (Black Box)
Sistema di backup e snapshot automatico
Salva tutti i progressi con timestamp e log dettagliati
"""

import os
import sys
import json
import shutil
import hashlib
from collections import Counter
from datetime import datetime
from pathlib import Path

# Configurazione
PROJECT_ROOT = Path(__file__).parent
BACKUP_DIR = PROJECT_ROOT / "backups"
LOG_FILE = PROJECT_ROOT / "scatola-nera.log"
STATE_FILE = PROJECT_ROOT / "scatola-nera-state.json"

# Escludi questi file/cartelle dal backup
EXCLUDE_PATTERNS = [
    'backups',
    '.git',
    'node_modules',
    '__pycache__',
    '*.pyc',
    '.DS_Store',
    'build',
    'dist',
    '*.apk',
    '*.aab',
    '.gradle'
]

class ScatolaNera:
    def __init__(self):
        self.backup_dir = BACKUP_DIR
        self.log_file = LOG_FILE
        self.state_file = STATE_FILE
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Crea directory backups se non esiste
        self.backup_dir.mkdir(exist_ok=True)

        # Carica stato precedente
        self.state = self.load_state()

    def log(self, message):
        """Scrivi nel log con timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"

        print(log_message.strip())

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message)

    def load_state(self):
        """Carica lo stato precedente"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'snapshots': [],
            'last_backup': None,
            'total_backups': 0
        }

    def save_state(self):
        """Salva lo stato corrente"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, indent=2, fp=f)

    def get_file_hash(self, filepath):
        """Calcola hash MD5 di un file"""
        md5 = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception:
            return None

    def should_exclude(self, path):
        """Verifica se un file/cartella deve essere escluso"""
        path_str = str(path)
        for pattern in EXCLUDE_PATTERNS:
            if pattern.startswith('*'):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        return False

    def scan_project(self):
        """Scansiona il progetto e raccogli info sui file"""
        files_info = {}

        for item in PROJECT_ROOT.rglob('*'):
            if item.is_file() and not self.should_exclude(item):
                rel_path = item.relative_to(PROJECT_ROOT)
                files_info[str(rel_path)] = {
                    'size': item.stat().st_size,
                    'modified': item.stat().st_mtime,
                    'hash': self.get_file_hash(item)
                }

        return files_info

    def create_snapshot(self, description="Snapshot automatico"):
        """Crea uno snapshot completo del progetto"""
        self.log("=" * 60)
        self.log(f"🔒 SCATOLA NERA - Creazione Snapshot")
        self.log(f"📝 Descrizione: {description}")
        self.log("=" * 60)

        # Crea cartella snapshot
        snapshot_name = f"snapshot_{self.timestamp}"
        snapshot_path = self.backup_dir / snapshot_name
        snapshot_path.mkdir(exist_ok=True)

        # Scansiona progetto
        self.log("📊 Scansione progetto in corso...")
        files_info = self.scan_project()
        total_size = sum(f['size'] for f in files_info.values())

        self.log(f"📁 File trovati: {len(files_info)}")
        self.log(f"💾 Dimensione totale: {total_size / 1024 / 1024:.2f} MB")

        # Copia tutti i file
        self.log("💾 Backup file in corso...")
        copied_count = 0

        for rel_path, info in files_info.items():
            src = PROJECT_ROOT / rel_path
            dst = snapshot_path / rel_path

            # Crea directory se necessario
            dst.parent.mkdir(parents=True, exist_ok=True)

            # Copia file
            try:
                shutil.copy2(src, dst)
                copied_count += 1
            except Exception as e:
                self.log(f"⚠️ Errore copia {rel_path}: {e}")

        self.log(f"✅ File copiati: {copied_count}/{len(files_info)}")

        # Salva metadata
        metadata = {
            'timestamp': self.timestamp,
            'datetime': datetime.now().isoformat(),
            'description': description,
            'files_count': len(files_info),
            'total_size': total_size,
            'files': files_info
        }

        metadata_file = snapshot_path / 'metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, indent=2, fp=f)

        # Aggiorna stato
        self.state['snapshots'].append({
            'name': snapshot_name,
            'timestamp': self.timestamp,
            'datetime': metadata['datetime'],
            'description': description,
            'files_count': len(files_info),
            'size': total_size
        })
        self.state['last_backup'] = metadata['datetime']
        self.state['total_backups'] += 1

        self.save_state()

        self.log("=" * 60)
        self.log(f"✅ SNAPSHOT COMPLETATO: {snapshot_name}")
        self.log(f"📍 Percorso: {snapshot_path}")
        self.log("=" * 60)

        return snapshot_path

    def list_snapshots(self):
        """Elenca tutti gli snapshot disponibili"""
        self.log("=" * 60)
        self.log("📦 SNAPSHOT DISPONIBILI")
        self.log("=" * 60)

        if not self.state['snapshots']:
            self.log("⚠️ Nessuno snapshot trovato")
            return

        for i, snapshot in enumerate(self.state['snapshots'], 1):
            self.log(f"\n{i}. {snapshot['name']}")
            self.log(f"   📅 Data: {snapshot['datetime']}")
            self.log(f"   📝 Descrizione: {snapshot['description']}")
            self.log(f"   📁 File: {snapshot['files_count']}")
            self.log(f"   💾 Dimensione: {snapshot['size'] / 1024 / 1024:.2f} MB")

        self.log("\n" + "=" * 60)

    def restore_snapshot(self, snapshot_name):
        """Ripristina un snapshot"""
        snapshot_path = self.backup_dir / snapshot_name

        if not snapshot_path.exists():
            self.log(f"❌ Snapshot non trovato: {snapshot_name}")
            return False

        self.log("=" * 60)
        self.log(f"🔄 RIPRISTINO SNAPSHOT: {snapshot_name}")
        self.log("=" * 60)
        self.log("⚠️ ATTENZIONE: Questo sovrascriverà i file correnti!")

        # Carica metadata
        metadata_file = snapshot_path / 'metadata.json'
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        self.log(f"📅 Data snapshot: {metadata['datetime']}")
        self.log(f"📁 File da ripristinare: {metadata['files_count']}")

        # Conferma (in modalità interattiva)
        if sys.stdin.isatty():
            response = input("\n⚠️ Vuoi procedere? (si/no): ")
            if response.lower() not in ['si', 'yes', 'y', 's']:
                self.log("❌ Ripristino annullato")
                return False

        # Ripristina file
        self.log("🔄 Ripristino in corso...")
        restored_count = 0

        for rel_path in metadata['files'].keys():
            src = snapshot_path / rel_path
            dst = PROJECT_ROOT / rel_path

            if src.exists():
                # Crea directory se necessario
                dst.parent.mkdir(parents=True, exist_ok=True)

                try:
                    shutil.copy2(src, dst)
                    restored_count += 1
                except Exception as e:
                    self.log(f"⚠️ Errore ripristino {rel_path}: {e}")

        self.log(f"✅ File ripristinati: {restored_count}/{metadata['files_count']}")
        self.log("=" * 60)
        self.log("✅ RIPRISTINO COMPLETATO")
        self.log("=" * 60)

        return True

    def analizza(self):
        """Analizza i dati degli snapshot e fornisce insights sul progetto.

        Mostra il trend di file count e dimensione per ogni snapshot,
        calcola la crescita totale tra il primo e l'ultimo snapshot,
        e identifica i file modificati più frequentemente confrontando
        gli hash tra snapshot consecutivi. I risultati vengono scritti nel log.
        """
        self.log("=" * 60)
        self.log("🔍 ANALISI DATI - Ordo ab Chao")
        self.log("=" * 60)

        if not self.state['snapshots']:
            self.log("⚠️ Nessuno snapshot disponibile per l'analisi")
            self.log("💡 Crea prima uno snapshot con: python3 scatola-nera.py snapshot")
            return

        snapshots = self.state['snapshots']
        self.log(f"📦 Snapshot analizzati: {len(snapshots)}")
        self.log(f"📅 Primo snapshot: {snapshots[0]['datetime']}")
        self.log(f"📅 Ultimo snapshot: {snapshots[-1]['datetime']}")

        # Trend dimensione e file count
        self.log("\n📊 TREND NEL TEMPO:")
        self.log(f"  {'Snapshot':<30} {'File':<8} {'Dimensione (MB)':<18}")
        self.log("  " + "-" * 56)
        for snap in snapshots:
            size_mb = snap['size'] / 1024 / 1024
            self.log(f"  {snap['name']:<30} {snap['files_count']:<8} {size_mb:<18.2f}")

        # Crescita totale
        if len(snapshots) > 1:
            first = snapshots[0]
            last = snapshots[-1]
            file_delta = last['files_count'] - first['files_count']
            size_delta_mb = (last['size'] - first['size']) / 1024 / 1024
            self.log(f"\n📈 CRESCITA TOTALE:")
            self.log(f"  File: {'+' if file_delta >= 0 else ''}{file_delta}")
            self.log(f"  Dimensione: {'+' if size_delta_mb >= 0 else ''}{size_delta_mb:.2f} MB")

        # Analisi file più modificati (confronto snapshot consecutivi)
        changed_counter = Counter()
        for i in range(1, len(snapshots)):
            prev_snap = snapshots[i - 1]
            curr_snap = snapshots[i]
            prev_path = self.backup_dir / prev_snap['name'] / 'metadata.json'
            curr_path = self.backup_dir / curr_snap['name'] / 'metadata.json'

            if not prev_path.exists() or not curr_path.exists():
                continue

            with open(prev_path, 'r', encoding='utf-8') as f:
                prev_meta = json.load(f)
            with open(curr_path, 'r', encoding='utf-8') as f:
                curr_meta = json.load(f)

            for file_path, info in curr_meta.get('files', {}).items():
                prev_info = prev_meta.get('files', {}).get(file_path)
                if prev_info is None or info.get('hash') != prev_info.get('hash'):
                    changed_counter[file_path] += 1

        if changed_counter:
            top_changed = changed_counter.most_common(10)
            self.log(f"\n🔄 FILE PIÙ MODIFICATI (top {len(top_changed)}):")
            for file_path, count in top_changed:
                self.log(f"  {count:>4}x  {file_path}")

        self.log("\n" + "=" * 60)
        self.log("✅ ANALISI COMPLETATA")
        self.log("=" * 60)

    def create_incremental_backup(self):
        """Crea backup incrementale (solo file modificati)"""
        self.log("🔄 Backup incrementale in corso...")

        if not self.state['snapshots']:
            self.log("⚠️ Nessuno snapshot precedente, creo snapshot completo")
            return self.create_snapshot("Primo snapshot")

        # Carica ultimo snapshot
        last_snapshot = self.state['snapshots'][-1]
        last_snapshot_path = self.backup_dir / last_snapshot['name']
        last_metadata_file = last_snapshot_path / 'metadata.json'

        with open(last_metadata_file, 'r', encoding='utf-8') as f:
            last_metadata = json.load(f)

        # Scansiona progetto corrente
        current_files = self.scan_project()

        # Trova file nuovi/modificati
        changed_files = {}
        for path, info in current_files.items():
            if path not in last_metadata['files']:
                changed_files[path] = 'new'
            elif info['hash'] != last_metadata['files'][path]['hash']:
                changed_files[path] = 'modified'

        # Trova file eliminati
        deleted_files = []
        for path in last_metadata['files']:
            if path not in current_files:
                deleted_files.append(path)

        if not changed_files and not deleted_files:
            self.log("✅ Nessuna modifica rilevata")
            return None

        self.log(f"📝 File nuovi: {len([f for f in changed_files.values() if f == 'new'])}")
        self.log(f"📝 File modificati: {len([f for f in changed_files.values() if f == 'modified'])}")
        self.log(f"📝 File eliminati: {len(deleted_files)}")

        # Crea snapshot con descrizione dettagliata
        description = f"Backup incrementale: {len(changed_files)} modifiche, {len(deleted_files)} eliminazioni"
        return self.create_snapshot(description)

def main():
    """Funzione principale"""
    scatola = ScatolaNera()

    if len(sys.argv) < 2:
        print("\n🔒 SCATOLA NERA - Sistema di Backup Ordo ab Chao\n")
        print("Uso:")
        print("  python3 scatola-nera.py snapshot [descrizione]  - Crea snapshot completo")
        print("  python3 scatola-nera.py backup                  - Crea backup incrementale")
        print("  python3 scatola-nera.py list                    - Elenca snapshot")
        print("  python3 scatola-nera.py restore <nome>          - Ripristina snapshot")
        print("  python3 scatola-nera.py analizza                - Analizza dati e fornisce insights")
        print("\nEsempi:")
        print("  python3 scatola-nera.py snapshot \"PWA completata\"")
        print("  python3 scatola-nera.py backup")
        print("  python3 scatola-nera.py restore snapshot_20250117_143022")
        print("  python3 scatola-nera.py analizza\n")
        sys.exit(0)

    command = sys.argv[1].lower()

    if command == 'snapshot':
        description = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else "Snapshot manuale"
        scatola.create_snapshot(description)

    elif command == 'backup':
        scatola.create_incremental_backup()

    elif command == 'list':
        scatola.list_snapshots()

    elif command == 'restore':
        if len(sys.argv) < 3:
            print("❌ Specifica il nome dello snapshot da ripristinare")
            sys.exit(1)
        snapshot_name = sys.argv[2]
        scatola.restore_snapshot(snapshot_name)

    elif command == 'analizza':
        scatola.analizza()

    else:
        print(f"❌ Comando sconosciuto: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
