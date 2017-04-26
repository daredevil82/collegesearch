#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

# Set provisioning variables
PROJECT_NAME=collegesearch

DB_USER=dev
DB_PASS=default123

VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME
BASH_RC='/home/vagrant/.bashrc'

echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.5" >> $BASH_RC
source $BASH_RC

# get postgres 9.6.x
PG_APT_REPO_SRC=/etc/apt/sources.list.d/pgdg.list
if [ ! -f $PG_APT_REPO_SRC ]; then
    echo "Adding Postgres repository and key to aptitude"
    echo "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main" > "$PG_APT_REPO_SRC"

    # Add Postgres repository key
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
fi

# need in order to add apt-add-repository command
apt-get install -y software-properties-common python3-software-properties

# add node and npm
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -

echo "Updating Ubuntu repositories and installed packages"

apt-get update -y
apt-get upgrade -y

echo "Installing required dependencies for project"
apt-get install -y python3-dev python3-pip autotools-dev blt-dev bzip2 dpkg-dev g++-multilib gcc-multilib libbluetooth-dev libbz2-dev libffi-dev \
    libffi6 libffi6-dbg libgdbm-dev libgpm2 libncursesw5-dev libreadline-dev libssl-dev libtinfo-dev \
    mime-support net-tools python3-crypto python3-mox3 python-ply quilt tk-dev zlib1g zlib1g-dev build-essential libxml2 \
    libxml2-dev libxslt1.1 libxslt1-dev nodejs apache2 libapache2-mod-wsgi-py3 python-gdal libgeos-dev postgresql-9.6 postgresql-contrib-9.6 \
    postgresql-9.6-pgrouting postgresql-9.6-postgis-2.3 postgresql-9.6-postgis-2.3-scripts postgresql-server-dev-9.6
apt-get autoremove -y


echo "Setting up Postgres with the following:"
echo "  USERNAME: $DB_USER"
echo "  PASSWORD: $DB_PASS"
echo "  DATABASE: $PROJECT_NAME"
echo ""

PG_CONF="/etc/postgresql/9.6/main/postgresql.conf"
PG_HBA="/etc/postgresql/9.6/main/pg_hba.conf"

# Edit pg conf to listen to * addresses
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Set default encoding
echo "client_encoding = utf8" >> "$PG_CONF"

# Copy pg_hba.conf file for auth settings & restart server
service postgresql stop
cp /home/vagrant/project/provision/files/pg_hba.conf "$PG_HBA"
service postgresql restart

# Create user and database
cat << EOF | su - postgres -c psql
-- Create the database user:
CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASS' SUPERUSER CREATEDB;

-- Create database:
CREATE DATABASE $DB_NAME WITH OWNER=$DB_USER LC_COLLATE='en_US.utf8' LC_CTYPE='en_US.utf8' ENCODING='UTF8' TEMPLATE=template0;
EOF

echo "Adding the following extensions:"
echo "  postgis"
echo "  pgrouting"
echo "  hstore"
echo "  fuzzystrmatch"
psql -U $DB_USER -d $DB_NAME -c 'CREATE EXTENSION postgis;'
psql -U $DB_USER -d $DB_NAME -c 'CREATE EXTENSION pgrouting;'
psql -U $DB_USER -d $DB_NAME -c 'CREATE EXTENSION hstore;'
psql -U $DB_USER -d $DB_NAME -c 'CREATE EXTENSION fuzzystrmatch;'

#echo "Installing gdal 2.x from source"

mkdir ~/download
cd ~/download
wget http://download.osgeo.org/gdal/2.1.3/gdal-2.1.3.tar.gz
tar -xvf gdal-2.1.3.tar.gz
cd gdal-2.1.3
./configure --with-python=/usr/bin/python3 --with-pg=yes --with-geos=yes
make
make install

echo "Configuring Virtualenv"

if [[ ! -f /usr/local/bin/virtualenvwrapper.sh ]]; then
    pip3 install -U pip
    pip3 install -U virtualenvwrapper
fi

if ! grep -Fq "WORKON_HOME" $BASH_RC; then
    echo "Exporting virtualenv variables"
    echo "export WORKON_HOME=/home/vagrant/.virtualenvs"  >> $BASH_RC
    echo "export PROJECT_HOME=/home/vagrant/$PROJECT_NAME" >> $BASH_RC
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> $BASH_RC
fi

pip3 install --upgrade pip # install latest pip version

WORKON_HOME=/home/vagrant/.virtualenvs
PROJECT_HOME=/home/vagrant/$PROJECT_NAME
source /usr/local/bin/virtualenvwrapper.sh
source $BASH_RC

# mkvirtualenv -p "/usr/bin/python3.6" --clear -a "/home/vagrant/project" $PROJECT_NAME
mkvirtualenv -p "/usr/bin/python3.5" -r "/home/vagrant/project/requirements.txt" -a "/home/vagrant/project" $PROJECT_NAME