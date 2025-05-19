# ──────────────────────────────────────────────────────────────
# Base image with conda (Miniconda3)
# ──────────────────────────────────────────────────────────────
FROM continuumio/miniconda3:24.1.2-0

# ──────────────────────────────────────────────────────────────
# Set working directory inside the container
# ──────────────────────────────────────────────────────────────
WORKDIR /app

# ──────────────────────────────────────────────────────────────
# Install necessary OS packages
# ──────────────────────────────────────────────────────────────
RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    gcc \
    libhdf5-dev \
    pkg-config \
    netcat && \
    rm -rf /var/lib/apt/lists/*

# ──────────────────────────────────────────────────────────────
# Copy application source code
# ──────────────────────────────────────────────────────────────
COPY . .

# ──────────────────────────────────────────────────────────────
# Create conda environment and clean up
# ──────────────────────────────────────────────────────────────
RUN conda env create -f environment.yml && conda clean -a -y

# ──────────────────────────────────────────────────────────────
# Copy and make wait-for-it.sh executable
# ──────────────────────────────────────────────────────────────
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# ──────────────────────────────────────────────────────────────
# Set environment variables
# ──────────────────────────────────────────────────────────────
ENV PYTHONPATH=/app

# ──────────────────────────────────────────────────────────────
# Expose the application port
# ──────────────────────────────────────────────────────────────
EXPOSE 5000

# ──────────────────────────────────────────────────────────────
# Launch the application using gunicorn with service waits
# ──────────────────────────────────────────────────────────────
CMD ["/bin/bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate ClassXTool && gunicorn --workers 10 --threads 12 -b 0.0.0.0:5000 wsgi:app"]

