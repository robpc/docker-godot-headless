#####################################################
# Dockerfile
#
# Creates an image with the Godot headless app.
#
# Build Args:
#   - GODOT_VERSION: The version of Godot
#   - EXPORT_TEMPLATES: Included export templates
#       examples "all", "none", "win"
#

ARG EXPORT_TEMPLATES=all

#------------------------------
# Alias for the root image
FROM debian:stable-slim AS base

ARG GODOT_VERSION=4.0

#------------------------------
# Installs packages to use wget
FROM base as wget

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    wget \
    unzip

#----------------
# Downloads Godot
FROM wget AS godot

RUN wget https://downloads.tuxfamily.org/godotengine/${GODOT_VERSION}/Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip
RUN unzip Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip
RUN mv Godot_v${GODOT_VERSION}-stable_linux.x86_64 /usr/local/bin/godot

#--------------------------------
# Downloads the export templates
FROM wget AS templates

RUN wget https://downloads.tuxfamily.org/godotengine/${GODOT_VERSION}/Godot_v${GODOT_VERSION}-stable_export_templates.tpz
RUN unzip Godot_v${GODOT_VERSION}-stable_export_templates.tpz

#------------------------------
# Clean setup with no templates

FROM base AS export-none

ENV XDG_DATA_HOME /usr/local/share
ENV EXPORT_TEMPLATES_DIR "${XDG_DATA_HOME}/godot/export_templates/${GODOT_VERSION}.stable/"

RUN mkdir -p /root/.cache
RUN mkdir -p /root/.config/godot

COPY --from=godot /usr/local/bin/godot /usr/local/bin/godot

ENTRYPOINT ["godot"]
CMD ["--help"]

#------------------------------
# Only linux template
FROM export-none AS export-linux

COPY --from=templates templates/linux* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only osx template
FROM export-none AS export-macos

COPY --from=templates templates/macos* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only win32 template
FROM export-none AS export-win32

COPY --from=templates templates/windows_*_32* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only win64 template
FROM export-none AS export-win64

COPY --from=templates templates/windows_*_64* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only win template
FROM export-none AS export-windows

COPY --from=templates templates/windows_* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All desktop templates
FROM export-none AS export-desktop

COPY --from=export-linux ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}
COPY --from=export-macos ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}
COPY --from=export-windows ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All android templates
FROM export-none AS export-android

COPY --from=templates templates/android* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All iphone templates
FROM export-none AS export-ios

COPY --from=templates templates/ios* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All mobile templates
FROM export-none AS export-mobile

COPY --from=export-android ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}
COPY --from=export-ios ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only HTML template
FROM export-none AS export-web

COPY --from=templates templates/web* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All templates
FROM export-none AS export-all

COPY --from=templates templates ${EXPORT_TEMPLATES_DIR}

#---------------------------------------
# Selects the export-* based on the arg
FROM export-${EXPORT_TEMPLATES}
