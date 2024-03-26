# ساخت دیتابیس
sudo -u postgres psql -c "CREATE DATABASE {{cookiecutter.DB_NAME}};"
sudo -u postgres psql -c "CREATE USER {{cookiecutter.DB_USER}} WITH PASSWORD '{{cookiecutter.DB_PASSWORD}}';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {{cookiecutter.DB_NAME}} TO {{cookiecutter.DB_USER}};"
echo "Database created"