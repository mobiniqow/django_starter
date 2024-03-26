#!/bin/bash

# make directory
pip install -r req.txt
sudo mkdir -p "/var/html/www/{{cookiecutter.app_name}}/static/"
echo "static directory created"

sudo mkdir -p "/var/html/www/{{cookiecutter.app_name}}/media/"
echo "media directory created"

sudo mkdir -p "/var/html/www/{{cookiecutter.app_name}}/template/"
echo "template directory created"

# create database
sudo chmod +X create_db.sh
sh ./create_db.sh

# deploy database
sudo  cp ./{{cookiecutter.app_name}}.config  /etc/nginx/sites-available/{{cookiecutter.app_name}}
sudo ln -sf /etc/nginx/sites-available/{{cookiecutter.app_name}}  /etc/nginx/sites-enabled/{{cookiecutter.app_name}}
sudo  cp ./{{cookiecutter.app_name}}.service  /etc/systemd/system/{{cookiecutter.app_name}}.service
sudo  cp ./{{cookiecutter.app_name}}.socket  /etc/systemd/system/{{cookiecutter.app_name}}.socket
sudo systemctl daemon-reload
python -m virtualenv venv

source ./venv/bin/activate

pip install -r req.txt

sudo nginx -t

sudo systemctl restart nginx

echo "sudo systemctl restart"
sudo systemctl restart {{cookiecutter.app_name}}.socket
sudo systemctl restart {{cookiecutter.app_name}}.server

sudo systemctl enable {{cookiecutter.app_name}}.socket

black .

echo "done"
