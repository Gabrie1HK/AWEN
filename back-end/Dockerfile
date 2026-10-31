# Dockerfile multi-stage para AWEN Backend
# Stage 1: Build
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar dependencias de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

WORKDIR /app

# Crear usuario no-root
RUN groupadd -r awen && useradd -r -g awen awen

# Copiar dependencias instaladas
COPY --from=builder /root/.local /home/awen/.local

# Copiar código de la aplicación
COPY --chown=awen:awen . .

# Cambiar a usuario no-root
USER awen

# Añadir ~/.local/bin al PATH
ENV PATH=/home/awen/.local/bin:$PATH

# Puerto expuesto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]