FROM python:3.14-alpine3.23
LABEL maintainer=lzn python-version=3.14
ARG TARGETOS
ARG TARGETARCH
ENV PATH="/root/.local/bin:$PATH"
COPY docker-entrypoint.sh /usr/bin/docker-entrypoint.sh
RUN chmod +x /usr/bin/docker-entrypoint.sh \
    && apk add --update --no-cache go bash jq groff zip kubectl helm curl \
    && pip install --upgrade pip && pip install --user awscli \
    && pip install boto3
RUN curl -L "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_Linux_${TARGETARCH}.tar.gz" -o /tmp/eksctl.tar.gz \
    && tar -C /tmp -xzf /tmp/eksctl.tar.gz && install -m 0755 /tmp/eksctl /usr/local/bin/eksctl
    
ENTRYPOINT [ "docker-entrypoint.sh" ]
