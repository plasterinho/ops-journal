# stage 1 - build the static site
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdocs build

# Stage 2 - server static files with NGINX
FROM nginx:alpine

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy the generated static site
COPY --from=builder /app/site /usr/share/nginx/html

# NGINX already listens on 80

