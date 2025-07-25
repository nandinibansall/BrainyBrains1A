# # Use official Python image for amd64
# FROM --platform=linux/amd64 python:3.10-slim

# # Install PyMuPDF library
# RUN pip install --no-cache-dir pymupdf pdfplumber

# # Set working folder
# WORKDIR /app

# # Copy Python script into image
# COPY extract_outline.py /app/

# # Entry command when container runs
# ENTRYPOINT ["python", "extract_outline.py"]


FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY extract_outline.py .

ENTRYPOINT ["python", "extract_outline.py"]