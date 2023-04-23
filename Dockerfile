# Use Ubuntu 22.04 as base image
FROM ubuntu:22.04 as build

# python/npm versions to use latest versions of
ARG PY_VERSION="3.10"
ARG NODE_VERSION="16.14"

# Set environment variable for the app directory
ENV APP_DIR /app

# Create the app directory
RUN mkdir $APP_DIR

# Set the working directory
WORKDIR $APP_DIR

# Update the package lists and upgrade the system
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago

RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

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
    zlib1g-dev \
    python3-dev \
    python3-venv

# Install pyenv and set up the environment
RUN curl https://pyenv.run | bash && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc && \
    export PYENV_ROOT="$HOME/.pyenv" && \
    export PATH="$PYENV_ROOT/bin:$PATH" && \
    eval "$(pyenv init -)" && \
    pyenv install $PY_VERSION && \
    pyenv global $PY_VERSION && \
    pyenv local $PY_VERSION

ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"

# Install nvm and latest Node.js version
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash && \
    echo 'export NVM_DIR="$HOME/.nvm"' >> ~/.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> ~/.bashrc && \
    export NVM_DIR="$HOME/.nvm" && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use $NODE_VERSION


# Clone the repository
ARG GITURL=https://github.com/cc-d/fedrit.git
RUN git clone $GITURL

# Set the working directory for the cloned repository
WORKDIR fedrit/

# Copy the nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Set up Python virtual environment and install dependencies
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Run Django migrations
RUN . venv/bin/activate && \
    python manage.py makemigrations && \
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
