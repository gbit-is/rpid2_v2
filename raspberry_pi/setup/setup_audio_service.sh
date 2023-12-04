#!/usr/bin/env bash
set -o pipefail


script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $script_dir



./create_audio_service.sh

sudo cp audio_server.service /etc/systemd/system/
sudo systemctl enable audio_server
sudo systemctl start audio_server
