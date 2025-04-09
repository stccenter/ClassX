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
COPY ./environment/environment.yml /app
COPY ./classxlib /app/classxlib
COPY ./flaskr /app/flaskr
COPY ./templates /app/templates

# COPY ./setup.py /app

RUN echo "Installing app requirements (setup.py):"
RUN conda env create -f environment.yml

# Copy the local code into the container at /app
COPY ./ /app

# Make port 5000 available to the world outside this container
EXPOSE 5001

# Run app.py when the container launches
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "ClassXTool"]
#CMD ["python", "-u","app.py"]

# Prod
#CMD ["gunicorn", "wsgi:app", "-b", "appx:5000"]

# Bypass for debugging
#ENTRYPOINT ["/bin/bash", "-c", "sleep infinity"]