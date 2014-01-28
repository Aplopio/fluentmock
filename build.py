#   fluentmock
#   Copyright 2013-2014 Michael Gruber
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

from pybuilder.core import Author, init, use_plugin

use_plugin('python.core')

use_plugin('copy_resources')
use_plugin('filter_resources')

use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('python.flake8')
use_plugin('python.install_dependencies')
use_plugin('python.unittest')

url = 'https://github.com/aelgru/fluentmock'
description = 'Please visit {0} for more information!'.format(url)

authors = [Author('Michael Gruber', 'aelgru@gmail.com')]
license = 'Apache License, Version 2.0'
summary = "Fluent interface facade for Michael Foord's mock."
version = '0.1.16'

default_task = ['analyze', 'publish']


@init
def set_properties(project):
    project.build_depends_on('PyHamcrest')
    project.build_depends_on('wheel')

    project.depends_on('mock')

    project.set_property('dir_source_integrationtest_python', 'src/unittest')

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
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance'])
