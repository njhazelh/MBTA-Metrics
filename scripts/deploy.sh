#!/bin/bash

rm -rf /var/mbta-app
cp -rp . /var/mbta-app
chown -R mbta-app:mbta-app /var/mbta-app
cd /var/mbta-app
source ./activate.sh

cp scripts/init.d/* /etc/init.d/

for service in scripts/init.d/*; do
    echo "Restarting '$service':"
    cp "$service" /etc/init.d/
    chmod +x "/etc/init.d/$(basename $service)"
    service "$(basename $service)" restart
done

