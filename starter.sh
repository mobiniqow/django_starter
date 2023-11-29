#!/bin/bash

sudo  cp ./{{app_nginx_copnfig_name}}.config  /etc/nginx/sites-available/{{app_nginx_copnfig_name}}
sudo ln -sf /etc/nginx/sites-available/{{app_nginx_copnfig_name}}  /etc/nginx/sites-enabled/{{app_nginx_copnfig_name}}
sudo  cp ./{{app_service_name}}.service  /etc/systemd/system/{{app_service_name}}.service
sudo  cp ./{{app_socket_name}}.socket  /etc/systemd/system/{{app_socket_name}}.socket
done
