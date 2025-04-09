# Use official Node.js image as base image
FROM node:22.4 AS build 

# Setting working directory
WORKDIR /react

# Copying package.json and package-lock.json
COPY ./frontend/package*.json ./ 

# Clean cache prior to installation
#RUN npm cache clean --force

# Installing dependencies
RUN npm install

# Copy the rest of app
COPY ./frontend/ ./
COPY ./frontend/.env /react/.env
#COPY ./frontend/src /src
#COPY ./frontend/public /public

# Build app using Vite
RUN npm run build

# Use NGINX to serve
FROM nginx:alpine

# Copy the built React app to Nginx's web server directory
COPY --from=build /react/dist /usr/share/nginx/html

# Copy NGINX config
# COPY deploy/nginx.default.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for the Nginx server
EXPOSE 80
EXPOSE 443

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]
