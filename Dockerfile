# syntax=docker/dockerfile:1

# Uses Python 3.10 slim for smaller image
FROM python:3.10-slim
ENV DEBIAN_FRONTEND=noninteractive
ENV NPM_BIN_PATH=/usr/bin/npm

# buildargs

# Set working directory to /app
WORKDIR /app

# Install packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -fsSL https://deb.nodesource.com/setup_current.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    gcc \
    python3-dev \
    libpq-dev

# Install Python dependencies
COPY requirements/* requirements/
RUN pip3 install --no-cache-dir -r requirements/prod.txt

# Copy everything to workpath
COPY . .

# Install node dependencies, build Tailwind and remove node packages + src
WORKDIR /app/theme/static_src
RUN npm install \
    && python3 /app/manage.py tailwind build \
    && rm -r /app/theme/static_src

# Uninstall unneeded packages
RUN apt-get purge --autoremove -y \
    nodejs \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# End job
WORKDIR /app
