#!/bin/bash

# make directory
mkdir -p "/var/html/www/{{cookiecutter.app_name}}/static/"
echo "static directory created"

mkdir -p "/var/html/www/{{cookiecutter.app_name}}/media/"
echo "media directory created"

mkdir -p "/var/html/www/{{cookiecutter.app_name}}/template/"
echo "template directory created"

# create database
sudo -u postgres psql -c "CREATE DATABASE {{cookiecutter.DB_NAME}};"
sudo -u postgres psql -c "CREATE USER {{cookiecutter.DB_USER}} WITH PASSWORD '{{cookiecutter.DB_PASSWORD}}';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {{cookiecutter.DB_NAME}} TO {{cookiecutter.DB_USER}};"
echo "Database created"

# deploy database
sudo  cp ./{{cookiecutter.app_name}}.config  /etc/nginx/sites-available/{{cookiecutter.app_name}}
sudo ln -sf /etc/nginx/sites-available/{{cookiecutter.app_name}}  /etc/nginx/sites-enabled/{{cookiecutter.app_name}}
sudo  cp ./{{cookiecutter.app_name}}.service  /etc/systemd/system/{{cookiecutter.app_name}}.service
sudo  cp ./{{cookiecutter.app_name}}.socket  /etc/systemd/system/{{cookiecutter.app_name}}.socket

python -m virtualenv venv

source ./venv/bin/activate

pip install -r req.txt

sudo nginx -t

sudo systemctl restart nginx

sudo systemctl restart {{cookiecutter.app_name}}.socket
sudo systemctl restart {{cookiecutter.app_name}}.server
echo "sudo systemctl restart"

sudo systemctl enable {{cookiecutter.app_name}}.socket

echo "done"
