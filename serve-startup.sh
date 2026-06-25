#!/bin/bash

set -e

echo "===== Updating Server ====="
apt update && apt upgrade -y

echo "===== Installing Python ====="
apt install -y python3 python3-pip python3-venv git

echo "===== Installing MySQL ====="
apt install -y mysql-server

systemctl enable mysql
systemctl start mysql



echo "===== Configuring APP ====="
PRODUCT_KEY="my_product_key"
DO_MAIN="zodex.in"
DB_NAME="myapp_db"
DB_USER="myapp_user"
DB_PASS="StrongPassword123"
DB_HOST="localhost"
DB_PORT="3306"

echo "===== Creating Database ====="

mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "===== Creating Project Folder ====="
mkdir /var/www
cd /var/www
git clone https://github.com/meghasainiahit-dev/crm-.git
cd /var/www/crm-
echo "===== Creating Virtual Environment ====="

python3 -m venv env
source env/bin/activate

echo "===== Installing Requirements ====="

if [ -f requirements.txt ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "requirements.txt not found, skipping..."
fi

echo "===== Creating .env ====="

cat > .env <<EOF
DATABASE_URL=mysql+pymysql://$DB_USER:$DB_PASS@$DB_HOST:$DB_PORT/$DB_NAME
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASS
PRODUCT_KEY=$PRODUCT_KEY

EOF

echo "===== Installing Redis ====="
apt update
apt install -y redis-server

echo "===== Enabling Redis ====="
systemctl enable redis-server
systemctl start redis-server

echo "===== Redis Status ====="
systemctl status redis-server --no-pager
echo "===== Redis Test ====="
redis-cli ping
redis-cli
SET name "Redis Test"
GET name


echo "===== 1. Redis Test Completed ====="
cat >  /var/www/crm-redis_test.py <<EOF
import sys
import redis


def test_redis():
    try:
        r = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True,
            socket_connect_timeout=5
        )

        # Connection Test
        r.ping()

        # Write Test
        r.set("redis_test_key", "Redis Working")

        # Read Test
        value = r.get("redis_test_key")

        print("✅ Redis Connected Successfully")
        print(f"✅ Test Value: {value}")

        # Cleanup
        r.delete("redis_test_key")

        print("✅ Redis Read/Write Test Passed")
        return True

    except Exception as e:
        print(f"❌ Redis Test Failed: {e}")
        return False


if __name__ == "__main__":
    success = test_redis()
    sys.exit(0 if success else 1)
EOF 

python3 redis_test.py

if [ $? -eq 0 ]; then
    echo "Redis is working properly"
else
    echo "Redis test failed"
fi

echo "===== 2. Redis Test Completed ====="

echo "===== Redis Installed Successfully ====="






echo "===== Starting Application ====="

cd /var/www/crm-
source env/bin/activate


cd /etc/systemd/system/

cat > myapp.service <<EOF
[Unit]
Description=My Python CRM App
After=network.target

[Service]
User=root
Group=root

WorkingDirectory=/var/www/crm-

Environment="PATH=/var/www/crm-/env/bin"

ExecStart=/var/www/crm-/env/bin/uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl start myapp

sudo systemctl status myapp

echo "===== Application Started Successfully ====="

echo "===== Installing Caddy ====="


sudo apt update
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl



curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | \
sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg


curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | \
sudo tee /etc/apt/sources.list.d/caddy-stable.list



sudo apt update
sudo apt install -y caddy


sudo systemctl enable caddy
sudo systemctl start caddy

sudo systemctl status caddy --no-pager

cd /etc/caddy
rm -rf Caddyfile
cat > Caddyfile <<EOF
$DO_MAIN {
    reverse_proxy localhost:8000
}
EOF

sudo systemctl reload caddy
sudo systemctl restart caddy

sudo systemctl status caddy --no-pager

echo "===== Caddy Installed Successfully ====="
echo "===== Domain Configuration Completed ====="



echo "===== Installation Complete ====="