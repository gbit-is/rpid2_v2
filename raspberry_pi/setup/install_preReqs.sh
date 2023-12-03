#!/usr/bin/env bash


if [[ $(whoami) == "root" ]];then
	echo "run script as pi user, not root"
	exit 1
fi

export script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo apt install beanstalkd -y 
sudo systemctl enable beanstalkd
sudo systemctl start beanstalkd


sudo apt install python3-venv -y

cd $script_dir
cd ..
python3 -m venv ./venv
source ./venv/bin/activate
pip install pystalk
