#!/bin/bash

echo 'Checking dependencies ...'
for i in 'pgrep' 'lsof' 'wget'; do
    if ! [ -x "$(command -v $i)" ]; then
        echo "Error: $i is not installed." >&2
        exit 1
    fi
done

python2 -c "import tabulate" &> /dev/null
if ! [ $? -eq 0 ]; then
    echo "Error: 'tabulate' not found in your python packages." >&2
    exit 2
fi

echo 'Installing ...'
wget "https://raw.githubusercontent.com/mrl-amrl/system-monitor/master/rosmonitor.py" -q -O /tmp/amrl_rosmonitor
sudo cp /tmp/amrl_rosmonitor /usr/bin/rosmonitor
sudo chmod +x /usr/bin/rosmonitor
echo 'The rosmonitor is now installed in your system.'
