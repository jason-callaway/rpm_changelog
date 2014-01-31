#!/usr/bin/env python
"""
Example that uses the Satellite XMLRPC API to fetch the list of errata from
an RHN software channel.

To run:
$ python get_errata.py RHNusername RHNpassword channel
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

errata = client.channel.software.listErrata(key, CHANNEL, '1970-01-01')
pp.pprint(errata)
