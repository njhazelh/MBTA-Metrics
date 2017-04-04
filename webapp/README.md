# MBTA Webapp

## Requirements
Requires Node.js v7.7.3 for development

```bash
wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
nvm install stable
nvm use stable
```

You also want to install yarn to dependency management
```bash
sudo apt-get install yarn
```

Note: The default (`npm`) may also work, but yarn is faster.

## Development
```bash
cd <webapp_root>

# Install dependencies
yarn

# Start the development server on port 8080
# This will enable you to see the webapp in your browser
yarn dev
```

```bash
# Run the linter
yarn lint

# Have the linter fix style issues
yarn lint:fix
```

## Deployment
```bash
webpack build:prod
<copy to webserver>
```

### Deployment Configuration
This project is currently running on Nginx 1.10.2.  For it to work, several settings are required.

#### Resource URLs
- The dashboard is located at `http://<webserver>/`
- The dashboard expects the API to be at `http://<webserver>/data/`.
- The API generally runs on `http://<webserver>:9000`, but isn't exposed to the internet.

For this to work, you will need to proxy requests for `/data` to the gunicorn
server (on port 9000).  This is a nice way of doing things, because it bypasses
the need to X-Site security policies.

```nginx
upstream api_server {
    server localhost:9000 fail_timeout=4;
}

server {
  ...
  location /data {
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $http_host;
    proxy_redirect off;
    proxy_pass http://api_server;
  }
  ...
}
```

#### Making things fast!
The dashboard is a single page application, which loads *A LOT* of JavaScript and
other resources up front.  This isn't a problem for most modern computers/phones considering
that you perform several optimizations.

##### Production Optimization
The `yarn build:prod` script will perform a variety of different optimizations to reduce
the uncompressed size of resources.  For example, it will minimize whitespace in javascript.

It also prefixes the filenames with a hashcode of the contents.  This is important, because it
means that we can tell if changes have been made and not hit the browser cache.

##### Gzip
Gzip significantly reduces the amount of data sent over the network.

You should definitely read the Nginx documentation, but the two key lines are:
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/javascript;
```

##### Browser Caching
```nginx
map $sent_http_content_type $expires {
    default                 off;
    text/html               epoch;
    text/css                max;
    application/javascript  max;
    ~image/                 max;
}

server {
  listen  80  default_server;
  listen  [::]:80 default_server;
  ...
  expires $expires;
  ...
}
```

Now you need to reload the config by restarting the server.
```bash
sudo service nginx restart
```

Once you have done this.  You just need to load the webpage from the server.
The way it's configured above, the browser will always get the html index, but that
is very small.  The html index references the resources, which have filenames that
are prefixed with a hash of the contents.  If the resource is css, js, or an image,
then the contents may be in the cache, which makes the lookup much faster.

Since the data in the API isn't likely to change much, it might also be worth adding
`application/json` to make that easier two, but it depends on how often you plan to
reload the same data.

##### HTTP/2
HTTP/2 makes downloading resources significantly faster.  At the moment, it's only
available if you're using HTTPS with nginx (you are... right?)  I leave this
up to the reader.
