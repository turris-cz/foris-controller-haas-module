#
# foris-controller-haas-module
# Copyright (C) 2020 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#

from setuptools import setup

from foris_controller_haas_module import __version__

DESCRIPTION = """
haas module for Foris Controller
"""

setup(
    name="foris-controller-haas-module",
    version=__version__,
    author="CZ.NIC, z.s.p.o. (http://www.nic.cz/)",
    author_email="packaging@turris.cz",
    packages=[
        "foris_controller_haas_module",
        "foris_controller_backends",
        "foris_controller_backends.haas",
        "foris_controller_modules",
        "foris_controller_modules.haas",
        "foris_controller_modules.haas.handlers",
    ],
    package_data={"foris_controller_modules.haas": ["schema", "schema/*.json"]},
    namespace_packages=["foris_controller_modules", "foris_controller_backends"],
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "foris-controller @ git+https://gitlab.nic.cz/turris/foris-controller/foris-controller.git"
    ],
    setup_requires=["pytest-runner", "flake8"],
    tests_require=["pytest", "foris-controller-testtools", "foris-client", "ubus", "paho-mqtt"],
    dependency_links=[
        "git+https://gitlab.nic.cz/turris/foris-controller/foris-controller-testtools.git#egg=foris-controller-testtools",
        "git+https://gitlab.nic.cz/turris/foris-controller/foris-client.git#egg=foris-client",
    ],
    include_package_data=True,
    zip_safe=False,
)
