#!/usr/bin/env python

import configparser, os
from sys import argv

# filter for .ovpn-files
def filterType(f):
	return f.endswith(".ovpn")

# updates the openvpn settings in the vpn configuration if needed
def updateOpenvpn(config, path):
	# get the correct .ovpn settings file
	ovpnPath = os.path.expanduser(path)
	filelist = os.listdir(ovpnPath)
	filelist = filter(lambda x: not os.path.isdir(x), filelist)
	filelist = filter(filterType, filelist)
	
	s = config.get('vpn', 'remote')
	server = ''.join([letter for letter in s if not letter.isdigit()]) # remove digits from server adress
	searchString = "remote " + server + " 1149"
	
	for file in filelist:
		for line in open(ovpnPath + "/" + file):
			if searchString in line:
				print(line + " found in " + file)
	
	# get the settings from the .ovpn file
	
	# write settings to the vpn configuration
	return
	

def main():
	# error cases
	nArgs = len(argv)
	if nArgs not in (4,5):
		print("Error, wrong arguments! Use pptool.py instead.")
		return
	if os.getuid() != 0:
		print("Error: This function needs root permissions!")
		return

	fileName = str(argv[1])
	newServer = str(argv[2])
	conType = str(argv[3])
	if conType == "openvpn":
		ovpnPath = str(argv[4])

	vpnconf = configparser.RawConfigParser()
	vpnconf.read(fileName)
	
	# get vpn type
	serverString = "gateway"
	sType = vpnconf.get("vpn", "service-type")
	if sType.endswith(".openvpn") and conType == "openvpn":
		serverString = "remote"
		print("Updating with openvpn VPN connection")
	elif not (sType.endswith(".pptp") and conType == "pptp"):
		print("Error: Invalid VPN-Type! (" + sType + ", tool-setting: " + conType + ") Please use pptp or openvpn.")
		return
	else:
		print("\nUpdating pptp VPN connection...")
	
	# get old server
	oldServer = vpnconf.get("vpn", serverString)

	if oldServer != newServer:
		# Set new server
		print("Changing PP server from " + oldServer + " to " + newServer)
		vpnconf.set("vpn", serverString, newServer)
		
		if conType == "openvpn":
			updateOpenvpn(vpnconf, ovpnPath)
		
		with open(fileName, 'w') as configfile:
			vpnconf.write(configfile)
		print("New Server written to configuration.\n")
		return
	else:
		print("Server didn't change - nothing to do.")
		return

if __name__ == '__main__':
        main()
