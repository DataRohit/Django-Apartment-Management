# Use the official Node.js 20.11 image based on Alpine 3.18 as the base image
FROM docker.io/node:20.11-alpine3.18 as base


# Create a new stage for building the Node.js application
FROM base as node-build-stage


# Install libc6-compat package to provide compatibility with glibc-based libraries
RUN apk add --no-cache libc6-compat


# Copy lock files to ensure consistent dependency installation
COPY ./client/package.json ./client/yarn.lock* ./client/package-lock.json* ./client/pnpm-lock.yaml* ./


# Install dependencies based on the available lock file
RUN \
	if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
	elif [ -f package-lock.json ]; then npm ci; \
	elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i; \
	else echo "Lockfile not found." && exit 1; \
	fi


# Create a new stage for running the Node.js application
FROM base as node-run-stage


# Set the application home directory
ARG APP_HOME=/app
WORKDIR ${APP_HOME}


# Copy the installed dependencies from the build stage
COPY --from=node-build-stage /node_modules ./node_modules


# Copy the application code into the container
COPY ./client ${APP_HOME}


# Start the application using npm
CMD [ "npm","run","dev" ]
