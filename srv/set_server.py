#!/usr/bin/env python

import configparser, os
from sys import argv, exit

# filter for .ovpn-files
def filterType(f):
	return f.endswith(".ovpn")

# updates the openvpn settings in the vpn configuration if needed
def updateOpenvpn(config, path):
	
	# get the correct .ovpn settings file
	ovpnPath = os.path.expanduser(path)
	filelist = os.listdir(ovpnPath)
	#filelist = filter(lambda x: not os.path.isdir(x), filelist)
	filelist = filter(filterType, filelist)
	s = config.get('vpn', 'remote')
	server = ''.join([letter for letter in s if not letter.isdigit()]) # remove digits from server adress
	searchString = "remote " + server + " "
	resFile = ""
	port = 0
	for file in filelist:
		for line in open(ovpnPath + "/" + file):
			if line.startswith(searchString):
				resFile = file
				port = int(line.split(" ")[-1])
				break
	
	# check if search was successful
	if resFile == "":
		exit("Error - no .ovpn File found to change the openvpn settings!")		
	else:
		print("Using " + resFile + " to update the openvpn settings...") 
	
	# get the settings from the .ovpn file
	# get .cert, .ca, .key & .ta-filenames
	getCa = getCert  = getKey = getTa = ""
	
	for line in open(ovpnPath + "/" + resFile):
		if line.startswith("ca "):
			getCa = line.split(" ")[1]
		elif line.startswith("cert "):
			getCert = line.split(" ")[1]
		elif line.startswith("key "):
			getKey = line.split(" ")[1]
		elif line.startswith("tls-auth "):
			getTa = line.split(" ")[1]
	
	# dirty litte bugfix: montreal.ovpn, moscow.ovpn and chicaco.ovpn
	# only have a pkcs12-setting => guess the filenames from getTag sting
	if getCa == "" and getCert == "" and getKey == "":
		if getTa != "":
			serverPre = getTa[:2]
			getCa = serverPre + "ca.crt"
			getCert = serverPre + "client.crt"
			getKey = serverPre + "client.key"
		else:
			exit("Error reading settings from " + resFile + " config file.")
	
	# other settings
	config.set('vpn', 'cert', ovpnPath + "/" + getCert)
	config.set('vpn', 'ca', ovpnPath + "/" + getCa)
	config.set('vpn', 'key', ovpnPath + "/" + getKey)
	config.set('vpn', 'ta', ovpnPath + "/" + getTa)
	config.set('vpn', 'port', port)
	return config
	

def main():
	# error cases
	nArgs = len(argv)
	if nArgs not in (4,5):
		exit("Error, wrong arguments! Use pptool.py instead.")

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
		exit("Error: Invalid VPN-Type! (" + sType + ", tool-setting: " + conType + ") Please use pptp or openvpn.")
		
	else:
		print("\nUpdating pptp VPN connection...")
	
	# get old server
	oldServer = vpnconf.get("vpn", serverString)

	if oldServer != newServer:
		# Set new server
		print("Changing PP server from " + oldServer + " to " + newServer)
		vpnconf.set("vpn", serverString, newServer)
		
		if conType == "openvpn":
			vpnconf = updateOpenvpn(vpnconf, ovpnPath)
		
		with open(fileName, 'w') as configfile:
			vpnconf.write(configfile)
		print("New Server written to configuration.\n")
		return
	else:
		print("Server didn't change - nothing to do.")
		return

if __name__ == '__main__':
        main()
