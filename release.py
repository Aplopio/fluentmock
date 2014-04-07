#!/usr/bin/env python

from subprocess import check_call
from sys import argv

version = argv[1]
print "Releasing version {version}".format(version=version)

check_call(["ci", "v{version}".format(version=version)])
check_call(["git", "tag", "v{version}".format(version=version)])
check_call(["git", "push", "--tags"])
check_call(["./setup.py", "sdist", "upload"], cwd="target/dist/fluentmock-{version}".format(version=version))
check_call(["./setup.py", "bdist_wheel", "upload"], cwd="target/dist/fluentmock-{version}".format(version=version))
