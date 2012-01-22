#!/usr/bin/env python
# Filename: initConfig.py

import configparser, os
from dialogs import errorDialog, infoDialog, questionDialog, choiceDialog
from sys import exit

# default config settings
defaultID = "PP"
defaultPath = "/etc/NetworkManager/system-connections/"
defaultEditor = "gedit"
defaultFile = "~/.ppvpntool.conf"

# checks if the default path exists and else asks for another path 
def checkPath(path, conID):
	if(os.path.exists(path)):
			print("Using " + path + " as vpn config path.")
			infoDialog("This Tool will look for your VPN Connection settings at " + path + ". If you need to change this, use the Tool Menu. (Connection -> Tool Settings)")
	else:
		print("Error: File not found at " + path)
		nmPath = questionDialog("No file found at " + path + "\nPlease specify the NetworkManager path for VPN-Connection-Settings on your system.", defaultPath)
		path = nmPath + conID
		if not os.path.exists(path):
			errorDialog("Error: no VPN configfile found at " + path + ". Please make sure you entered the right values and created the PP VPN connection in NetworkManager and rerun this tool!")
			exit("Error: Setup failed (invalid VPN config file)")
	return path


# ask the user for the settings
def setID():
	return questionDialog("Please input the name (ID) of your VPN Connection", defaultID)
	
def setEditor():
	return questionDialog("Please input your prefered (graphical) Editor:", defaultEditor)		

def setvpnType():
	return choiceDialog("Please choose the type of your VPN connection", ["pptp", "openvpn"])

def setPath():
	path = questionDialog("Invalid setting: please specify the NetworkManager path for VPN-Connection-Settings on your system.", defaultPath)
	if not os.path.exists(path):
			errorDialog("Error: the path " + path + " doesn't exist. Please make sure you entered the right values, check the tool configuration (" + defaultFile + ") and rerun this tool!")
			exit("Error: Setup failed (invalid VPN config path)")
	print("Using " + path + " as NM path.")
	return path

def setOvpnFolder():
	path = questionDialog("You choose openvpn as connection type. PP Config Tool will use the openvpn configuration files from the PP member downloads. Please get that package (https://www.perfect-privacy.com/members/All.ovpn.ubuntu.zip), extract it and input the path of that folder below:", os.path.expanduser("~/Downloads/All.ovpn.ubuntu"))
	if not os.path.exists(path):
			errorDialog("Error: the path " + path + " doesn't exist. Please make sure you entered the right values, check the tool configuration (" + defaultFile + ") and rerun this tool!")
			exit("Error: Setup failed (invalid VPN config path)")
	return path

# validate the config file
def checkConfig(config, path):	
	config.read(path)
	eCount = 0

	try:
		config.get('General', 'connection')
	except configparser.NoOptionError as ex:
		print("Error: (broken config)\n" + str(ex))
		eCount = eCount + 1
		config.set('General', 'connection', setID())

	try:		
		config.get('General', 'path')
	except configparser.NoOptionError as ex:
		print("Error: (broken config)\n" + str(ex))
		eCount = eCount + 1
		config.set('General', 'path', setPath())

	try:
		config.get('General', 'editor')
	except configparser.NoOptionError as ex:
		print("Error: (broken config)\n" + str(ex))
		eCount = eCount + 1
		config.set('General', 'editor', setEditor())

	try:
		config.get('General', 'type')
	except configparser.NoOptionError as ex:
		print("Error: (broken config)\n" + str(ex))
		eCount = eCount + 1
		config.set('General', 'type', setvpnType())

	if config.get('General', 'type') == "openvpn":
		try:
			config.get('Openvpn', 'certfolder')
		except configparser.NoSectionError:
			config.add_section('Openvpn')
			config.set('Openvpn', 'certfolder', setOvpnFolder())
		except configparser.NoOptionError:
			config.set('Openvpn', 'certfolder', setOvpnFolder())


	if eCount > 0:
		print("Rewriting config file.")
		with open(path, 'w') as configfile:
			config.write(configfile)
	else:
		print("Configuration read without errors.")
	
	
# running whenever the tool starts
def initConfig():
	# try to read tool configuration
	mainconfig = configparser.RawConfigParser()
	confpath = os.path.expanduser(defaultFile)

	if (os.path.exists(confpath) == False):
		print("\nConfigfile", confpath, "not found. Running Config Setup...")
		infoDialog("The configuration was not found at " + defaultFile + ". Starting Setup-Process...")
		
		conID = setID()

		path = defaultPath + conID
		
		# validate vpn config path and set editor
		path = checkPath(path, conID)
		vpntype = setvpnType()
		editor = setEditor()

		# write config file
		mainconfig.add_section('General')
		mainconfig.set('General', 'path', path)
		mainconfig.set('General', 'connection', conID)
		mainconfig.set('General', 'type', vpntype)
		mainconfig.set('General', 'editor', editor)

		if mainconfig.get('General', 'type') == "openvpn":
			mainconfig.add_section('Openvpn')
			mainconfig.set('Openvpn', 'certfolder', setOvpnFolder())

		with open(confpath, 'w') as configfile:
			mainconfig.write(configfile)

		infoDialog("The configuration was written to \n" + confpath)
	
	print("Reading configuration...")
	checkConfig(mainconfig, confpath)

	return mainconfig

