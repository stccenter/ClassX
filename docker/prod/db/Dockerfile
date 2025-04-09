# Use the official MySQL image
FROM mysql:8.0.34

COPY ./mysql-init/init-databases.sql /docker-entrypoint-initdb.d/
# Expose the MySQL port
EXPOSE 3306
