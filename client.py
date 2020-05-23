import os
import sys
import socket as s
import hashlib
import pickle
import shutil
from datetime import datetime
import time
from pathlib import Path

host_name = 'localhost'
port_number = 5050
UDP_PORT = 5051
cache_folder = './CacheFolder'
cache_size = 1000000

try:
	os.mkdir(cache_folder)
except:
	pass

def name_split(cmnd, i):
	cmnd = cmnd.split(" ")
	return cmnd[i]


def soc(cmnd):
	s1 = s.socket(s.AF_INET, s.SOCK_STREAM)
	s1.connect((host_name, port_number))
	s1.sendall(pickle.dumps(cmnd))

	return s1

def convert_date(timestamp):
	d = datetime.fromtimestamp(timestamp)
	formated_date = d.strftime('%d-%b-%Y %H:%M')
	return formated_date

def GetSize_Cache():
	entries = os.scandir(cache_folder)
	size = 0
	for entry in entries:
		size = size + os.path.getsize('./CacheFolder/'+entry.name)
	return size

def deleteCache(size):
	print("Cache limit reached!!! Cache size = ", size)
	list_of_files = os.listdir(cache_folder)
	for i in range(len(list_of_files)):
		list_of_files[i] = './CacheFolder/' + list_of_files[i]

	oldest_file = min(list_of_files, key=os.path.getctime)
	os.remove(os.path.abspath(oldest_file))
	print("Oldest file Deleted")
	return

def quit(cmnd):

	s1 = soc(cmnd)
	s1.close()
	return


def IndexGet(cmnd, extension_flag):
	s1 = soc(cmnd)
	command = name_split(cmnd,1)
	s1.sendall(pickle.dumps(cmnd)) 
	try:
		
		t1=s1.recv(4096)
		mid = pickle.loads(t1)
		bon_arr_extn = []


		if command == 'shortlist':
			if(len(cmnd.split(" ")) == 7):
				extn = name_split(cmnd,6)


			if(extension_flag == 0):
				for i in range(len(mid[1])):
					print(mid[1][i])

			else:
				extension_flag = 0 
				for i in range(len(mid[0])):
					bon_arr_extn.append(os.path.splitext(mid[0][i]))

				for i in range(len(mid[1])):
					if(extn == bon_arr_extn[i][1]):
						print(mid[1][i])

		elif (command =='longlist'):

			if(len(cmnd.split(" ")) == 3):
				extn = name_split(cmnd,2)
			
			if(extension_flag == 0):
				
				for i in range(len(mid[0])):
					print(mid[0][i])

			else:
				try:
					extension_flag = 0

					for i in range(len(mid[1])):
						bon_arr_extn.append(os.path.splitext(mid[1][i]))

					for i in range(0,len(mid[1])):
						if(extn == bon_arr_extn[i][1]):
							print(mid[0][i])

				except:
					print("No such files found.")
		s1.close()
	except:
		print("Invalid command!")
	return

def extensionIndexget(cmnd):
	extension_flag = 1
	IndexGet(cmnd,extension_flag)
	return

def download(cmnd):
	s1 = soc(cmnd)
	file_name = name_split(cmnd,1)
	try:
		data = s1.recv(4096)
		if not data:
			s1.close()
			return
		with open(file_name, "wb") as file_receive:
			while True:
				file_receive.write((data))
				data = s1.recv(4096)
				if not data:
					break

		file_receive.close()
		print(os.popen("ls -ogh --time-style=long-iso " + file_name).read())
		FileHash("FileHash verify " + file_name)
	except:
		print("Not found!")
	s1.close()
	return

def download_udp(cmnd):
	file_name = name_split(cmnd,1)
	udp_s=s.socket(s.AF_INET, s.SOCK_DGRAM)
	udp_s.bind((host_name, UDP_PORT))
	udp_s.settimeout(2)
	s1 = soc(cmnd)
	s1.close()

	try:
		data = udp_s.recv(4096)
		if not data:
			udp_s.close()
			return
		with open(file_name, "wb") as file_receive:
			while True:
				file_receive.write((data))
				data = udp_s.recv(4096)
				if not data:
					break
		file_receive.close()	
	except:
		pass
	print( os.popen("ls -ogh --time-style=long-iso " + file_name).read())
	FileHash("FileHash verify " + file_name)
	udp_s.close()    
	return


