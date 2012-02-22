#!/usr/bin/env python

	#############################################################################
	#																			#
	#			P^2 Config Tool for NetworkManager (Gnome)						#
	#		little helper to switch between Perfect Privacy Servers easily!		#	
	#	more infos? please visit https://github.com/pylight/P-2-Config-Tool		#
	#																			#
	#############################################################################

version = "v0.314159265"
desc = "Little config tool for Perfect Privacy / Gnome Network Manager to change the VPN servers quickly! :)"

import os, sys, configparser, webbrowser
from gi.repository import Gtk, GObject
from urllib.request import urlopen 
from subprocess import Popen, getoutput

# own modules
from initConfig import initConfig

UI_FILE = "gui/window.ui"


class VPNTool:
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		# get objects
		self.window = self.builder.get_object('window')
		self.infolabel = self.builder.get_object('labelinfo')
		self.statuslabel = self.builder.get_object('labelonoff')
		self.serverBox = self.builder.get_object('serverlist')
		print("Little PP Config Tool " + version + " started!")
		self.getServers()

		# set up tray icon
		self.tray = Gtk.StatusIcon()
		self.tray.set_visible(False)
		self.tray.set_from_file("./gui/trayicon.svg")
		self.tray.connect("activate", self.iconToogleVisibility)
		
		self.checkCounter = 0;	
		self.checkVPN()
		GObject.timeout_add(3500, self.checkVPN)	# check vpn status every 3.5 seconds
		
		
		self.window.show_all()
		self.tray.set_visible(True)

	# get the list of avaliable pp-servers from github
	def getServers(self):
		self.currentServer = self.getCurrentServer()
		cIndex = i = 0		# pos. of the server in the serverlist
	
		f = open("./srv/servers.list", 'r')
		servers = f.readlines()
		for url in servers:
			server = url.rstrip()
			# remove comments
			if '#' in server:
				if server.startswith('#'):
					continue
				else:
					server = server.split('#', 1)[0]
			i += 1
			self.serverBox.append_text(server)
			if server == self.currentServer:
				cIndex = i
					
		self.serverBox.set_active(cIndex)
		f.close()

	# gets the current server url from nmcli and returns it if possible
	def getCurrentServer(self):
		out = getoutput("nmcli con list id " + mainconfig.get('General', 'connection'))
		outlist = out.splitlines()
		for i in range(0, len(outlist)):
			if outlist[i].startswith("vpn.data: "):
				vpnData = outlist[i].replace(' ', '').split(',')
				for n in range(0, len(vpnData)):
					if vpnData[n].startswith("gateway="):	# pptp
						return vpnData[n][8:]
					if vpnData[n].startswith("remote="):	# openvpn
						return vpnData[n][7:]
				break
		return ""

	# return the current PP server ip the user is connected to
	def getActiveServer(self):
		data = str(urlopen('http://checkip.dyndns.org').read())
		m = search('([0-9]*)(\.)([0-9]*)(\.)([0-9]*)(\.)([0-9]*)', data)
		currentIP = m.group(0)
		serverName = socket.gethostbyaddr(currentIP)[0]
		return serverName

	# checks frequently if the connection is active
	# updates the trayicon and the "connection status"-label
	def checkVPN(self):
		activeVPN = False
			
		# check if vpn connection is active
		python = sys.executable
		vpnStatus = getoutput(python + " ./srv/vpn_status.py " + mainconfig.get('General', 'connection'))

		if vpnStatus == "connected":
			if self.checkCounter == 1:
				return True

			# get the server name
			activeServer = getoutput(python + " ./srv/get_servername.py")
								
			# connected
			if activeServer != "" and activeServer.endswith('.perfect-privacy.com'):
				connectionInfo = activeServer.split('.')[0]
				self.infolabel.set_label(connectionInfo)
				self.statuslabel.set_label(' <span color="darkgreen">online</span> ')
				self.tray.set_from_file("./gui/trayicon2.svg")
				self.checkCounter = 1
			return True
		
		# connecting
		elif vpnStatus == "connecting":
			self.statuslabel.set_label('<span color="orange">connecting</span>')
			self.infolabel.set_label("-")
			self.checkCounter = 0
			return True

		# (re)connect button was clicked
		if hasattr(self, 'nextConnect') and self.nextConnect:
			self.doConnect()
			self.nextConnect = False
			return True
		
		# inactive connection 
		self.infolabel.set_label("-")
		self.statuslabel.set_label(' <span color="darkred">offline</span> ')
		self.tray.set_from_file("./gui/trayicon.svg")
		self.checkCounter = 0
		return True

	""" Menu Items """
	# disconnects the vpn connection if established
	def stopVPN(self, menuitem):
		print("Disconnecting VPN...")
		self.statuslabel.set_label('<span color="orange">disconnecting</span>')
		self.pStop = Popen("nmcli con down id " + mainconfig.get('General', 'connection'), shell=True)

	# "Edit File"-Menuentrys
	def openSysConfig(self, menuitem):
		self.openEditor(mainconfig.get('General', 'path'), True)

	def openToolConfig(self, menuitem):
		self.openEditor(confpath)

	def openServerlist(self, menuitem):
		self.openEditor("./srv/servers.list")

	# Open File with editor and check for changes afterwards
	def openEditor(self, filepath, root=False):
		# get "last modified" date
		watcher = os.stat(filepath)
		self.last_modified = watcher.st_mtime
		
		# open the file with an editor
		if root == True:
			pEdit = Popen("gksu " + mainconfig.get('General', 'editor') + " " + filepath, shell=True)
		else:
			pEdit = Popen(mainconfig.get('General', 'editor') + " " + filepath, shell=True)
		pEdit.wait()
		
		# was the file changed?
		self.checkChanges(filepath)

	# check for file changes
	def checkChanges(self, file):
		watcher = os.stat(file)
		modificationTime = watcher.st_mtime
		
		# if modified, restart tool to get new settings
		if modificationTime > self.last_modified:
			print("File edited - restarting!")
			python = sys.executable
			os.execl(python, python, * sys.argv)

	# open the server status-website with the default browser
	def openInfopage(self, menuitem):
		label = menuitem.get_label()
		if label == "PP Server Status Page":
			url = "https://www.perfect-privacy.com/members/server.html"
		elif label == "PP CheckIP":
			url = "http://checkip.perfect-privacy.com/"
		elif label == "Extended IP Info":
			url = "http://www.whoer.net/extended"
		else:
			print("Unknown MenuItem: " + label)
			return		
		webbrowser.open(url, new=0)

	# show/hide connection status info
	def toggleStatus(self, menuitem):
		self.infobox = self.builder.get_object('statusbox')
		self.togglelabel = self.builder.get_object('labeltogglestatus')
		
		if self.infobox.get_visible():
			self.infobox.hide()
			self.togglelabel.set_label("Show connection status")
		else:
			self.infobox.show()
			self.togglelabel.set_label("Hide connection status")

	
	# show about dialog
	def aboutClicked(self, window):
		self.about_dialog = Gtk.AboutDialog()
		self.about_dialog.set_title("About")
		self.about_dialog.set_program_name("PP VPN Config Tool")
		self.logo = Gtk.Image()
		self.logo.set_from_file("gui/icon.svg")
		self.logo.set_pixel_size(32)
		aboutBox = self.about_dialog.get_content_area()
		aboutBox.add(self.logo)
		self.about_dialog.set_version(version)
		self.about_dialog.set_comments(desc)
		self.about_dialog.set_website("https://github.com/pylight/P-2-Config-Tool")
		
		self.about_dialog.connect("response", self.aboutClose)
		self.about_dialog.show_all()

	# close the about dialog
	def aboutClose(self, about_dialog, resid):
		self.about_dialog.destroy()

	
	""" Buttons - Server connection (Apply) and Close """
	# Apply / (Re)Connect VPN
	# because we have to wait for the end of the disconnect, the actual doConnect-call will be in 
	# the frequently checkVPN function
	def reconnect(self, button):
		self.stopVPN(self)	# disconnect
		self.nextConnect = True 

	def doConnect(self):
		print("Connecting to VPN...")	
		self.statuslabel.set_label('<span color="orange">connecting</span>')
		self.infolabel.set_label("-")
		self.tray.set_from_file("./gui/trayicon.svg")
		self.pCon = Popen("nmcli con up id " + mainconfig.get('General', 'connection'), shell=True)
	
	# update PP gateway server
	def setNewServer(self, combobox):
		newserver = self.serverBox.get_active_text()
		if combobox.get_active() != 0 and newserver != self.currentServer:		
			vpnType = mainconfig.get('General', 'type')
			setServerCmd = "srv/set_server.py "+ mainconfig.get('General', 'path') + " " + newserver + " " + vpnType
			if vpnType == "openvpn":
				setServerCmd = setServerCmd + " " +  mainconfig.get('Openvpn', 'certfolder')
			Popen("gksu " + sys.executable + " " + setServerCmd, shell=True)
			self.currentServer = newserver

	# tray-icon-clcked: toogle window visibility
	def iconToogleVisibility(self, trayicon):
		if self.window.get_visible():
			self.window.hide()
		else:
			self.window.show()

	# close app
	def destroy(self, window):
		Gtk.main_quit()	

def main():
	# init and read config
	global mainconfig, confpath
	confpath = os.path.expanduser("~/.ppvpntool.conf")
	mainconfig = initConfig()
	
	# start main Gtk app
	app = VPNTool()
	Gtk.main()

if __name__ == '__main__':
	main()
