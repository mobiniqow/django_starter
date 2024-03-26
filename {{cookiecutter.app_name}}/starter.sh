#!/bin/bash

mkdir -p "/var/html/www/{{cookiecutter.app_name}}/static/"
echo "static directory created"

mkdir -p "/var/html/www/{{cookiecutter.app_name}}/media/"
echo "media directory created"

mkdir -p "/var/html/www/{{cookiecutter.app_name}}/template/"
echo "template directory created"

sudo  cp ./{{cookiecutter.app_name}}.config  /etc/nginx/sites-available/{{cookiecutter.app_name}}
sudo ln -sf /etc/nginx/sites-available/{{cookiecutter.app_name}}  /etc/nginx/sites-enabled/{{cookiecutter.app_name}}
sudo  cp ./{{cookiecutter.app_name}}.service  /etc/systemd/system/{{cookiecutter.app_name}}.service
sudo  cp ./{{cookiecutter.app_name}}.socket  /etc/systemd/system/{{cookiecutter.app_name}}.socket

python -m virtualenv venv

source ./venv/bin/activate

pip install -r req.txt

sudo systemctl restart {{cookiecutter.app_name}}.socket
sudo systemctl restart {{cookiecutter.app_name}}.server
echo "sudo systemctl restart"

sudo systemctl enable {{cookiecutter.app_name}}.socket

echo "done"