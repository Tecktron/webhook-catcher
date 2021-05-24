FROM tecktron/python-bjoern:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get clean && apt-get update && \
    apt-get -y install --no-install-recommends \
    apt-utils \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

ENV MODULE_NAME=webhook_catcher.wsgi

COPY . /app
RUN chmod +x /app/prestart.sh
WORKDIR /app/

RUN python -m pip install pip --no-cache-dir --upgrade
RUN pip install -r /app/requirements.txt
