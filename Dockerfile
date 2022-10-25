# syntax=docker/dockerfile:1

FROM python:3.10
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install node & npm
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash - && apt-get install -y nodejs

# Install additional packages
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev

# Remove apt cache
RUN rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements/* requirements/
RUN pip3 install --no-cache-dir -r requirements/prod.txt

# Copy everything to workpath
COPY . .

# Install node dependencies
WORKDIR /app/theme/static_src
RUN npm install

# Build Tailwind for production
WORKDIR /app
RUN python3 manage.py tailwind build
