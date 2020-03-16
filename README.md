# UP42 Docker images

Docker base images used by blocks.

## Getting started

### Python

For the initial setup, you will need to create the virtual environment using Python 3.7.

The following commands use virtualenvwrapper (https://virtualenvwrapper.readthedocs.io/) which
is the recommended way for this setup.

```
mkvirtualenv --python=$(which python3.7) up42-docker
```

### Environment variables

In order to test pushing images into DockerHub make sure to add `DOCKERHUB_PASS` and `DOCKERHUB_USERNAME` to your environment.
```bash
export DOCKERHUB_USERNAME=[USERNAME]
export DOCKERHUB_PASS=[PASSWORD]
```

## Usage

To build all base images:
```bash
make build all
```
