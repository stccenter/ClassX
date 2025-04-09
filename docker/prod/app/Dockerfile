# Use the official Miniconda3 image as a base image
FROM continuumio/miniconda3:24.1.2-0

# Labels
LABEL maintainer="Gian Sung <jsung24@gmu.edu>"

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx gcc libhdf5-dev pkg-config

# Creating directories for setup
RUN mkdir environment \
    && mkdir classxlib \
    && mkdir flaskr \
    && mkdir templates

# Copy dependency necessary files and set environment
COPY ./environment/stable_env.yml /app
COPY ./classxlib /app/classxlib
COPY ./flaskr /app/flaskr
COPY ./templates /app/templates

# COPY ./setup.py /app

RUN echo "Installing app requirements (setup.py):"
RUN conda env create -f stable_env.yml

# Copy certificates to container private directory
COPY ./docker/prod/nginx/certs/__stcenter_net_cert.cer /etc/ssl/private
COPY ./docker/prod/nginx/certs/__stcenter_net_interm.cer /etc/ssl/private
COPY ./ /app

# Concatenate certificates to the existing CA bundle
RUN cat /etc/ssl/private/__stcenter_net_cert.cer >> /etc/ssl/certs/ca-certificates.crt
RUN cat /etc/ssl/private/__stcenter_net_interm.cer >> /etc/ssl/certs/ca-certificates.crt

# Set the environment variables for Python requests to use the updated CA bundle
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Dev
# ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ClassXTool"]
# CMD ["python", "app.py"]

# Prod
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ClassXTool"]
CMD ["gunicorn", "--workers","5","--threads","6","-b", "0.0.0.0:5000", "wsgi:create_app()"]

# Bypass for debugging
# ENTRYPOINT ["/bin/bash", "-c", "sleep infinity"]
