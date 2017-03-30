#!/usr/bin/python  
  
import socket  
import sys  
import re  
 

# Establish socket connection
def connect(host, port):  
	s = None  
	for res in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM):  
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
  
# If the weight is incorrect, then the counterfeit coin is in the current half
# Otherwise, it is in the other half 
def weight(current_index, coin_weight, other_index):  
	if coin_weight != (current_index[1] - current_index[0]) * 10:  
		return current_index  
	else:  
		return (current_index[1], other_index[1])  


# Format the index range to string  
def getNumbers(i_range):  
	string_list = []  
	for i in range(i_range[0], i_range[1]):  
		string_list.append(str(i))  
	return ' '.join(string_list)  


def main(): 
	# Uploaded script to server and ran local for more speed
	host = 'localhost'   
	#host = 'pwnable.kr'   

	# Port used by server
	port = 9007   
	s = connect(host, port)  
	if s is None:  
		print "[!] Unable to open socket"
		sys.exit(1)  

	# The range to be weighed  
	index = None
	# The range that contains the counterfeit coin 
	second_range = None 
	  
	while True:  
		data = s.recv(1024)  
		print str(data)  
	  
		pattern1 = re.compile("""^N=([0-9]*) C=([0-9]*)$""")  
		match1 = pattern1.match(str(data))  
	  
		pattern2 = re.compile("""^([0-9]*)$""")  
		match2 = pattern2.match(str(data))  
	  
		# First round  
		if match1:  
			first_range = (0, int(match1.group(1)) / 2)  
			second_range = (0, int(match1.group(1)))  
			print str(getNumbers(first_range))  
			s.send(getNumbers(first_range) + "\r\n")  

		# Second round  
		elif match2 and len(match2.group(1)) > 0:  
			second_range = weight(index, int(match2.group(1)), second_range)
			# Get the ceiling value when divided by 2  
			index = (second_range[0], (second_range[0] + second_range[1]) / 2 + (second_range[0] + second_range[1]) % 2)  
			print str(getNumbers(index))  
			s.send(getNumbers(index) + "\r\n")  

		elif "format error" in str(data) or "time expired! bye!" in str(data):  
			break  
	  
	s.close()

main()
