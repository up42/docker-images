import argparse
import glob
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
UP42_BASE_IMAGE_PREFIX = 'up42'


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(LOG_FORMAT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = get_logger(__name__)


def image_paths():
    p = Path('./dockerfiles/blocks/')
    return [x for x in p.glob("**/*") if "Dockerfile_" in str(x)]

def image_names():
    images = image_paths()
    return [str(image.name).replace("_","-").replace("Dockerfile", UP42_BASE_IMAGE_PREFIX) for image in images]

def base_images():
    base_images_map = {}
    for image_path in image_paths():
        base_image_name = str(image_path.name).replace("_","-").replace("Dockerfile", UP42_BASE_IMAGE_PREFIX)
        base_images_map[base_image_name] = str(image_path)
    return base_images_map

def build(image_name, image_path):
    logger.info("\n")
    logger.info(f"Building image '{image_name}' from file {image_path}")
    image_build_cmd = f"""docker build -t {image_name} -f {image_path} ."""
    return_value = os.system(image_build_cmd)
    if return_value:
        logger.error(f"Building for {image_name} failed!")
        raise Exception(f"Building for {image_name} failed!")

def push(image_name):
    cmd_tag = f"docker tag {image_name} up42/{image_name}"
    return_value = os.system(cmd_tag)
    if return_value:
        logger.error(f"Tagging for {image_name} failed!")
        raise Exception(f"Tagging for {image_name} failed!" % image_name)
    cmd_pushing = f"""docker push {UP42_BASE_IMAGE_PREFIX}/{image_name}"""
    return_value = os.system(cmd_pushing)
    if return_value:
        logger.error(f"Pushing for {image_name} failed!")
        raise Exception(f"Pushing for {image_name} failed!")

def login():
    cmd_login = """echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin"""
    return_value = os.system(cmd_login)
    if return_value:
        logger.error("Login to DockerHub failed! Set DOCKERHUB_PASS and DOCKERHUB_USERNAME in your environment.")
        raise Exception("Login to DockerHub failed!")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Utilities for building and pushing images')
    parser.add_argument('--list-images', action='store_true', help='List all images')
    parser.add_argument('--build', type=str, help='Build all images')
    parser.add_argument('--push', type=str, help='Push all images')

    args = parser.parse_args()

    all_images = base_images()

    if args.list_images:
        images = image_names()
        [logger.info(image) for image in images]

    if args.build:
        if args.build == "all":
            for image_name in all_images:
                build(image_name, all_images[image_name])
        elif args.build in all_images:
            build(args.build, all_images[args.build])
        else:
            logger.error(f"No image named {args.build}")

    if args.push:
        login()
        if args.push == "all":
            for image_name in all_images:
                push(image_name)
        elif args.push in all_images:
            push(args.push)
        else:
            logger.error(f"No image named {args.push}")
