import xmlrpclib
import sys
import pprint

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]
CHANNEL = sys.argv[3]
RPM_NAME = sys.argv[4]

pp = pprint.PrettyPrinter(indent=4)

SATELLITE_FQDN = 'rhn.redhat.com'
SATELLITE_URL = 'https://' + SATELLITE_FQDN + '/rpc/api'

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(USERNAME, PASSWORD)

print 'Generating package list...'
channel_packages = client.channel.software.listAllPackages(key, CHANNEL)
for pkg in channel_packages:
	if pkg['package_name'] == RPM_NAME:
		print 'name: ' + pkg['package_name']
		print 'id: ' + str(pkg['package_id'])
		print 'changelog:'
		changelog = client.packages.listChangelog(key, pkg['package_id'])
		pp.pprint(changelog)
