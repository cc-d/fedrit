# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04 as build

# python/npm versions to use latest versions of
ARG PV="3.10"
ARG NV="16.14"

# Set environment variable for the app directory
ENV APP_DIR /app

# Create the app directory
RUN mkdir $APP_DIR

# Set the working directory
WORKDIR $APP_DIR

# Update the package lists and upgrade the system
RUN apt-get update && \
    apt-get upgrade -y

# Install dependencies
RUN apt-get install -y \
    build-essential \
    curl \
    git \
    libbz2-dev \
    libffi-dev \
    liblzma-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    llvm \
    make \
    netbase \
    nginx \
    tk-dev \
    wget \
    xz-utils \
    zlib1g-dev

# Install pyenv
RUN curl https://pyenv.run | bash

# Set up pyenv environment variables
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Install latest Python version using pyenv
RUN pyenv install $(pyenv install $PV | grep -v - | grep -v b | tail -1) && \
    pyenv global $PV

# Install nvm and latest Node.js version
ENV NVM_DIR /root/.nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash && \
    . $NVM_DIR/nvm.sh && \
    nvm install $NV && \
    nvm use $NV

# Set up nvm environment variables
ENV NODE_PATH $NVM_DIR/versions/node/$(nvm current)/lib/node_modules
ENV PATH $NVM_DIR/versions/node/$(nvm current)/bin:$PATH

# Clone the repository
ARG GITURL=https://github.com/cc-d/fedrit.git
RUN git clone $GITURL

# Set the working directory for the cloned repository
WORKDIR fedrit/

# Copy the nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Set up Python virtual environment and install dependencies
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Run Django migrations
RUN python manage.py makemigrations && \
    python manage.py migrate

# Install frontend dependencies
RUN npm ci --prefix frontend

# Build frontend assets
RUN npm run build --prefix frontend

# Final stage
FROM ubuntu:22.04

ENV APP_DIR /app
WORKDIR $APP_DIR

# Copy files from build stage
COPY --from=build $APP_DIR/fedrit $APP_DIR/fedrit
COPY --from=build /etc/nginx/nginx.conf /etc/nginx/nginx.conf

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y \
    nginx \
    python3

EXPOSE 8000
EXPOSE 3000
EXPOSE 80

