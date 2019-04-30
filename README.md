# Parse Genie

The network genie filter takes unstructured network CLI command output from all
Cisco Systems network operating systems, and outputs structured data. While similar to other
network CLI parsers already available (parse_cli, parse_cli_textfsm), this parser is
powered by a very mature and robust library written by Cisco Systems called Genie (and underlying framework pyATS).
This provides over 500 parsers that transform configuration and CLI
output to structured data that is normalized and conforms to standard, OS-agnostic data models.

The Genie library can also serve as an engine to parse tabular and non-tabular free-form text
    using much less code than traditional parsing requires. Therefore, it can be used to
    parse any vendor output; not just that of Cisco devices. However, that would involve writing custom parsers.
    This release does not include the functionality to utilize custom parsers. The supported parsers are whatever
    is included in the release of Genie that the user has installed on the Ansible control machine.

To convert the output of a network device CLI command, use the ``parse_genie`` filter as shown in this example
(do not use abbreviated CLI commands).

Converting CLI output of the ``show version`` command from a Cisco IOS-XE device to structured data::

    {{ cli_output | parse_genie(command='show version', os='iosxe') }}

The above example would yield the following:

    {
        "version": {
            "chassis": "CSR1000V",
            "chassis_sn": "9TKUWGKX5MO",
            "curr_config_register": "0x2102",
            "disks": {
                "bootflash:.": {
                    "disk_size": "7774207",
                    "type_of_disk": "virtual hard disk"
                },
                "webui:.": {
                    "disk_size": "0",
                    "type_of_disk": "WebUI ODM Files"
                }
            },
            "hostname": "host-172-16-1-96",
            "image_id": "X86_64_LINUX_IOSD-UNIVERSALK9-M",
            "image_type": "production image",
            "last_reload_reason": "Reload Command",
            "license_level": "ax",
            "license_type": "Default. No valid license found.",
            "main_mem": "1126522",
            "mem_size": {
                "non-volatile configuration": "32768",
                "physical": "3018840"
            },
            "next_reload_license_level": "ax",
            "number_of_intfs": {
                "Gigabit Ethernet": "2"
            },
            "os": "IOS-XE",
            "platform": "Virtual XE",
            "processor_type": "VXE",
            "rom": "IOS-XE ROMMON",
            "rtr_type": "CSR1000V",
            "system_image": "bootflash:packages.conf",
            "uptime": "2 minutes",
            "uptime_this_cp": "3 minutes",
            "version": "16.5.1b,",
            "version_short": "16.5"
        }
    }


The list of supported operating systems and commands, as well
as the data's schema definitions (data models) which describe exactly what fields and
data types will be returned for any given command, is available from Cisco Systems at the link below.

https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/parsers

