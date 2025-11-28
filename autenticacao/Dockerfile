FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Instalar dependências do sistema necessárias para MySQL client e build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

## Copiar todo o código do serviço de autenticação para /app
# (copiar contexto inteiro primeiro evita problemas com arquivos ausentes
# quando a ferramenta de build calcula checksums)
COPY . .

COPY ca.pem /app/ca.pem


# Instalar dependências a partir do requirements.txt presente no contexto
# Use `python -m pip` para garantir que o pip usado corresponde ao interpretador
RUN if [ -f requirements.txt ]; then \
            python -m pip install --no-cache-dir -U pip setuptools wheel && \
            python -m pip install --no-cache-dir -r requirements.txt ; \
        fi

# Ensure uvicorn is installed in the runtime interpreter (explicitly). This
# avoids "No module named uvicorn" when the console script is not available
# or when some requirements failed to install optional extras.
RUN python -m pip install --no-cache-dir "uvicorn[standard]"

WORKDIR /app

EXPOSE 8001

# Comando padrão: executa o app em autenticacao/main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
