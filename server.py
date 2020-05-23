import os
import sys
import socket
import hashlib
import pickle
from datetime import datetime, time

host_name = "localhost"
port_number = 5050
UDP_PORT = 5051

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print( "Server Activated...")
except socket.error :
	print( "Unable to create Server!")
	sys.exit()

try:
	s.bind((host_name, port_number))
except socket.error:
	print( 'Server binding failed!!')
	sys.exit()

s.listen(1)
print( "Server listening...")
history = ""


def shortlist(val):
	try:
		sDate = datetime.strptime(val[2]+" "+val[3], '%d-%m-%Y %H:%M:%S')
		eDate = datetime.strptime(val[4]+" "+val[5], '%d-%m-%Y %H:%M:%S')

		strt_ts = datetime.timestamp(sDate)
		end_ts = datetime.timestamp(eDate)

		fileNameArr = os.popen("ls").read().split("\n")[:-1]
		content = os.popen('ls -ogh --time-style=long-iso').read().split("\n")[1:-1]

		timeArr = []
		for i in fileNameArr:
			timeArr.append(os.stat(i).st_mtime)

		snd_name = []
		snd_cntnt = []

		for i in range(len(timeArr)):
			if int(timeArr[i]) > strt_ts and int(timeArr[i]) < end_ts:
				snd_name.append(fileNameArr[i])
				snd_cntnt.append(content[i])

		finl_rslt = [snd_name, snd_cntnt]
		snd.sendall(pickle.dumps(finl_rslt))
	except:
		pass
	return

def longlist():

	ls = os.popen("ls -ogh --time-style=long-iso").read()
	content = ls.split("\n")[1:-1]
	fileNameArr = os.popen("ls").read().split("\n")
	t5 = [content,fileNameArr]
	data_long = pickle.dumps(t5)
	
	snd.sendall(data_long)
	return

def verify(tq1):
	try:
		snd.sendall(pickle.dumps(hashlib.md5(open(tq1,'rb').read()).hexdigest()))
	except:
		print("File not found on the server!")
	return

def checkall():
	addr = os.getcwd()
	file_hash = {}
	for f in os.listdir(addr):
		if os.path.isfile(f):
			file_hash[f] = hashlib.md5(open(f,'rb').read()).hexdigest()
	hash_data = pickle.dumps(file_hash)
	snd.sendall(hash_data)
	return

def FileDownload(cmnd):
	file_name = cmnd.split(" ")
	try:
		with open(file_name[1], 'rb') as file_down:
			for data in file_down:
				snd.sendall((data))
	except:
		print("File not found!")
	return

def FileDownload_udp(cmnd):
	udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dest = (host_name, UDP_PORT)
	file_name = cmnd.split(" ")
	try:
		with open(file_name[1], 'rb') as file_down:
			for data in file_down:
				udp_s.sendto(data,dest)
		
	except:
		print("File not on server!")
	udp_s.close()
	return

while 1:
	
	snd, num = s.accept()
	print( "Got connected from ", num[0], ':', num[1])
	data = pickle.loads(snd.recv(4096))
	history = history + (data + "\n")
	val = data.strip().split(" ")
	if (data == 'Q' or data == 'q'):
		snd.close()
		break

	elif (val[1] == "shortlist"):
		shortlist(val)

	elif (val[1] == "longlist"):
		longlist()

	elif (val[0] == "FileHash"):
		if(val[1] == "verify"):
			verify(val[2])
		elif (val[1] == "checkall"):
			checkall()
	elif(val[0] == "FileDownload"):
		if val[2]=='TCP':
			FileDownload(data)
		else:
			FileDownload_udp(data)
	snd.close()

s.close()