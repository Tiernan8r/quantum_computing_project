import setuptools


# import requirements used in development so that the python
# project requirements match
with open('requirements.in', 'r') as fh:
    requirements = []
    for line in fh.readlines():
        line = line.strip()
        if line[0] != '#':
            requirements.append(line)

# import the README of the project
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='quantum_computing_project',
    use_scm_version=True, # tags the project version from the git tag
    setup_requires=['setuptools_scm', 'pytest-runner'],
    packages=setuptools.find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
)

