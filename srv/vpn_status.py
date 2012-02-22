from subprocess import getoutput
from sys import argv, exit

def main():
	if len(argv) != 2:
		exit("Usage: ./vpn_status.py <conName>")
	
	toolOutput = getoutput("nm-tool")
	lines = toolOutput.split("\n")
	conName = argv[1]
	searchString = "VPN:  [" + conName + "]"

	checkStatus = False
	for line in lines:
		if checkStatus == True:
			status = line.rsplit()
			if len(status) >= 2:  
				print(status[1])
				break
		elif searchString in line:
			checkStatus = True

if __name__ == '__main__':
	main()
