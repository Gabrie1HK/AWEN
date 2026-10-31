#!/usr/bin/env bash
# scripts/migrate_to_supabase.sh
# Migra la base de datos local a Supabase
# Uso: ./scripts/migrate_to_supabase.sh

set -e

echo "🚀 Migrando base de datos local a Supabase..."

# Verificar variables requeridas
if [ -z "$SUPABASE_DB_URL" ]; then
    echo "❌ Error: SUPABASE_DB_URL no está configurada"
    echo "   Exporta la URL de conexión de Supabase:"
    echo "   export SUPABASE_DB_URL='postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres'"
    exit 1
fi

# Configuración local
LOCAL_DB_URL="postgresql://awen:awen@localhost:5432/awen"

echo "📦 Haciendo backup de la BD local..."
pg_dump "$LOCAL_DB_URL" --no-owner --no-privileges --clean --if-exists > /tmp/awen_local_dump.sql

echo "🔄 Restaurando en Supabase..."
# Usar psql con la URL de Supabase
psql "$SUPABASE_DB_URL" < /tmp/awen_local_dump.sql

echo "✅ Migración completada"
echo "🔍 Verificando tablas..."
psql "$SUPABASE_DB_URL" -c "\dt"

echo ""
echo "✅ Migración completada exitosamente"
echo "   Verifica en Supabase Dashboard → Table Editor"