# Copyright 2022 Tiernan8r
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import setuptools


# import requirements used in development so that the python
# project requirements match
with open('requirements.in', 'r') as fh:  # pylint: disable=unspecified-encoding # noqa: E501
    requirements = []
    for line in fh.readlines():
        line = line.strip()
        if line[0] != '#':
            requirements.append(line)

# import the README of the project
with open("README.md", "r") as fh:  # pylint: disable=unspecified-encoding
    long_description = fh.read()


setuptools.setup(
    name='quantum_computing_project',
    use_scm_version=True,  # tags the project version from the git tag
    setup_requires=['setuptools_scm', 'pytest-runner'],
    packages=setuptools.find_packages(where="src", exclude=['docs', 'tests']),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
)
