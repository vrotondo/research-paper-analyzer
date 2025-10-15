# Use Alpine (much smaller - ~50MB vs ~150MB)
FROM python:3.12-alpine

WORKDIR /app

# Install only essential dependencies
RUN apk add --no-cache gcc musl-dev linux-headers curl

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create directories
RUN mkdir -p data/raw data/processed

EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]