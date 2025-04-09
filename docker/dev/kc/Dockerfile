# Official Keycloak Image
FROM quay.io/keycloak/keycloak:24.0.2

# Labels
LABEL maintainer="Gian Sung <jsung24@gmu.edu>"

# Enable health and metrics
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# Bypass for debugging
# ENTRYPOINT ["/bin/sh", "-c", "sleep infinity"]