## Dockerfile
## https://docker.github.io/engine/reference/builder/
FROM alpine:3.11

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13
ENV PYTHONUNBUFFERED=1

RUN set -eux; \
    apk add --no-cache python3 \
    && python3 -m pip install --no-cache-dir --upgrade pip

ADD . /tmp/src/
RUN set -eux; \
    cd /tmp/src/ \
    && python3 -m pip install --no-cache-dir -r requirements.txt \
    && rm -rf /tmp/src
ADD entrypoint.sh /usr/bin/

ENTRYPOINT ["/usr/bin/entrypoint.sh"]