def FileHash(cmnd):
	raw1 = name_split(cmnd,1)
	test = cmnd.split()
	if test[1] == 'verify' and len(test)<3:
		return
	s1 = soc(cmnd)
	try:
		if raw1 == "verify":
			raw2 = name_split(cmnd,2)
			hashServer=pickle.loads(s1.recv(4096))
			print(("Hash Value (Server) = ", hashServer))
			try:
				hashClient = hashlib.md5(open(raw2,'rb').read()).hexdigest()
				print(("Hash Value (Client) = ", hashClient))
				print(os.popen("ls -ogh --time-style=long-iso " + raw2).read())
			except:
				print("The file is not on the system")
				print()
			
		elif raw1 == 'checkall':
			f = s1.recv(4096)
			f1 = pickle.loads(f)
			for key, value in f1.items():
				print( "Filename = ", key)
				print( "Server side Hash Value = ", value)
				try:
					hashClient = hashlib.md5(open(key,'rb').read()).hexdigest()
					print( "Client side Hash Value = ", hashClient)
					print(os.popen("ls -ogh --time-style=long-iso " + key).read())
				except:
					print("The file is not on this system.")
					print()
	except:
		print('File Not found!')
	s1.close()
	return

 
def CacheData(cmnd):
	command = name_split(cmnd,1)
	entries = os.scandir(cache_folder)

	if command == "show":
		for entry in entries:
			if entry.is_file():
				info = entry.stat();
				modi = convert_date(info.st_mtime)
				size = os.path.getsize('./CacheFolder/'+entry.name)
				print('{0}\t Last Modified: {1}\t Size: {2}'.format(entry.name,modi,size))
		print('Cache Size = ',GetSize_Cache())


	elif command == "verify":
		flag = 0
		file_name = name_split(cmnd,2)
		# entries = os.scandir(cache_folder)
		for entry in entries:
			if file_name == entry.name:
				print("{0} already in Cache Folder".format(entry.name))
				info = entry.stat()
				atime = info.st_atime
				currtime = time.time()
				os.utime(cache_folder+'/'+entry.name,(atime,currtime))
				flag = 1

		if flag==0:
			cmnd = "FileDownload " + file_name + " TCP"
			print(cmnd)
			s1 = soc(cmnd)
			data = s1.recv(4096)
			if not data:
				flag = -1

			else:
				with open(file_name, "wb") as file_receive:
					file_receive.write((data))
					while True:
						data = s1.recv(4096)
						if not data:
							break
						file_receive.write((data))

				file_receive.close()
				size_file_receive = os.path.getsize(file_name)
				print(size_file_receive)
				if size_file_receive > cache_size:
					os.remove(os.path.abspath(file_name))
					print("File too large for Cache! Did not store the file.")

				else:
					shutil.move('./'+file_name,'./CacheFolder')
					print("File stored in Cache")
				
				size = GetSize_Cache()
				while size > cache_size:
					deleteCache(size)
					size = GetSize_Cache()
			  
			s1.close()
		if flag==-1:
			print("!! File Not Found !!")
	return


history = ""
while 1:
	sys.stdout.write ("$$ ")
	sys.stdout.flush()
	inp = sys.stdin.readline().strip()
	history = history + (inp +"\n")
	bon = inp.split(" ")
	extension_flag = 0
	
	if (inp == 'q' or inp == 'Q'):
		quit(inp)
		break

	elif (len(bon) == 7 and bon[0] == "IndexGet") or (len(bon) == 3 and bon[0] == "IndexGet"):
			extensionIndexget(inp)
	else:
		command = name_split(inp,0)
		if command == 'FileDownload':
			try:
				if(name_split(inp,2) == 'TCP'):
					download(inp)
				else:
					download_udp(inp)
			except:
				pass
		elif command =='IndexGet':
			IndexGet(inp,extension_flag)
		elif command == 'FileHash':
			FileHash(inp)
		elif command == 'Cache':
			CacheData(inp)
