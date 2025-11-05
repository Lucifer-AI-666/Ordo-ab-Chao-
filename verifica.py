#!/usr/bin/env python3
"""
Verifica che l'inizializzazione sia stata completata correttamente
Usage: python3 verifica.py
"""

import os
import sys
from pathlib import Path

def check_directory_structure():
    """Verifica la struttura delle directory"""
    required_dirs = [
        "01-tauros", "02-lucy", "scripts", "docs", 
        "legal", "gateway", "tests", "logs"
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not Path(directory).is_dir():
            missing_dirs.append(directory)
    
    return missing_dirs

def check_required_files():
    """Verifica i file essenziali"""
    required_files = [
        "allowlist.example.json",
        "README.md",
        "01-tauros/README.md",
        "02-lucy/README.md", 
        "02-lucy/requirements.txt",
        "gateway/README.md",
        "gateway/requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).is_file():
            missing_files.append(file_path)
    
    return missing_files

def check_modelfiles():
    """Verifica i Modelfiles"""
    # Optimized: single list comprehension with multiple paths
    modelfiles = [
        str(modelfile) 
        for directory in ["01-tauros", "02-lucy"]
        for modelfile in Path(directory).glob("*.Modelfile")
    ]
    return modelfiles

def main():
    print("🔍 Verifica inizializzazione priv-cyber-agents...")
    print("")
    
    # Check directory structure
    missing_dirs = check_directory_structure()
    if missing_dirs:
        print("❌ Directory mancanti:")
        for directory in missing_dirs:
            print(f"   - {directory}")
        print("")
    else:
        print("✅ Struttura directory: OK")
    
    # Check required files
    missing_files = check_required_files()
    if missing_files:
        print("❌ File mancanti:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("")
    else:
        print("✅ File essenziali: OK")
    
    # Check Modelfiles
    modelfiles = check_modelfiles()
    if modelfiles:
        print("✅ Modelfiles trovati:")
        for modelfile in modelfiles:
            print(f"   - {modelfile}")
    else:
        print("⚠️  Nessun Modelfile trovato (eseguire inizializzazione?)")
    
    print("")
    
    # Overall status
    if not missing_dirs and not missing_files:
        print("🎉 Inizializzazione completata con successo!")
        print("")
        print("📋 Prossimi passi consigliati:")
        print("   1. Copia allowlist.example.json in allowlist.json e personalizza")
        print("   2. Setup Ollama: cd 01-tauros && ollama create tauros_private -f *.Modelfile")
        print("   3. Setup Python env: cd 02-lucy && python3 -m venv .venv")
        print("")
        return 0
    else:
        print("⚠️  Inizializzazione incompleta. Eseguire:")
        print("   ./inizia.sh  oppure  python3 inizia.py")
        print("")
        return 1

if __name__ == "__main__":
    sys.exit(main())