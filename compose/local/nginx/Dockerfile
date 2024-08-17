# Use the official Nginx Alpine image as the base image
FROM docker.io/nginx:1.27.0-alpine


# Copy the custom Nginx configuration file from the host into the container
COPY ./compose/local/nginx/default.conf /etc/nginx/conf.d/default.conf
