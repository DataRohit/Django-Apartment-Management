# Use the official PostgreSQL 16 as the base image
FROM docker.io/postgres:16


# Copy maintenance scripts from host to container
COPY ./compose/local/postgres/maintenance /usr/local/bin/maintenance


# Grant execute permissions to all scripts in the maintenance directory
RUN chmod +x /usr/local/bin/maintenance/*


# Move scripts from maintenance directory to /usr/local/bin and remove the maintenance directory
RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
    && rmdir /usr/local/bin/maintenance
