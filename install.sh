#!/bin/bash

set -e

echo 'Checking dependencies ...'
for i in 'lsof' 'wget'; do
    if ! [ -x "$(command -v $i)" ]; then
        echo "Error: $i is not installed." >&2
        sudo apt install -yq $i
    fi
done

python2 -c "import tabulate" &> /dev/null
if ! [ $? -eq 0 ]; then
    echo "Error: 'tabulate' not found in your python packages." >&2
    
    if ! [ -x "$(command -v pip)" ]; then
        echo "Error: pip is not installed." >&2
        sudo apt install -yq python-pip
    fi
    sudo pip install tabulate
fi

echo 'Installing ...'
wget "https://raw.githubusercontent.com/mrl-amrl/system-monitor/master/rosmonitor.py" -q -O /tmp/amrl_rosmonitor
sudo rm -rf /usr/bin/rosmonitor
sudo mv /tmp/amrl_rosmonitor /usr/bin/rosmonitor
sudo chmod +x /usr/bin/rosmonitor
echo 'The rosmonitor is now installed in your system.'
