#!/usr/bin/env python3
"""Setup of py-zabbix."""

import re
from setuptools import setup


def get_variable_from_file(ffile, variable):
    """Get variable from file."""
    variable_re = f"^{variable} = ['\"]([^'\"]*)['\"]"
    with open(ffile, "r", encoding="utf8") as ffile_obj:
        match = re.search(variable_re, ffile_obj.read(), re.M)
    if match:
        return match.group(1)
    return None


def get_requirements(rfile):
    """Get list of required Python packages."""
    requires = []
    with open(rfile, "r", encoding="utf8") as reqfile:
        for line in reqfile.readlines():
            requires.append(line.strip())
    return requires


def get_version():
    """Get package version."""
    return get_variable_from_file("pyzabbix/__init__.py", "__version__")


setup(
    name='zabbix',
    version=get_version(),
    description='Python module to work with zabbix.',
    long_description_content_type='text/markdown',
    long_description="**It's a fork of** "
                     "<https://github.com/adubkov/py-zabbix>.\n\n" +
                     "\n\n" +
                     "Please read more at "
                     "<https://github.com/nixargh/py-zabbix>",
    author='nixargh',
    author_email='nixargh@protonmail.com',
    packages=['pyzabbix'],
    install_requires=get_requirements("./requirements.txt"),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Systems Administration'
    ])
