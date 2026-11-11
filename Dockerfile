# CBOM Testbench: the pinned environment every published score is produced in.
#
#   docker build -t cbom-benchmark:2.3.0 .
#   docker run --rm --network none cbom-benchmark:2.3.0 checks            # required checks
#   docker run --rm --network none -v "$PWD/out:/out" my-scanner-image \
#       run --name "Scanner X" --scanner-cmd "scanx {corpus} -o {out}/cbom.json" --bundle /out/bundle
#
# To score a scanner, build FROM this image and install the scanner on top (see the README), so the
# scanner, the corpus and the scorer share one digest-pinned environment. Run it with
#   --network none --cap-add SYS_ADMIN --security-opt apparmor=unconfined
# The capability lets tools/sandbox.py make the mount namespace it needs for the filesystem
# boundary (the scanner must not be able to read /testbench/expected). Without it the sandbox still
# scrubs the environment and hashes the corpus, records "filesystem: not confined", and
# --require-isolation refuses to run. For a scanner you don't trust at all, don't share an image
# with it: see the two-job workflow in integrations/qci-pqc/github-workflow.yml.
#
# Tested without the official base images (the build environment couldn't pull them): this file
# builds and passes its strict corpus check against stand-in bases with the same layout, and the
# release workflow's container steps pass against that image. What a tagged build on GitHub adds is
# the real bases, the apt step and the digest.
#
# Base images are pinned by tag here. The release workflow resolves and records their digests and
# the digest of the built image; pin by digest (image@sha256:...) once a release is cut.

# 3.13: corpus/tier5/python/compiled/ledger_sync.pyc is Python 3.13 bytecode, and the strict corpus check
# below runs it. (The harness itself supports 3.11+; CI tests that floor separately.)
ARG PYTHON_IMAGE=python:3.13-slim-bookworm
ARG GO_IMAGE=golang:1.24-bookworm
ARG NODE_IMAGE=node:22.18-bookworm-slim
ARG JDK_IMAGE=eclipse-temurin:21-jdk

FROM ${GO_IMAGE} AS go
FROM ${NODE_IMAGE} AS node
FROM ${JDK_IMAGE} AS jdk

FROM ${PYTHON_IMAGE}
ARG PYTHON_IMAGE GO_IMAGE NODE_IMAGE JDK_IMAGE

# C toolchain and OpenSSL 3 headers for the C cases.
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential libssl-dev ca-certificates util-linux \
 && rm -rf /var/lib/apt/lists/*

COPY --from=go /usr/local/go /usr/local/go
COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=jdk /opt/java/openjdk /opt/java/openjdk
ENV PATH=/usr/local/go/bin:/opt/java/openjdk/bin:$PATH \
    JAVA_HOME=/opt/java/openjdk \
    GOTOOLCHAIN=local GOTELEMETRY=off \
    PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /testbench
COPY requirements.txt requirements-verify.txt ./
RUN pip install -r requirements-verify.txt

COPY . .
# Toolchain versions, recorded once at build time and copied into every evidence bundle.
RUN { echo "{"; \
      echo "  \"python\": \"$(python --version 2>&1)\","; \
      echo "  \"go\": \"$(go version)\","; \
      echo "  \"node\": \"$(node --version)\","; \
      echo "  \"javac\": \"$(javac -version 2>&1)\","; \
      echo "  \"cc\": \"$(cc --version | head -1)\","; \
      echo "  \"openssl\": \"$(dpkg-query -W -f='${Version}' libssl-dev 2>/dev/null || openssl version)\","; \
      echo "  \"base_images\": \"${PYTHON_IMAGE} ${GO_IMAGE} ${NODE_IMAGE} ${JDK_IMAGE}\""; \
      echo "}"; } > /testbench/TOOLCHAINS.json \
 && python tools/verify_corpus.py --strict > /dev/null

ENTRYPOINT ["python", "tools/bench.py"]
CMD ["--help"]
