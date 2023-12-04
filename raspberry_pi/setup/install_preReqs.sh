#!/usr/bin/env bash


if [[ $(whoami) == "root" ]];then
	echo "run script as pi user, not root"
	exit 1
fi

export script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# MQ
sudo apt install beanstalkd -y 
sudo systemctl enable beanstalkd
sudo systemctl start beanstalkd

# Apache
sudo apt install apache2 -y
sudo systemctl enable apache2 
sudo systemctl start apache2
sudo apt-get install libapache2-mod-wsgi-py3 -y



#Python
sudo apt install python3-venv -y

cd $script_dir
cd ..
python3 -m venv ./venv
source ./venv/bin/activate
pip install pystalk
pip install flask
pip install pygame
