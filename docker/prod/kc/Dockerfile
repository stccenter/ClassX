# Official Keycloak Image
FROM quay.io/keycloak/keycloak:24.0.2

# Labels
LABEL maintainer="Gian Sung <jsung24@gmu.edu>"

# Enable health and metrics
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

#COPY ./docker/prod/nginx/certs/__stcenter_net_cert.cer /opt/keycloak/conf/server.crt
#COPY ./docker/prod/nginx/certs/__stcenter_net_interm.cer /opt/keycloak/conf/truststores/trustedcert.crt
#COPY ./docker/prod/nginx/certs/star_stcenter_net.key /opt/keycloak/conf/server.key

# Bypass for debugging
# ENTRYPOINT ["/bin/sh", "-c", "sleep infinity"]
