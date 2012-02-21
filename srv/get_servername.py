import socket, urllib.error
from re import search
from urllib.request import urlopen

# return the current PP server ip the user is connected to
def getActiveServer():
	data = str(urlopen('http://checkip.dyndns.org').read())
	m = search('([0-9]*)(\.)([0-9]*)(\.)([0-9]*)(\.)([0-9]*)', data)
	currentIP = m.group(0)
	serverName = socket.gethostbyaddr(currentIP)[0]
	return serverName

def main():
	try:
		print(getActiveServer())
	except:
		pass

if __name__ == '__main__':
	main()
