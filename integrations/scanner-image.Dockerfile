# A scanner-only image for `bench.py run --scanner-image`: the scanner and nothing else.
#
#   pip wheel --wheel-dir wheels "path/to/scanner[x509]"          # in a job with no secrets
#   docker build -f integrations/scanner-image.Dockerfile -t my-scanner:1.0 --build-arg WHEELS=wheels \
#       --build-arg PACKAGE="qci-pqc-scan[x509]" .
#   python tools/bench.py run --scanner-image my-scanner:1.0 \
#       --scanner-cmd "qci-pqc scan {corpus} --reproducible --out {out} --json" ...
#
# bench.py starts it with no network, a read-only root, no capabilities, the corpus mounted read-only
# at /in/corpus and the output directory at /out. No testbench file exists inside it.
ARG BASE=python:3.13-slim-bookworm
FROM ${BASE}
ARG WHEELS=wheels
ARG PACKAGE
COPY ${WHEELS} /wheels
RUN python3 -m venv /opt/scanner \
 && /opt/scanner/bin/pip install --no-index --find-links /wheels --only-binary :all: "${PACKAGE}" \
 && rm -rf /wheels
ENV PATH=/opt/scanner/bin:/usr/local/bin:/usr/bin:/bin
