# Use official Node.js image as base image
FROM node:22.4 AS build 

# Setting working directory
WORKDIR /react

# Copying package.json and package-lock.json
COPY ./frontend/package*.json /react

# Installing dependencies
RUN npm install

# Copy rest of app
COPY ./frontend/index.html /react
COPY ./frontend/vite.config.js /react
COPY ./frontend/public /react/public
COPY ./frontend/src /react/src
COPY ./frontend/.env /react/.env

# Build app
RUN npm run build

# Use NGINX to serve react
FROM nginx:alpine

# Copy built react app to NGINX's web server directory
COPY --from=build /react/dist /usr/share/nginx/html

# Expost port 80 for NGINX (shouldn't matter??)
EXPOSE 80
