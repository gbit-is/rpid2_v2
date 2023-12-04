#!/usr/bin/env bash

set -o pipefail

#export python_path=$(which python3)
export script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $script_dir
cd ..

source ./venv/bin/activate
export python_path=$(which python3)

cd ./bin

export run_dir=$(pwd)
export exe_file="${run_dir}/gamepad.py"


cd $script_dir 

cat rpid2.service_template | envsubst > rpid2.service

