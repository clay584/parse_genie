# Parse Genie

[![Published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/clay584/parse_genie)

![Ansible Role](https://img.shields.io/ansible/role/40061.svg?color=orange&label=ansible%20role&style=popout)
![Ansible Version](https://img.shields.io/badge/ansible-%3E%3D2.7-blue.svg)
![Python Version](https://img.shields.io/badge/python-%3E%3D3.4-blue.svg)

[![Build Status](https://travis-ci.org/clay584/parse_genie.svg?branch=master)](https://travis-ci.org/clay584/parse_genie)
![Ansible Quality Score](https://img.shields.io/ansible/quality/40061.svg?label=code%20quality&style=popout)


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

The list of supported operating systems and commands, as well
as the data's schema definitions (data models) which describe exactly what fields and
data types will be returned for any given command, is available from Cisco Systems at the link below.

https://pubhub.devnetcloud.com/media/pyats-packages/docs/genie/genie_libs/#/parsers

## Prerequisites

This plugin will require the following:

1. Python 3.4+
2. pyATS and Genie packages
3. Ansible 2.7+ (It should work on older versions as long as the other requirements are satisfied)

## Installation

Please follow these instructions to ensure that the filter plugin will function with your playbooks:

1. Create a directory for your playbook and go into it. `mkdir network_ops && cd network_ops`
2. Create a virtual environment. `python3 -m venv .venv`
3. Activate the virtual environment. `source .venv/bin/activate`
4. Install Ansible. `pip install ansible`
5. Install Genie and pyATS. `pip install genie`
6. Install the parse_genie role from Ansible Galaxy. `ansible-galaxy install clay584.parse_genie`

## Ansible to Genie OS Mappings

Below are the mappings from Ansible's `ansible_network_os` to Genie's `os`:

| Ansible Network OS  | Genie OS      |
| ------------------- | ------------- |
| ios                 | ios, iosxe    |
| nxos                | nxos          |
| iosxr               | iosxr         |
| junos               | junos         |

If you are working with IOS or IOS-XE there is ambiguity in that Ansible considers IOS and IOS-XE
the same and therefore the `ansible_network_os = ios`, but Genie needs to know specifically if it is
IOS or IOS-XE in order to parse the CLI output correctly. If you pass `ansible_network_os` to this filter plugin,
and it is equal to `ios`, parse_genie will try to parse it with Genie using `os=ios` first, and if that fails, it will
then try to parse it with `os=iosxe`.

So keep that in mind when creating your playbooks. It may be best to pass the real OS to the parse_genie.
You can do that by keeping another inventory variable or host_var to specify the Genie OS for each network device
and using that variable as the OS for the parse_genie.

### Usage

Make sure to read in the parse_genie role before you attempt to use it later in your playbook.

    ...trunctated...
    
	  tasks:
	  - name: Read in parse_genie role
		include_role:
		  name: clay584.parse_genie
		  
    ...trunctated...


### Short Example
To convert the output of a network device CLI command, use the `parse_genie` filter as shown in this example
(do not use abbreviated CLI commands).

Converting CLI output of the `show version` command from a Cisco IOS-XE device to structured data::

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

### Full Example #1

Playbook:

	---
	
	- hosts: localhost
	  connection: local
	  vars:
		show_version_output: |
		  Cisco IOS XE Software, Version 16.05.01b
		  Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.5.1b, RELEASE SOFTWARE (fc1)
		  Technical Support: http://www.cisco.com/techsupport
		  Copyright (c) 1986-2017 by Cisco Systems, Inc.
		  Compiled Tue 11-Apr-17 16:41 by mcpre
	
	
		  Cisco IOS-XE software, Copyright (c) 2005-2017 by cisco Systems, Inc.
		  All rights reserved.  Certain components of Cisco IOS-XE software are
		  licensed under the GNU General Public License ("GPL") Version 2.0.  The
		  software code licensed under GPL Version 2.0 is free software that comes
		  with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
		  GPL code under the terms of GPL Version 2.0.  For more details, see the
		  documentation or "License Notice" file accompanying the IOS-XE software,
		  or the applicable URL provided on the flyer accompanying the IOS-XE
		  software.
	
	
		  ROM: IOS-XE ROMMON
	
		  host-172-16-1-96 uptime is 2 minutes
		  Uptime for this control processor is 3 minutes
		  System returned to ROM by reload
		  System image file is "bootflash:packages.conf"
		  Last reload reason: Reload Command
	
	
	
		  This product contains cryptographic features and is subject to United
		  States and local country laws governing import, export, transfer and
		  use. Delivery of Cisco cryptographic products does not imply
		  third-party authority to import, export, distribute or use encryption.
		  Importers, exporters, distributors and users are responsible for
		  compliance with U.S. and local country laws. By using this product you
		  agree to comply with applicable laws and regulations. If you are unable
		  to comply with U.S. and local laws, return this product immediately.
	
		  A summary of U.S. laws governing Cisco cryptographic products may be found at:
		  http://www.cisco.com/wwl/export/crypto/tool/stqrg.html
	
		  If you require further assistance please contact us by sending email to
		  export@cisco.com.
	
		  License Level: ax
		  License Type: Default. No valid license found.
		  Next reload license Level: ax
	
		  cisco CSR1000V (VXE) processor (revision VXE) with 1126522K/3075K bytes of memory.
		  Processor board ID 9TKUWGKX5MO
		  2 Gigabit Ethernet interfaces
		  32768K bytes of non-volatile configuration memory.
		  3018840K bytes of physical memory.
		  7774207K bytes of virtual hard disk at bootflash:.
		  0K bytes of WebUI ODM Files at webui:.
	
		  Configuration register is 0x2102
	
	  tasks:
	  - name: Read in parse_genie role
		include_role:
		  name: clay584.parse_genie
	
	  - name: Debug Genie Filter
		debug:
		  msg: "{{ show_version_output | parse_genie(command='show version', os='iosxe') }}"
		delegate_to: localhost


Output:

	$ ansible-playbook -i inventory debug.yml
	
	PLAY [localhost] *************************************************************************
	
	TASK [Gathering Facts] *******************************************************************
	ok: [localhost]
	
	TASK [Read in parse_genie role] **********************************************************
	
	TASK [Debug Genie Filter] ****************************************************************
	ok: [localhost -> localhost] => {
		"msg": {
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
	}


### Full Example #2

Playbook:

	---
	
	- hosts: csr1000v
	  gather_facts: False
	  tasks:
	  - name: Read in parse_genie role
		include_role:
		  name: clay584.parse_genie
	
	  - name: Get Data From Device
		ios_command:
		  commands: show arp vrf Mgmt-intf
		register: arp_output
	
	  - name: Print Structured Data
		debug:
		  msg: "{{ arp_output['stdout'][0] | parse_genie(command='show arp vrf Mgmt-intf', os='iosxe') }}"
		delegate_to: localhost

Output:

	$ ansible-playbook -i inventory playbook.yml
	
	PLAY [csr1000v] **************************************************************************
	
	TASK [Read in parse_genie role] **********************************************************
	
	TASK [Get Data From Device] **************************************************************
	ok: [csr1000v]
	
	TASK [Print Structured Data] *************************************************************
	ok: [csr1000v -> localhost] => {
		"msg": {
			"interfaces": {
				"GigabitEthernet1": {
					"ipv4": {
						"neighbors": {
							"172.16.1.111": {
								"age": "0",
								"ip": "172.16.1.111",
								"link_layer_address": "5e00.4004.0000",
								"origin": "dynamic",
								"protocol": "Internet",
								"type": "ARPA"
							},
							"172.16.1.114": {
								"age": "-",
								"ip": "172.16.1.114",
								"link_layer_address": "5e00.4001.0000",
								"origin": "static",
								"protocol": "Internet",
								"type": "ARPA"
							}
						}
					}
				}
			}
		}
	}

## Development

Set up your development environment:

1. Clone the repo and go into it. `git clone https://github.com/clay584/parse_genie.git && cd parse_genie`
2. Create a virtual environment. `python3 -m venv .venv`
3. Activate the virtual environment. `source .venv/bin/activate`
4. Install Ansible. `pip install ansible`
5. Install Genie and pyATS. `pip install genie`
6. Install yamllint. `pip install yamllint`

### Testing

Run these commands to test locally:

1. Lint all of the YAML files. `yamllint -c yamllint_config.yml *`
2. Run the test playbook. `ansible-playbook tests/test.yml --connection=local -i tests/inventory`

### Pushing

Ansible Galaxy works on tags.

1. `git commit -m"whatever'`
2. `git tag -a X.X.X` - where X.X.X is a symantec versioning number.
3. `git push origin master`
4. `git push X.X.X`
