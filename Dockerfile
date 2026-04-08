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

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy custom NGINX configuration
COPY platform/nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy the generated static site
COPY --from=builder /app/site /usr/share/nginx/html

# Inject version information into the environment
RUN echo "{\"git_sha\": \"${GIT_SHA}\"}" > /usr/share/nginx/html/monitor_version.json

# NGINX already listens on 80