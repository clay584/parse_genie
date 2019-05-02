# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

__author__ = "Clay Curtis"
__license__ = "GPLv3"
__email__ = "jccurtis@presidio.com"
__version__ = "1.0"

import sys

from ansible.errors import AnsibleError, AnsibleFilterError
from ansible.module_utils._text import to_native, to_text
from ansible.module_utils.six import string_types
from ansible.utils.display import Display

try:
    from genie.conf.base import Device, Testbed
    from genie.libs.parser.utils import get_parser
    HAS_GENIE = True
except ImportError:
    HAS_GENIE = False

try:
    from pyats.datastructures import AttrDict
    HAS_PYATS = True
except ImportError:
    HAS_PYATS = False


display = Display()


def parse_genie(cli_output, command=None, os=None):
    """
    Uses the Cisco pyATS/Genie library to parse cli output into structured data.
    :param cli_output: (String) CLI output from Cisco device
    :param command: (String) CLI command that was used to generate the cli_output
    :param os: (String) Operating system of the device for which cli_output was obtained.
    :return: Dict object conforming to the defined genie parser schema.
             https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/parsers/show%20version
    """

    # Does the user have the necessary packages installed in order to use this filter?
    if not HAS_GENIE:
        raise AnsibleFilterError("parse_genie: Genie package is not installed. To install, run 'pip install genie'.")

    if not HAS_PYATS:
        raise AnsibleFilterError("parse_genie: pyATS package is not installed. To install, run 'pip install pyats'.")

    # Does the user have the required version of Python 3.4 that Genie and pyATS requires?
    if sys.version_info[0] == 3 and sys.version_info[1] >= 4:
        pass
    else:
        raise AnsibleFilterError("parse_genie: pyATS/Genie package requires python 3.4 or greater.")

    # Input validation

    # Is the CLI output a string?
    if not isinstance(cli_output, string_types):
        raise AnsibleError(
            "The content provided to the genie_parse filter was not a string."
        )

    # Is the command a string?
    if not isinstance(command, string_types):
        raise AnsibleFilterError(
            "The command provided to the genie_parse filter was not a string."
        )

    # Is the OS a string?
    if not isinstance(os, string_types):
        raise AnsibleFilterError(
            "The network OS provided to the genie_parse filter was not a string."
        )

    # Is the OS provided by the user a supported OS by Genie?
    # Supported Genie OSes: https://github.com/CiscoTestAutomation/genieparser/tree/master/src/genie/libs/parser
    supported_oses = ["ios", "iosxe", "iosxr", "junos", "nxos"]
    if os.lower() not in supported_oses:
        raise AnsibleFilterError(
            "The network OS provided ({0}) to the genie_parse filter is not a supported OS in Genie.".format(
                os
            )
        )

    def _parse(raw_cli_output, cmd, nos):
        # Boilerplate code to get the parser functional
        # tb = Testbed()
        device = Device("new_device", os=nos)

        device.custom.setdefault("abstraction", {})["order"] = ["os"]
        device.cli = AttrDict({"execute": None})

        # User input checking of the command provided. Does the command have a Genie parser?
        try:
            get_parser(cmd, device)
        except Exception as e:
            raise AnsibleFilterError(
                "genie_parse: {0} - Available parsers: {1}".format(
                    to_native(e), "https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/parsers"
                )
            )

        try:
            parsed_output = device.parse(cmd, output=raw_cli_output)
            return parsed_output
        except Exception as e:
            raise AnsibleFilterError(
                "genie_parse: {0} - Failed to parse command output.".format(
                    to_native(e)
                )
            )

    # Try to parse the output
    # If OS is IOS, ansible could have passed in IOS, but the Genie device-type is actually IOS-XE,
    # so we will try to parse both.
    if os == "ios":
        try:
            return _parse(cli_output, command, "ios")
        except Exception:
            return _parse(cli_output, command, "iosxe")
    else:
        return _parse(cli_output, command, os)


class FilterModule(object):
    """ Cisco pyATS/Genie Parser Filter """

    def filters(self):
        return {
            "parse_genie": parse_genie
        }
