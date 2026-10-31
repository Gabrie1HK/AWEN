#!/usr/bin/env python
# scripts/migrate_to_supabase.py
# Migra la base de datos local a Supabase (versión Python para Windows)
# Uso: python scripts/migrate_to_supabase.py

import os
import subprocess
import sys
from urllib.parse import urlparse

def run_cmd(cmd, env=None):
    """Ejecuta comando y retorna (success, output)"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def main():
    print("🚀 Migrando base de datos local a Supabase...")
    
    # Leer URL de Supabase desde variable de entorno
    supabase_url = os.environ.get("SUPABASE_DB_URL") or os.environ.get("POSTGRES_URL")
    
    if not supabase_url:
        print("❌ Error: Variable de entorno SUPABASE_DB_URL o POSTGRES_URL no configurada")
        print("   Configura la URL de conexión de Supabase:")
        print("   $env:SUPABASE_DB_URL='postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres'")
        print("   (En PowerShell) o export SUPABASE_DB_URL=... (en bash)")
        sys.exit(1)
    
    # URL local por defecto
    local_url = os.environ.get("LOCAL_DB_URL", "postgresql://awen:awen@localhost:5432/awen")
    
    print(f"📦 Haciendo backup de la BD local ({local_url})...")
    dump_file = "awen_local_dump.sql"
    
    # pg_dump
    success, output = run_cmd(f'pg_dump "{local_url}" --no-owner --no-privileges --clean --if-exists > {dump_file}')
    if not success:
        print(f"❌ Error en pg_dump: {output}")
        sys.exit(1)
    
    print(f"📦 Backup guardado en {dump_file}")
    
    print(f"🔄 Restaurando en Supabase...")
    # psql restore
    success, output = run_cmd(f'psql "{supabase_url}" < {dump_file}')
    if not success:
        print(f"❌ Error restaurando en Supabase: {output}")
        sys.exit(1)
    
    print("✅ Migración completada")
    
    # Verificar tablas
    print("🔍 Verificando tablas en Supabase...")
    success, output = run_cmd(f'psql "{supabase_url}" -c "\\dt"')
    if success:
        print(output)
    
    # Limpiar
    if os.path.exists(dump_file):
        os.remove(dump_file)
    
    print("✅ Migración completada exitosamente")
    print("   Verifica en Supabase Dashboard → Table Editor")

if __name__ == "__main__":
    main()