#!/bin/bash

# Copy Python files to deploy directory and install
rm -rf /var/mbta-app
cp -rp . /var/mbta-app
chown -R mbta-app:mbta-app /var/mbta-app
cd /var/mbta-app
source ./bin/activate.sh
deactivate

# Deploy Services
cp bin/init.d/* /etc/init.d/

for service in bin/init.d/*; do
    echo "Restarting '$service':"
    cp "$service" /etc/init.d/
    chmod +x "/etc/init.d/$(basename $service)"
    service "$(basename $service)" restart
done

# install the webapp
cd webapp
rm -rf /usr/share/ngnix/html
yarn
yarn build:prod
cp -Rf dist/* /usr/share/nginx/html
rm -rf dist
