#!/usr/bin/env python

def main():
	import configparser
	import sys, os

	# error cases
	if len(sys.argv) != 3:
		print("Error, wrong arguments! Use pptool.py instead.")
		sys.exit()
	if os.getuid() != 0:
		print("Error: This function needs root permissions!")
		sys.exit()

	filename = str(sys.argv[1])
	newserver = str(sys.argv[2])

	vpnconf = configparser.RawConfigParser()
	vpnconf.read(filename)
	gateway = vpnconf.get("vpn", "gateway")

	if gateway != newserver:
		# Set new server
		print("Changing PP server from " + gateway + " to " + newserver)
		vpnconf.set("vpn", "gateway", newserver)
		
		with open(filename, 'w') as configfile:
			vpnconf.write(configfile)
		print("New Server written to configuration.")
	else:
		sys.exit()

if __name__ == '__main__':
        main()
