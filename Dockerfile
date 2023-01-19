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
RUN apt-get install python3 python3-pip python3-venv git nodejs npm -y

RUN git clone https://github.com/cc-d/fedrit.git
WORKDIR fedrit/

RUN npm install --prefix frontend

EXPOSE 8000
EXPOSE 3000

CMD ["sh", "-c", "python3 fedrit/manage.py runserver 0.0.0.0:8000 & npm start --prefix frontend"]