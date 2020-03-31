FROM python:3.8-alpine3.10
LABEL maintainer=Zhennan.luo python-version=3.8
ENV PATH="/root/.local/bin:$PATH"
COPY docker-entrypoint.sh /usr/bin/docker-entrypoint.sh
RUN chmod +x /usr/bin/docker-entrypoint.sh \
    && apk add --update --no-cache bash jq groff \
    && pip install --user awscli \
    && pip install boto3

# ENTRYPOINT [ "/root/.local/bin/aws" ]
ENTRYPOINT [ "docker-entrypoint.sh" ]