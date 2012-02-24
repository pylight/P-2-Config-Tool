import socket, urllib.error
from re import search
from urllib.request import urlopen

# return the current PP server ip the user is connected to
def getActiveServer():
	data = str(urlopen('http://checkip.dyndns.org').read())
	m = search('([0-9]*)(\.)([0-9]*)(\.)([0-9]*)(\.)([0-9]*)', data)
	currentIP = m.group(0)
	
	if currentIP == "180.153.108.198":
		serverName = "shanghai.perfect-privacy.com"
	else:
		serverName = socket.gethostbyaddr(currentIP)[0]
	
	if serverName.endswith(".dsl.il-dialup.net") and currentIP.startswith("2"):
		serverName = "chicago.perfect-privacy.com"
	elif serverName.endswith(".dip.tx-dialin.net") and currentIP.startswith("204.45."):
		serverName = "denver.perfect-privacy.com" 
	return serverName


def main():
	try:
		print(getActiveServer())
	except:
		pass

if __name__ == '__main__':
	main()
