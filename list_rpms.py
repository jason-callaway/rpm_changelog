#!/usr/bin/env python
"""
Example script that uses the Satellite XMLRPC API to fetch the list of rpms
from a particular channel in RHN.
To run:
$ python list_rpms.py RHNusername RHNpassword channelName
"""

import xmlrpclib
import sys
import pprint

__author__ = 'Jason Callaway'
__email__ = 'jcallaway@redhat.com'
__license__ = 'GPL'
__version__ = '0.1'

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
CHANNEL = sys.argv[3]

pp = pprint.PrettyPrinter(indent=4)

SATELLITE_FQDN = 'rhn.redhat.com'
SATELLITE_URL = 'https://' + SATELLITE_FQDN + '/rpc/api'

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(USERNAME, PASSWORD)

channel_packages = client.channel.software.listAllPackages(key, CHANNEL)
for pkg in channel_packages:
	print pkg['package_name'].strip() + '-' + pkg['package_version'] + '-' + pkg['package_release']
