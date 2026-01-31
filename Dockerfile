FROM nginx:alpine

# Remove default nginx content
RUN rm -rf /usr/share/nginx/html/*

# Copy the generated static site
COPY site/ /usr/share/nginx/html/

# NGINX already listens on 80

