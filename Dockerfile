FROM ubuntu:22.04

# Set environment variable for the app directory
ENV APP_DIR /app

# Create the app directory
RUN mkdir $APP_DIR

# Set the working directory
WORKDIR $APP_DIR

# Update the package lists and upgrade the system
RUN apt-get update
RUN apt-get upgrade -y

# assumed 3.10
RUN apt-get install python3 -y
RUN python3 --version