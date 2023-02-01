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

# assumed python 3.10
RUN apt-get install python3 python3-pip python3-venv git nodejs npm gnupg nginx -y
RUN apt-get install nginx -y

ARG GITURL=https://github.com/cc-d/fedrit.git
RUN git clone $GITURL # 5555

WORKDIR fedrit/
COPY nginx.conf /etc/nginx/nginx.conf

RUN python3 -m venv venv
RUN . venv/bin/activate
RUN pip install -r requirements.txt # cahebreak
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

RUN npm install --prefix frontend

EXPOSE 8000
EXPOSE 3000
EXPOSE 80

CMD ["sh", "-c", "python3 manage.py runserver 0.0.0.0:8000 & npm start --prefix frontend & nginx -g \"daemon off;\""]
