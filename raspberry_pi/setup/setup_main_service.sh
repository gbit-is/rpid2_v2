#!/usr/bin/env bash
set -o pipefail


script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $script_dir



./create_service_file.sh

sudo cp rpid2.service /etc/systemd/system/
sudo systemctl enable rpid2
sudo systemctl start rpid2
