#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

# Set provisioning variables
PROJECT_NAME=collegesearch

DB_USER=dev
DB_PASS=default123

VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME
BASH_RC='/home/vagrant/.bashrc'

# get postgres 9.6.x
PG_APT_REPO_SRC=/etc/apt/sources.list.d/pgdg.list
if [ ! -f $PG_APT_REPO_SRC ]; then
    echo "Adding Postgres repository and key to aptitude"
    echo "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main" > "$PG_APT_REPO_SRC"

    # Add Postgres repository key
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
fi

apt-get install -y software-properties-common python3-software-properties

# add python 3.6 binaries and ubuntu GIS
add-apt-repository ppa:jonathonf/python-3.6
add-apt-repository ppa:ubuntugis/ppa

# add node and npm
echo "Adding nodesource repository"
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -

# add yarn
echo "Adding yarn repository"
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

echo "Updating Ubuntu repositories and installed packages"
apt-get update -y
apt-get upgrade -y

echo "Installing required dependencies for project"
apt-get install -y python3.6 python3.6-dev python3-dev python3-pip autotools-dev blt-dev bzip2 dpkg-dev g++-multilib \
    gcc-multilib libbz2-dev libffi-dev libffi6 libffi6-dbg libgdbm-dev libgpm2 libncursesw5-dev libreadline-dev \
    mime-support net-tools python3-crypto python3-mox3 python-ply quilt tk-dev zlib1g zlib1g-dev build-essential libxml2 \
    libxml2-dev libxslt1.1 libxslt1-dev nodejs yarn postgresql-9.6 postgresql-9.6 postgresql-contrib-9.6 libgdal-dev \
    postgresql-server-dev-9.6 python3-gdal libssl-dev libtinfo-dev python3.6-venv postgresql-9.6-postgis-2.4 postgresql-9.6-postgis-2.4-scripts \
    postgresql-9.6-pgrouting
apt-get autoremove -y

echo "*:*:*:$DB_USER:$DB_PASS" > ".pgpass"
source $BASH_RC
chmod 600 ".pgpass"

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

GEOS_VERSION="3.4.2"
GEOS="http://download.osgeo.org/geos/geos-$GEOS_VERSION.tar.bz2"

mkdir -p /home/vagrant/download
cd /home/vagrant/download

echo "Retrieving GEOS source code tarball"
wget $GEOS

tar -xvf "geos-$GEOS_VERSION.tar.bz2"
cd "geos-$GEOS_VERSION"
./configure
make
make install

# Create user and database
cat << EOF | sudo su - postgres -c psql
CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASS' SUPERUSER CREATEDB;

CREATE DATABASE $PROJECT_NAME WITH OWNER=$DB_USER LC_COLLATE='en_US.utf8' LC_CTYPE='en_US.utf8' ENCODING='UTF8' TEMPLATE=template0;
CREATE DATABASE test_$PROJECT_NAME WITH OWNER=$DB_USER LC_COLLATE='en_US.utf8' LC_CTYPE='en_US.utf8' ENCODING='UTF8' TEMPLATE=template0;
EOF

echo "Adding the following extensions to $PROJECT_NAME and test_$PROJECT_NAME databases:"
echo "  postgis"
echo "  pgrouting"
echo "  hstore"
echo "  fuzzystrmatch"
psql -U $DB_USER -d $PROJECT_NAME -w -c 'CREATE EXTENSION postgis;'
psql -U $DB_USER -d $PROJECT_NAME -w -c 'CREATE EXTENSION pgrouting;'
psql -U $DB_USER -d $PROJECT_NAME -w -c 'CREATE EXTENSION hstore;'
psql -U $DB_USER -d $PROJECT_NAME -w -c 'CREATE EXTENSION fuzzystrmatch;'

psql -U $DB_USER -d "test_$PROJECT_NAME" -w -c 'CREATE EXTENSION postgis;'
psql -U $DB_USER -d "test_$PROJECT_NAME" -w -c 'CREATE EXTENSION pgrouting;'
psql -U $DB_USER -d "test_$PROJECT_NAME" -w -c 'CREATE EXTENSION hstore;'
psql -U $DB_USER -d "test_$PROJECT_NAME" -w -c 'CREATE EXTENSION fuzzystrmatch;'

echo "Configuring Virtualenv"

#if [[ ! -f /usr/local/bin/virtualenvwrapper.sh ]]; then
#    python3.6 -m pip install -U pip
#    python3.6 -m pip install -U virtualenvwrapper
#fi
#

WORKON_HOME=/home/vagrant/envs/collegesearch
PROJECT_HOME=/home/vagrant/project/$PROJECT_NAME
if ! grep -Fq "WORKON_HOME" $BASH_RC; then
    echo "Exporting virtualenv variables"
    echo "export WORKON_HOME=$WORKON_HOME"  >> $BASH_RC
    echo "export PROJECT_HOME=$PROJECT_HOME" >> $BASH_RC

fi

source $BASH_RC
python3.6 -m venv $WORKON_HOME
chown -R vagrant:vagrant $WORKON_HOME
echo "export PATH=$WORKON_HOME/bin:$PATH" >> $BASH_RC
source $BASH_RC
source activate
pip install -r "/home/vagrant/project/requirements.txt"

npm install -g create-react-app

mkdir -p "/home/vagrant/project/logs"