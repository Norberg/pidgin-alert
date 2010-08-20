import sys, socket

PORT = 7011
HOST = "sheeva"

def sendLED(argv):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((HOST,PORT))
	except:
		print "sensorDispatcher isnt running, please start it first"
		return
	sep = " "
	output = sep.join(argv)
	s.send(output)
	s.close()

def main():
	sendLED(sys.argv[1:])

if __name__ == "__main__":
	main()
