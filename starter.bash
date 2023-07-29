#!/bin/bash

cp ./{{app_nginx_copnfig_name}}.config  /etc/nginx/site-available/{{app_nginx_copnfig_name}}
cp ./{{app_nginx_copnfig_name}}.config  /etc/nginx/site-enabled/{{app_nginx_copnfig_name}}
cp ./{{app_service_name}}.service  /etc/systemd/system/{{app_service_name}}.service
cp ./{{app_socket_name}}.socket  /etc/systemd/system/{{app_socket_name}}.socket
done