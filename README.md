# UP42 Docker images

Docker base images used by up42 blocks and CI.

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

To build a specific image:
```bash
make build up42-snap-py37
```

See `make list-images`

### Adding a new block base image

When adding a new base image, make sure you create the corresponding `Dockerfile` with the naming convention `Dockerfile_[descriptor snap]_[python version e.g. py37]` - the result image name will be `up42-[descriptor]_[python version]`.

Additionally add another `anchore/image_scan` in the `.circleci/config.yml` for the new base image.
