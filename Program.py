import sys
import telnetlib
import psutil
import signal
import binascii
import regex as re
import OogaAPI as oob
from termcolor import colored
from time import sleep
from os import path

# Config
tn_host = "127.0.0.1"
tn_port = "2121"
cfg_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\cfg\\"
user = "Bizon Man" # Your CSGO Username to avoid infinite looping (just the base name, no clan or anything else)

def signal_handler(signal, frame):
	print("\nquitting...")
	sys.exit(0)

# List PIDs of processes matching processName
def processExists(processName):
	procList = []
	for proc in psutil.process_iter(['name']):
		if proc.info['name'].lower() == processName.lower():
			return True
	return False

# Runs commands on the CS:GO console
def run(txn, command):
	cmd_s = command + "\n"
	txn.write(cmd_s.encode('utf-8'))
	sleep(0.005)

signal.signal(signal.SIGINT, signal_handler)

def main():
	if (len(sys.argv) > 1):
		if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
			print(colored("Run with no arguments to initiate and connect to csgo", attrs=['bold']))
			print(colored("Make sure you set up csgo to receive connections with this launch option: -netconport "+str(tn_port), attrs=['bold']))
	
	# Make sure CS:GO is running before trying to connect
	if not processExists("csgo.exe"):
		print("Waiting for csgo to start... ")
		while not processExists("csgo.exe"):
			sleep(0.25)
		sleep(10)

	# Initialises CS:GO telnet connection
	print("Trying to connect to " + tn_host + ":" + tn_port)
	try:
		tn = telnetlib.Telnet(tn_host, tn_port)
	except ConnectionRefusedError:
		sleep(30)
		pass
	try:
		tn = telnetlib.Telnet(tn_host, tn_port)
	except ConnectionRefusedError:
		print("Connection refused. Don't forget to add   -netconport " + str(tn_port) + "to launch options.")
		sys.exit(1)
	print("Successfully Connected")

	print("Listening for messages...")
	while True:
		try:
			result = tn.expect([b"\r\n"])
			last_line = result[2].decode("utf-8").splitlines()
			last_line = last_line[len(last_line) - 1]
			# Special characters used to determine what and where chat messages start and end.
			if "‎" in last_line and "​" not in last_line:
				whole_line = last_line
				last_line = last_line.split("‎")

				# Parses the name
				sender = str(last_line[0])
				sender = sender.replace("(Counter-Terrorist) ", "")
				sender = sender.replace("(Terrorist) ", "")
				sender = sender.replace("*DEAD* ", "")
				sender = sender.replace("*DEAD*", "")
				sender = sender.replace("*SPEC* ", "")
				sender = sender.replace("(Spectator) ", "")

				message = str(last_line[1])
				message = re.sub(r'^.*? : ', '', message)
				message = re.sub(r"^\s+", "", message)

				print(sender + " : " + message)
				if sender == user:
					if message[:3] == 'prompt:':
						message = message[6:]
						response = oob.getResponse(message)
						run(tn, "say " + response)
						print("AI : " + response)
					else:
						print(sender + " : " + message)
						pass
				else:
					print(sender + " : " + message)
					response = oob.getResponse(message)
					run(tn, "say " + response)
					print("AI : " + response)
		except Exception as e:
			print("Something went wrong. Make your -netconport " + str(tn_port) + "is added to launch options.")
			print('Error:' + e)
			sys.exit(1)


if __name__== "__main__":
  main()
