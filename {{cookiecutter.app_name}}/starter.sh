#!/bin/bash
# make directory 
sudo mkdir -p "/var/html/www/{{cookiecutter.app_name}}/static/" 
sudo chmod -R 777 "/var/html/www/{{cookiecutter.app_name}}/static/"
sudo mkdir -p "/var/log/{{cookiecutter.app_name}}" 
sudo touch  "/var/log/{{cookiecutter.app_name}}/access.log"  
echo "static directory created"

sudo mkdir -p "/var/html/www/{{cookiecutter.app_name}}/media/"
sudo chmod -R 777 "/var/html/www/{{cookiecutter.app_name}}/media/"
echo "media directory created"

sudo mkdir -p "/var/html/www/{{cookiecutter.app_name}}/template/"
sudo chmod -R 777 "/var/html/www/{{cookiecutter.app_name}}/template/"

echo "template directory created"

# create database
sudo chmod +X create_db.sh
sh ./create_db.sh
cd {{cookiecutter.APP_URL}}

# deploy database
sudo  cp ./{{cookiecutter.app_name}}.config  /etc/nginx/sites-available/{{cookiecutter.app_name}} 
sudo ln -sf /etc/nginx/sites-available/{{cookiecutter.app_name}}  /etc/nginx/sites-enabled/{{cookiecutter.app_name}} 
sudo  cp ./{{cookiecutter.app_name}}.service  /etc/systemd/system/{{cookiecutter.app_name}}.service
echo "template directory created"
sudo  cp ./{{cookiecutter.app_name}}.socket  /etc/systemd/system/{{cookiecutter.app_name}}.socket
echo "template directory created"
sudo systemctl daemon-reload

python -m pip install pip

pip install -q -r req.txt

sudo nginx -t

sudo systemctl restart nginx

echo "sudo systemctl restart"
sudo systemctl restart {{cookiecutter.app_name}}.socket
sudo systemctl restart {{cookiecutter.app_name}}.service

sudo systemctl enable  {{cookiecutter.app_name}}.socket 
sudo systemctl restart {{cookiecutter.app_name}}.service

black .

python manage.py makemigrations --settings core.settings.prod
python manage.py migrate --settings core.settings.prod
python manage.py collectstatic --no-input --settings core.settings.prod

sudo certbot --nginx -d {{cookiecutter.DOMAIN}} -d www.{{cookiecutter.DOMAIN}}
sudo systemctl restart nginx
echo "done"
