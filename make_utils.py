import sys
import os
import subprocess
import argparse
from pathlib import Path
import logging
import glob
import re
import json

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
    p = Path('.')
    return [x for x in p.iterdir() if str(x).startswith("Dockerfile_")]

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
    logger.info("Building image '%s' from file %s" % (image_name, image_path))
    image_build_cmd = """docker build -t %s -f %s .""" % (image_name, image_path)
    return_value = os.system(image_build_cmd)
    if return_value:
        logger.error("Building for %s failed!" % image_name)
        raise Exception("Building for %s failed!" % image_name)

def push(image_name):
    cmd_tag = "docker tag %s up42/%s" % (image_name, image_name)
    return_value = os.system(cmd_tag)
    if return_value:
        logger.error("Tagging for %s failed!" % image_name)
        raise Exception("Tagging for %s failed!" % image_name)
    cmd_pushing = """docker push %s/%s""" % (UP42_BASE_IMAGE_PREFIX, image_name)
    return_value = os.system(cmd_pushing)
    if return_value:
        logger.error("Pushing for %s failed!" % image_name)
        raise Exception("Pushing for %s failed!" % image_name)

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
            logger.error("No image named %s" % args.build)

    if args.push:
        login()
        if args.push == "all":
            for image_name in all_images:
                push(image_name)
        elif args.push in all_images:
            push(args.push)
        else:
            logger.error("No image named %s" % args.push)
