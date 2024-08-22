#
# foris-controller-haas-module
# Copyright (C) 2020-2023 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
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

import pytest

from foris_controller_testtools.fixtures import UCI_CONFIG_DIR_PATH
from foris_controller_testtools.utils import get_uci_module, check_service_result


def test_get_settings(file_root_init, infrastructure):
    res = infrastructure.process_message(
        {"module": "haas", "action": "get_settings", "kind": "request"}
    )
    assert "errors" not in res
    assert "data" in res
    assert res["data"]["enabled"] is True
    assert res["data"]["token"] == ""  # initial settings with unset token


def test_update_settings(file_root_init, uci_configs_init, infrastructure):
    new_token = "81f2cd612ea14da5bbaeaf08e7dc2a39"
    data = {"token": new_token, "enabled": False}
    res = infrastructure.process_message(
        {
            "module": "haas",
            "action": "update_settings",
            "kind": "request",
            "data": data,
        }
    )

    assert res == {
        "module": "haas",
        "action": "update_settings",
        "kind": "reply",
        "data": {"result": True},
    }

    res = infrastructure.process_message(
        {
            "module": "haas",
            "action": "get_settings",
            "kind": "request",
        }
    )

    assert res["data"]["token"] == new_token


@pytest.mark.parametrize("new_token", ["81f2cd612ea14da5bbaeaf08e7dc2a39","3e489258c9099ac89096374a48fe04a1b46e9314142f6d02"])
@pytest.mark.only_backends(["openwrt"])
def test_update_settings_uci(
    file_root_init,
    uci_configs_init,
    infrastructure,
    new_token,
    init_script_result,
):
    data = {"token": new_token, "enabled": False}

    res = infrastructure.process_message(
        {
            "module": "haas",
            "action": "update_settings",
            "kind": "request",
            "data": data,
        }
    )

    assert res == {
        "module": "haas",
        "action": "update_settings",
        "kind": "reply",
        "data": {"result": True},
    }

    uci = get_uci_module(infrastructure.name)

    with uci.UciBackend(UCI_CONFIG_DIR_PATH) as backend:
        data = backend.read()
    token = uci.get_option_named(data, "haas", "settings", "token")
    assert new_token == token

    check_service_result("firewall", "restart", True)
