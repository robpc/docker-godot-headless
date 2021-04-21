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

ARG GODOT_VERSION=3.3

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

RUN wget https://downloads.tuxfamily.org/godotengine/${GODOT_VERSION}/Godot_v${GODOT_VERSION}-stable_linux_headless.64.zip
RUN unzip Godot_v${GODOT_VERSION}-stable_linux_headless.64.zip
RUN mv Godot_v${GODOT_VERSION}-stable_linux_headless.64 /usr/local/bin/godot

#--------------------------------
# Downloads the export templates
FROM wget AS templates

RUN wget https://downloads.tuxfamily.org/godotengine/${GODOT_VERSION}/Godot_v${GODOT_VERSION}-stable_export_templates.tpz
RUN unzip Godot_v${GODOT_VERSION}-stable_export_templates.tpz

#------------------------------
# Clean setup with no templates

FROM base AS export-none

ENV XDG_DATA_HOME /usr/local/share
ENV EXPORT_TEMPLATES_DIR "${XDG_DATA_HOME}/godot/templates/${GODOT_VERSION}.stable/"

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
FROM export-none AS export-osx

COPY --from=templates templates/osx* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only win32 template
FROM export-none AS export-win32

COPY --from=templates templates/windows_32* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only win64 template
FROM export-none AS export-win64

COPY --from=templates templates/windows_64* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only win template
FROM export-none AS export-win

COPY --from=templates templates/windows_* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only uwp32 template
FROM export-none AS export-uwp32

COPY --from=templates templates/uwp_x86* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only uwp64 template
FROM export-none AS export-uwp64

COPY --from=templates templates/uwp_x64* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All uwp templates
FROM export-none AS export-uwp

COPY --from=templates templates/uwp_* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All windows templates
FROM export-none AS export-windows

COPY --from=export-uwp ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}
COPY --from=export-win ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All desktop templates
FROM export-none AS export-desktop

COPY --from=export-linux ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}
COPY --from=export-osx ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}
COPY --from=export-windows ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All android templates
FROM export-none AS export-android

COPY --from=templates templates/android* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All iphone templates
FROM export-none AS export-iphone

COPY --from=templates templates/iphone* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All mobile templates
FROM export-none AS export-mobile

COPY --from=export-android ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}
COPY --from=export-iphone ${EXPORT_TEMPLATES_DIR} ${EXPORT_TEMPLATES_DIR}

#------------------------------
# Only HTML template
FROM export-none AS export-html

COPY --from=templates templates/webassembly* ${EXPORT_TEMPLATES_DIR}

#------------------------------
# All templates
FROM export-none AS export-all

COPY --from=templates templates ${EXPORT_TEMPLATES_DIR}

#---------------------------------------
# Selects the export-* based on the arg
FROM export-${EXPORT_TEMPLATES}
