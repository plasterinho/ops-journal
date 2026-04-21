# stage 1 - build the static site
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdocs build

# Stage 2 - server static files with NGINX
FROM nginx:alpine

# Build arguments for versioning
ARG GIT_SHA=dev

# Install the Python runtime used by the in-container metrics exporter.
RUN apk add --no-cache python3 py3-pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --break-system-packages --no-cache-dir -r /app/requirements.txt \
    && pip install --break-system-packages --no-cache-dir prometheus_client

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy custom NGINX configuration
COPY platform/nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy the generated static site
COPY --from=builder /app/site /usr/share/nginx/html
COPY metrics /app/metrics
COPY reality /app/reality
COPY docs/journal/week-06.checks.yaml /app/docs/journal/week-06.checks.yaml
COPY start-services.sh /app/start-services.sh

# Inject version information into the environment
RUN echo "{\"git_sha\": \"${GIT_SHA}\"}" > /usr/share/nginx/html/monitor_version.json

RUN chmod +x /app/start-services.sh

ENV OPS_JOURNAL_CHECKS_FILE=/app/docs/journal/week-06.checks.yaml

# NGINX already listens on 80
CMD ["/app/start-services.sh"]
