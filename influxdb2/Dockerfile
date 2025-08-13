ARG BUILD_ARCH=${BUILD_ARCH:-aarch64}
ARG BUILD_FROM=ghcr.io/hassio-addons/debian-base/${BUILD_ARCH}:7.8.3
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup base system
ARG BUILD_ARCH=${BUILD_ARCH:-aarch64}
ARG INFLUXDB=2.7.12

# Copy root filesystem
COPY rootfs /

RUN \
    export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt upgrade -y \
    && case "${BUILD_ARCH}" in \
        aarch64) ARCH="arm64" ;; \
        amd64)  ARCH="amd64" ;; \
        *) echo "Unsupported architecture: ${BUILD_ARCH}"; exit 1 ;; \
    esac \
    && INFLUXDB_FILE="influxdb2_${INFLUXDB}-1_${ARCH}.deb" \
    && INFLUXDB_CLI_FILE="influxdb2-client-${INFLUXDB}-1_${ARCH}.deb" \
    && URL_BASE="https://dl.influxdata.com/influxdb/releases/v${INFLUXDB}" \
    \
    && curl -f -J -L -o /tmp/influxdb2.deb "${URL_BASE}/${INFLUXDB_FILE}" || { echo "InfluxDB package not found: ${URL_BASE}/${INFLUXDB_FILE}"; exit 1; } \
    \
    && dpkg --install /tmp/influxdb2.deb \
    && rm -fr /tmp/* /var/{cache,log}/* /var/lib/apt/lists/* \
    && mkdir -p /data/influxdb2/engine \
    && chmod +x /etc/cont-init.d/influxdb.sh \
    && chmod +x /etc/services.d/influxdb/run \
    && chmod +x /etc/services.d/influxdb/finish

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="ViperRNMC" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="ViperRNMC Add-ons" \
    org.opencontainers.image.authors="ViperRNMC" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/ViperRNMC" \
    org.opencontainers.image.source="https://github.com/${BUILD_REPOSITORY}" \
    org.opencontainers.image.documentation="https://github.com/${BUILD_REPOSITORY}/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}
