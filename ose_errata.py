import xmlrpclib
import sys

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

SATELLITE_FQDN = 'rhn.redhat.com'
SATELLITE_URL = 'https://' + SATELLITE_FQDN + '/rpc/api'

client = xmlrpclib.Server(SATELLITE_URL, verbose=0)
key = client.auth.login(USERNAME, PASSWORD)

#channel_list = []
#channel_list.append('rhel-x86_64-server-6-ose-1.2-rhc')
#channel_list.append('rhel-x86_64-server-6-ose-1.2-rhc-debuginfo')
#channel_list.append('rhel-x86_64-server-6-ose-1.2-infrastructure')
#channel_list.append('rhel-x86_64-server-6-ose-1.2-infrastructure-debuginfo')
#channel_list.append('rhel-x86_64-server-6-ose-1.2-jbosseap')
#channel_list.append('rhel-x86_64-server-6-ose-1.2-jbosseap-debuginfo')
#channel_list.append('rhel-x86_64-server-6-ose-1.2-node')
#channel_list.append('rhel-x86_64-server-6-ose-1.2-node-debuginfo')
#channel_list.append('rhel-x86_64-server-6-ose-2.0-rhc')
#channel_list.append('rhel-x86_64-server-6-ose-2.0-rhc-debuginfo')
#channel_list.append('rhel-x86_64-server-6-ose-2.0-infrastructure')
#channel_list.append('rhel-x86_64-server-6-ose-2.0-infrastructure-debuginfo')
#channel_list.append('rhel-x86_64-server-6-ose-2.0-jbosseap')
#channel_list.append('rhel-x86_64-server-6-ose-2.0-jbosseap-debuginfo')
#channel_list.append('rhel-x86_64-server-6-ose-2.0-node')
#channel_list.append('rhel-x86_64-server-6-ose-2.0-node-debuginfo')
#channel_list.append('rhel-x86_64-server-6-osop-1-rhc')
#channel_list.append('rhel-x86_64-server-6-osop-1-rhc-debuginfo')
#channel_list.append('rhel-x86_64-server-6-osop-1-infrastructure')
#channel_list.append('rhel-x86_64-server-6-osop-1-infrastructure-debuginfo')
#channel_list.append('rhel-x86_64-server-6-osop-1-jbosseap')
#channel_list.append('rhel-x86_64-server-6-osop-1-jbosseap-debuginfo')
#channel_list.append('rhel-x86_64-server-6-osop-1-node')
#channel_list.append('rhel-x86_64-server-6-osop-1-node-debuginfo')

channels = client.channel.listSoftwareChannels(key)
channel_list = []
for c in channels:
	if 'ose' in c['channel_label'] and not 'beta' in c['channel_label'] and not 'debug' in c['channel_label']:
		channel_list.append(c['channel_label'])
	if 'osop' in c['channel_label'] and not 'beta' in c['channel_label'] and not 'debug' in c['channel_label']:
		channel_list.append(c['channel_label'])

advisory_count = 0
rhsa_count = 0
cve_count = 0
output_list = []
for channel in channel_list:
	for e in client.channel.software.listErrata(key, channel, '1970-01-01'):
		advisory_count = advisory_count + 1
		if 'RHSA' in e['errata_advisory']:
			rhsa_count = rhsa_count + 1
		cve_list = client.errata.listCves(key, e['errata_advisory'])
		cve_count = cve_count + len(cve_list)
		output_list.append('"' + channel + '","' + e['errata_advisory'] + '","' + e['errata_issue_date'] + '","' + e['errata_synopsis'] + '","' + '","'.join(cve_list) + '"')
print '"total advisories","' + str(advisory_count) + '"'
print '"security advisories","' + str(rhsa_count) + '"'
print '"CVEs addressed","' + str(cve_count) + '"'
print '\n'.join(output_list)
