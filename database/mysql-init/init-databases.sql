-- Create keycloak DB on startup
CREATE DATABASE IF NOT EXISTS keycloak_db;
CREATE DATABASE IF NOT EXISTS label_db;
CREATE USER IF NOT EXISTS 'keycloakuser'@'%' IDENTIFIED BY 'secretpass';
GRANT ALL PRIVILEGES ON keycloak_db.* TO 'keycloakuser'@'%';
FLUSH PRIVILEGES;
