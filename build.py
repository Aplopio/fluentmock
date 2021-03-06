#   fluentmock
#   Copyright 2013-2015 Michael Gruber
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys
from pybuilder.core import Author, init, use_plugin

use_plugin('python.core')

use_plugin('copy_resources')
use_plugin('filter_resources')

use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('python.flake8')
use_plugin('python.install_dependencies')
use_plugin('python.unittest')

use_plugin('pypi:pybuilder_release_plugin')
use_plugin('pypi:pybuilder_header_plugin')

url = 'https://github.com/aelgru/fluentmock'
description = "Please visit {url}".format(url=url)

authors = [Author('Michael Gruber', 'aelgru@gmail.com')]
license = 'Apache License, Version 2.0'
summary = "Fluent interface facade for Michael Foord's mock."
version = '0.3.0'

default_task = ['analyze', 'check_source_file_headers', 'publish']


@init
def set_properties(project):
    project.build_depends_on('PyHamcrest')
    project.build_depends_on('wheel')

    python_version = sys.version_info[0:2]

    if python_version == (2, 6):
        project.depends_on('importlib')

    project.depends_on('mock')

    project.set_property('coverage_break_build', True)

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('LICENSE.txt')
    project.get_property('copy_resources_glob').append('setup.cfg')

    project.include_file('fluentmock', 'LICENSE.txt')

    project.get_property('filter_resources_glob').append('**/fluentmock/__init__.py')

    project.set_property('flake8_verbose_output', True)
    project.set_property('flake8_break_build', True)
    project.set_property('flake8_include_test_sources', True)

    project.get_property('distutils_commands').append('bdist_wheel')
    project.set_property('distutils_classifiers', [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance'])

    header = open('header.py').read()
    project.set_property('pybuilder_header_plugin_expected_header', header)
    project.set_property('pybuilder_header_plugin_break_build', True)
