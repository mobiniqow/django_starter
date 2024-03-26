#!/bin/bash

# make directory
pip install -r req.txt
sudo mkdir -p "/var/html/www/{{cookiecutter.APP_NAME}}/static/"
echo "static directory created"

sudo mkdir -p "/var/html/www/{{cookiecutter.APP_NAME}}/media/"
echo "media directory created"

sudo mkdir -p "/var/html/www/{{cookiecutter.APP_NAME}}/template/"
echo "template directory created"

# create database
sudo chmod +X create_db.sh
./create_db.sh

# deploy database
sudo  cp ./{{cookiecutter.APP_NAME}}.config  /etc/nginx/sites-available/{{cookiecutter.APP_NAME}}
sudo ln -sf /etc/nginx/sites-available/{{cookiecutter.APP_NAME}}  /etc/nginx/sites-enabled/{{cookiecutter.APP_NAME}}
sudo  cp ./{{cookiecutter.APP_NAME}}.service  /etc/systemd/system/{{cookiecutter.APP_NAME}}.service
sudo  cp ./{{cookiecutter.APP_NAME}}.socket  /etc/systemd/system/{{cookiecutter.APP_NAME}}.socket
sudo systemctl daemon-reload
python -m virtualenv venv

source ./venv/bin/activate

pip install -r req.txt

sudo nginx -t

sudo systemctl restart nginx

echo "sudo systemctl restart"
sudo systemctl restart {{cookiecutter.APP_NAME}}.socket
sudo systemctl restart {{cookiecutter.APP_NAME}}.server

sudo systemctl enable {{cookiecutter.APP_NAME}}.socket

black .

echo "done"
