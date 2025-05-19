# ./docker/auth/Dockerfile

FROM quay.io/keycloak/keycloak:20.0.1

USER root
RUN mkdir -p /opt/keycloak/data/import && \
    chown -R 1000:1000 /opt/keycloak/data/import

COPY auth.json /opt/keycloak/data/import/auth.json

USER 1000

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]

