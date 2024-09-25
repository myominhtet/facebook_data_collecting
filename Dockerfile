# Base image: Python with necessary dependencies
FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libxi6 \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    libxdamage1 \
    libxtst6 \
    fonts-liberation \
    libappindicator1 \
    xdg-utils \
    chromium-driver

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Create the scraped_data directory in the container
RUN mkdir -p /app/scraped_data

# Copy your script into the container
COPY scraper.py /app/scraper.py

# Set working directory
WORKDIR /app

# Default command to run your script
CMD ["python", "scraper.py"]
