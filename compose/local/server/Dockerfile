# Define an alias for the specific python version used in this file.
FROM docker.io/python:3.12.3-slim-bookworm AS python


# Python build stage
FROM python AS python-build-stage


# Define an argument for the build environment (default is local)
ARG BUILD_ENVIRONMENT=local


# Install apt packages required for building Python packages and psycopg dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev


# Copy requirements files to the build stage
COPY ./server/requirements .


# Create Python Dependency and Sub-Dependency Wheels
RUN pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt


# Python 'run' stage
FROM python AS python-run-stage


# Define arguments for the build environment and application home directory
ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app


# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}


# Set working directory
WORKDIR ${APP_HOME}


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


# Install git
RUN apt-get update && apt-get install -y git


# Copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/


# Use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/


# Copy entrypoint script and set permissions
COPY ./compose/local/server/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


# Copy start script and set permissions
COPY ./compose/local/server/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


# Copy Celery worker start script and set permissions
COPY ./compose/local/server/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker


# Copy Celery beat start script and set permissions
COPY ./compose/local/server/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat


# Copy Celery Flower start script and set permissions
COPY ./compose/local/server/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower


# Copy application code to WORKDIR
COPY server ${APP_HOME}


# Define entrypoint
ENTRYPOINT ["/entrypoint"]
