#!/usr/bin/env bash -eux
# Filename:     mysql.sh
# Purpose:      install mysql server for openthinclient installer
#------------------------------------------------------------------------------

export DEBIAN_FRONTEND="noninteractive"

MYSQL_ROOT_PWD=root

MYSQL_OTC_USER=openthinclient
MYSQL_OTC_PWD=openthinclient

echo $MYSQL_ROOT_PWD
echo $MYSQL_OTC_PWD

sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password $MYSQL_ROOT_PWD"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $MYSQL_ROOT_PWD"

sudo apt-get update
#sudo apt-get install -y python-software-properties
echo "==> Installing mysql-server package"
sudo apt-get -y install mysql-server
#sed -i "s/^bind-address/#bind-address/" /etc/mysql/my.cnf
echo "==> Setting mysql root user privileges"
mysql -u root -p${MYSQL_ROOT_PWD} -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'root' WITH GRANT OPTION; FLUSH PRIVILEGES;"

echo "==> Creating database for otc-manager"
sudo mysql -uroot -p${MYSQL_ROOT_PWD} -e "CREATE DATABASE openthinclient;"

echo "==> Creating openthinclient user in mysql"
sudo mysql -uroot -p${MYSQL_ROOT_PWD} -e "CREATE USER openthinclient@'localhost' IDENTIFIED BY '$MYSQL_OTC_PWD';"

echo "==> Granting permissions to all tables in database openthinclient to user openthinclient"
sudo mysql -uroot -p${MYSQL_ROOT_PWD} -e "GRANT ALL PRIVILEGES ON openthinclient.* TO openthinclient@'localhost' IDENTIFIED BY '$MYSQL_OTC_PWD';"

echo "==> Updating mySQL privileges"
sudo mysql -uroot -p${MYSQL_ROOT_PWD} -e "FLUSH PRIVILEGES;"

echo "==> Restarting mySQL database server"
sudo /etc/init.d/mysql restart

echo "==> Checking mySQL database server status"
sudo service mysql status

echo "==> Listing current databases"
sudo mysql -uroot -p${MYSQL_ROOT_PWD} -e "SHOW DATABASES;"

echo "==> Testing database access as ${MYSQL_OTC_USER} user"
sudo mysql -u${MYSQL_OTC_USER} -p${MYSQL_OTC_PWD} -e "SHOW DATABASES;"