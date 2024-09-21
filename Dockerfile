# Base Image
FROM python:3.10-slim

# Set working dir
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3-dev \
    libxss1 \
    libappindicator1 \
    fonts-liberation \
    libu2f-udev \
    libvulkan1 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libatk1.0-0 \
    libcups2 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*


RUN dpkg -L google-chrome-stable

# Copy your ChromeDriver into the container
COPY chromedriver /usr/local/bin/chromedriver

# Make sure ChromeDriver is executable
RUN chmod +x /usr/local/bin/chromedriver

# Copy your scraper script
COPY scraper.py .

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your scraper
ENTRYPOINT ["python", "/app/scraper.py"]
CMD []