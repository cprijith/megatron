#!/usr/bin/env python

import os
from setuptools import find_packages, setup

REQUIREMENTS = []
EXCLUDED = ['static', 'templates', 'target', 'assembly']
DESCRIPTION = "Transform data from different sources into a common format, with hooks to log, validate and monitor"

# set project root to correct working dir
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# version number tracking
with open(os.path.join(os.path.dirname(__file__), '.bumpversion.cfg')) as version:
    for line in version:
        if 'current_version' in line:
            VERSION = line.split('=')[-1].strip()
            print("VERSION: {0}".format(VERSION))
        elif 'artifact_id' in line:
            ARTIFACT_ID = line.split('=')[-1].strip()
            print("ARTIFACT ID: {0}".format(ARTIFACT_ID))

setup(
    name=ARTIFACT_ID,
    version=VERSION,
    packages=find_packages(exclude=EXCLUDED),
    include_package_data=True,
    license='proprietory',
    install_requires=REQUIREMENTS,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    zip_safe=False,
    scripts=[],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[
        'artifactId :: %s' % ARTIFACT_ID,
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.x'
    ],
)
