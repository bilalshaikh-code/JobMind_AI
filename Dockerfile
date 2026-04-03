# Use the standard Python image (not slim) to ensure all build tools are present
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install only the absolute essentials (if needed)
# Most are already in the non-slim python:3.12 image
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app code
COPY . .

# Streamlit port
EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]