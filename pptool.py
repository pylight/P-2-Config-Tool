#!/usr/bin/env python

	#############################################################################
	#																			#
	#			P^2 Config Tool for NetworkManager (Gnome)						#
	#		little helper to switch between Perfect Privacy Servers easily!		#	
	#	more infos? please visit https://github.com/pylight/P-2-Config-Tool		#
	#																			#
	#############################################################################

version = "v0.21"
desc = "Little config tool for Perfect Privacy / Gnome Network Manager to change the VPN servers quickly! :)"

import os, sys, configparser, webbrowser
from gi.repository import Gtk
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
		self.infolabel = self.builder.get_object('menuitem3')
		self.serverlist = self.builder.get_object('serverlist')

		# set up tray icon
		self.tray = Gtk.StatusIcon()
		self.tray.set_visible(False)
		self.tray.set_from_stock(Gtk.STOCK_NETWORK)
		self.tray.connect("activate", self.toogle_visible)
		
		print("Little PP Config Tool " + version + " started!")
		self.getservers()
	
		self.window.show_all()
		self.tray.set_visible(True)

	# get the list of avaliable pp-servers from github
	def getservers(self):
		self.currentServer = self.getCurrentServer()
		cIndex = i = 0		# pos. of the server in the serverlist
	
		f = open("./srv/servers.list", 'r')
		servers = f.readlines()
		for url in servers:
			i += 1
			server = url.rstrip()
			self.serverlist.append_text(server)
			if server == self.currentServer:
				cIndex = i
					
		self.serverlist.set_active(cIndex)
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


	""" Menu Items """
	# disconnects the vpn connection if established
	def stop_vpn(self, menuitem):
		print("Disconnecting VPN...")
		pStop = Popen("nmcli con down id " + mainconfig.get('General', 'connection'), shell=True)
		pStop.wait()
		self.infolabel.set_label("VPN Offline")

	# "Edit File"-Menuentrys
	def sysconfig_open(self, menuitem):
		self.open_editor(mainconfig.get('General', 'path'), True)

	def toolconfig_open(self, menuitem):
		self.open_editor(confpath)

	# Open File with editor and check for changes afterwards
	def open_editor(self, filepath, root=False):
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
		self.check_changes(filepath)

	# check for file changes
	def check_changes(self, file):
		watcher = os.stat(file)
		this_modified = watcher.st_mtime
		
		# if modified, restart tool to get new settings
		if this_modified > self.last_modified:
			print("File edited - restarting!")
			python = sys.executable
			os.execl(python, python, * sys.argv)

	# open the server status-website with the default browser
	def open_infopage(self, menuitem):
		webbrowser.open("https://www.perfect-privacy.com/members/server.html", new=0)
		
	# show about dialog
	def about_clicked(self, window):
		self.about_dialog = Gtk.AboutDialog()
		self.about_dialog.set_title("About")
		self.about_dialog.set_program_name("PP VPN Config Tool")
		self.about_dialog.set_version(version)
		self.about_dialog.set_comments(desc)
		#self.about_dialog.set_logo_icon("gui/pptool.ico")
		self.about_dialog.set_website("https://github.com/pylight/P-2-Config-Tool")
		self.about_dialog.connect("response", self.about_close)
		self.about_dialog.show_all()

	# close the about dialog
	def about_close(self, about_dialog, resid):
		self.about_dialog.destroy()

	
	""" Buttons - Server connection (Apply) and Close """
	
	# Apply / (Re)Connect VPN
	def connect_vpn(self, button):
		self.stop_vpn(self)
		print("Connecting to VPN...")
		pCon = Popen("nmcli con up id " + mainconfig.get('General', 'connection'), shell=True)
		stat = pCon.wait()
		if stat == 0:
			serverInfo = self.currentServer.partition('.')[0]
			self.infolabel.set_label("Connected to " + serverInfo)
		else:
			self.infolabel.set_label("Error: Couldn't connect to server!")
		
	# update PP gateway server
	def set_new_server(self, combobox):
		newserver = self.serverlist.get_active_text()
		if combobox.get_active() != 0 and newserver != self.currentServer:		
			vpnType = mainconfig.get('General', 'type')
			setServerCmd = "srv/set_server.py "+ mainconfig.get('General', 'path') + " " + newserver + " " + vpnType
			if vpnType == "openvpn":
				setServerCmd = setServerCmd + " " +  mainconfig.get('Openvpn', 'certfolder')
			Popen("gksu " + sys.executable + " " + setServerCmd, shell=True)
			self.currentServer = newserver

	# tray-icon-clcked: toogle window visibility
	def toogle_visible(self, trayicon):
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
