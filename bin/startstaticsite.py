#! /usr/bin/env python

import argparse
import subprocess
import sys

STATICSITE_TEMPLATE_URL = 'https://github.com/carltongibson/staticsite-template/archive/master.zip'

parser = argparse.ArgumentParser(
    description='Create Staticsite Project with `project_name`'
)
parser.add_argument(
    'project_name',
    help="The project_name for your new Staticsite"
)


def start_staticsite():
    args = parser.parse_args()

    sys.stdout.write("Creating Staticsite in {}... ".format(args.project_name))
    sys.stdout.flush()

    subprocess.run(
        ['django-admin',
         'startproject',
         '--template',
         STATICSITE_TEMPLATE_URL,
         args.project_name,
        ]
    )

    sys.stdout.write("Done\n")


if __name__ == '__main__':
    start_staticsite()
