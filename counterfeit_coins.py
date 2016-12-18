#!/usr/bin/python  
  
import socket  
import sys  
import re  
  
# Establish socket connection  - IP version agnostic
def connect(HOST, PORT):  
	s = None  
	for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):  
		af, socktype, proto, canonname, sa = res  
		try:  
			s = socket.socket(af, socktype, proto)  
		except socket.error, msg:  
			s = None  
			continue  
		try:  
			s.connect(sa)  
		except socket.error, msg:  
			s.close()  
			s = None  
			continue  
			break  
	return s  
  
# If the weight is correct, then the counterfeit coint is in the other half
# Otherwise, it is in the current half 
def weight(cIndex, cWeight, lIndex):  
	if cWeight != (cIndex[1] - cIndex[0]) * 10:  
		return cIndex  
	else:  
		return (cIndex[1], lIndex[1])  
  
# Format the index range to string  
def getNumbers(index):  
	strList = []  
	for i in range(index[0], index[1]):  
		strList.append(str(i))  
	return ' '.join(strList)  
  
# The remote host  
# Uploaded script to server and ran local for more speed
HOST = 'localhost'   
#HOST = 'pwnable.kr'   

# Port used by server
PORT = 9007   
s = connect(HOST, PORT)  
if s is None:  
	print '[!] Unable to open socket'  
	sys.exit(1)  

# The range to be weighted  
index = None
# The range that contains the counterfeit coin 
lastIndex = None 
  
while True:  
	data = s.recv(1024)  
	print str(data)  
  
	pattern1 = re.compile("""^N=([0-9]*) C=([0-9]*)$""")  
	match1 = pattern1.match(str(data))  
  
	pattern2 = re.compile("""^([0-9]*)$""")  
	match2 = pattern2.match(str(data))  
  
	# First round  
	if match1:  
		index = (0, int(match1.group(1)) / 2)  
		lastIndex = (0, int(match1.group(1)))  
		print str(getNumbers(index))  
		s.send(getNumbers(index) + "\r\n")  
	# Second round  
	elif match2 and len(match2.group(1)) > 0:  
		lastIndex = weight(index, int(match2.group(1)), lastIndex)
		# Get the ceiling value when divided by 2  
		index = (lastIndex[0], (lastIndex[0] + lastIndex[1]) / 2 + (lastIndex[0] + lastIndex[1]) % 2)  
		print str(getNumbers(index))  
		s.send(getNumbers(index) + "\r\n")  
	elif "format error" in str(data) or "time expired! bye!" in str(data):  
		break  
  
s.close()

