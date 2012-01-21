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

	fileName = str(sys.argv[1])
	newServer = str(sys.argv[2])

	vpnconf = configparser.RawConfigParser()
	vpnconf.read(fileName)
	
	# get vpn type
	serverString = "gateway"
	sType = vpnconf.get("vpn", "service-type")
	if sType.endswith(".openvpn"):
		serverString = "remote"
	elif not sType.endswith(".pptp"):
		print("Warning: Unsupported VPN-Type! (" + sType + ") Please use pptp or openvpn.")
	
	# get old server
	oldServer = vpnconf.get("vpn", serverString)

	if oldServer != newServer:
		# Set new server
		print("Changing PP server from " + oldServer + " to " + newServer)
		vpnconf.set("vpn", serverString, newServer)
		
		with open(fileName, 'w') as configfile:
			vpnconf.write(configfile)
		print("New Server written to configuration.")
	else:
		sys.exit()

if __name__ == '__main__':
        main()
