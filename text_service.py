import argparse
import sys
import socket
import os
import json

max_byte=65500

class server:
	def __init__(self,interface,port):
		self.interface=interface
		self.port=port

	def modify_json(self,file_text,file_json):
		js_load=json.loads(file_json)
		new_file=file_text
		key_list=js_load.keys()
		for i in key_list:
			new_file=new_file.replace(i,js_load[i])

		return new_file

	def to_encode(self,text,key):
		encoded=""
		while len(key)<len(text):
			key+=key

		for i in range(len(text)):
			a=text[i]
			b=key[i]
			encoded+=chr(ord(a)^ord(b))

		return encoded
		


	def start(self):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		sock.bind((self.interface,self.port))
		sock.listen(5)
		print("Listening at ",sock.getsockname())
		while True:
			sc,sockname=sock.accept()
			print("We hace accepted a connection from {}".format(sockname))
			print("socket name:",sc.getsockname())
			print("socket peer:",sc.getpeername())
			mode,file1,file2=sc.recv(65500).decode().split("!")
			print("Incoming mode:{}".format(mode))
			if mode=="change_text":
				new_file=self.modify_json(file1,file2)
				sc.sendall(new_file.encode("ascii"))
			if mode=="encode_text":
				print("Incoming text:{}".format(file1))
				new_file=self.to_encode(file1,file2)
				sc.sendall(new_file.encode("ascii"))
			sc.close()
			print("Socket closed")


class client:
	
	def __init__(self,mode,host,port):
		self.host=host
		self.port=port
		self.mode=mode
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.connect((self.host,self.port))
		

	def first(self,file1,file2):

		x=open(file1,"r")
		x_con=x.read()
		x_name=x.name.split(".txt")[0]
		x.close()

		l_json=open(file2,"r")
		l_json_con=l_json.read()
		l_json.close()

		#send files
		self.sock.sendall(str.encode("!".join([self.mode,x_con,l_json_con])))

		modified_file=self.sock.recv(65500)
		print("Modified file: {}".format(modified_file.decode()))

	def second(self,text,key):
		x=open(text,"r")
		x_con=x.read()
		x.close()

		l=open(key)
		l_con=l.read()
		l.close()
		#sending text and key
		self.sock.sendall(str.encode("!".join([self.mode,x_con,l_con])))
		#receiving encoded text
		encoded=self.sock.recv(65500)
		print("Encoded file:{}".format(encoded.decode()))


if __name__=="__main__":
	choices={'client':client,'server':server}
	parser=argparse.ArgumentParser()
	parser.add_argument('role',choices=choices)
	parser.add_argument('host')
	parser.add_argument('-p',type=int,default=1060)
	if sys.argv[1]== "client":
		parser.add_argument('mode')
		parser.add_argument("first_file")
		parser.add_argument("second_file")
	args=parser.parse_args()
	func=choices[args.role]
	if func==client:
		cln=func(args.mode,args.host,args.p)
		if args.mode=="change_text":
			cln.first(args.first_file,args.second_file)
		elif args.mode=="encode_text":
			cln.second(args.first_file,args.second_file)
	if func==server:
		func(args.host,args.p).start()





