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
**Work in Progress**

```bash
webpack build:prod
...
```

