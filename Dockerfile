# Use the base image of your choice (e.g., Ubuntu or Debian)
FROM ubuntu:20.04

# Disable interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages, including Python and pip
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
    chromium-driver \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /app/requirements.txt

# Create the scraped_data directory in the container
RUN mkdir -p /app/scraped_data

# Copy your script into the container
COPY scraper.py /app/scraper.py

# Set working directory
WORKDIR /app

# Default command to run your script
CMD ["python3", "scraper.py"]
