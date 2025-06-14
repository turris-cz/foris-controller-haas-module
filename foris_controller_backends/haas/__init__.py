#
# foris-controller-haas-module
# Copyright (C) 2025 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
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

import logging
from pathlib import Path

from foris_controller_backends.uci import UciBackend, get_option_named
from foris_controller_backends.services import OpenwrtServices

logger = logging.getLogger(__name__)


class HaasUci:
    @staticmethod
    def get_service():
        if Path("/etc/init.d/sshoxy-haas").exists():
            # new proxy present
            return "sshoxy-haas"
        else:
            # fallback to old proxy
            return "haas-proxy"

    @classmethod
    def get_settings(cls):
        with UciBackend() as backend:
            haas_data = backend.read("haas")

        token = get_option_named(haas_data, "haas", "settings", "token", "")

        with OpenwrtServices() as services:
            enabled = services.is_enabled(HaasUci.get_service())

        return {
            "token": token,
            "enabled": enabled,
        }

    @classmethod
    def update_settings(cls, token, enabled):
        with UciBackend() as backend:
            backend.set_option("haas", "settings", "token", token)

        with OpenwrtServices() as services:
            service = HaasUci.get_service()
            if enabled:
                services.enable(service, fail_on_error=False)
                services.restart(service, fail_on_error=False)
            else:
                services.disable(service, fail_on_error=False)
                services.stop(service, fail_on_error=False)
            services.restart("firewall", fail_on_error=False)

        return True
