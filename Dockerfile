FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y --no-install-recommends build-essential \
	&& rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /tmp/backend-requirements.txt
COPY autenticacao/requirements.txt /tmp/auth-requirements.txt

RUN pip install --no-cache-dir -U pip setuptools wheel \
	&& pip install --no-cache-dir pylint \
	&& pip install --no-cache-dir python-jose[cryptography] fastapi-mail \
	&& if [ -f /tmp/backend-requirements.txt ]; then pip install --no-cache-dir -r /tmp/backend-requirements.txt; fi \
	&& if [ -f /tmp/auth-requirements.txt ]; then pip install --no-cache-dir -r /tmp/auth-requirements.txt; fi

CMD ["pylint", "--disable=C0114,C0115,C0116", "--score=y", "."]
