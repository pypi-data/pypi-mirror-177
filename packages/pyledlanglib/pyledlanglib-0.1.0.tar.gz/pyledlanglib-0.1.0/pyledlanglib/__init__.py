# This an open source convert an python code into an bin firmware to sd card.
import sys
import os
import platform
import time
class Compiler:
	# welcome banner
	step=20 
	verison="v0.01"
	debug=True
	time_run=0
	def __init__(self):
		print("Welcome the compiler tool. ")
		print("=============> In progress <============")
		self.output_file=open(sys.argv[1],"wb")
		self.output_file_path=sys.argv[1]
		print(f"Output file:{sys.argv[1]}")
		if(sys.argv[2]=="False"):
			self.debug=False
		print("You are running PyLEDLangLib on top of Python 3")
		print(f"Python verison: {sys.version} PyLEDLangLib version: {self.verison} Platform: {platform.platform()}")
		print(f"Debug: {self.debug}")
		self.time_run=time.time()

	pass
	# time in milliseconds
	def sleep(self,time:int):
		int_values=(int(time / self.step)) # convert to loop amount if need
		if(self.debug):
			self.output_file.write(bytes(f';user defined delay block via sleep method: {time} cycles\n','UTF-8')) # write to file
		for a in range(0,int_values):
			self.output_file.write(bytes(f'slp:0{a} -> sleep\n','UTF-8')) # write to file
	pass

	def final_build(self):
		print("=============> Build is successful <==============")
		print(f"Taken: {(time.time()-self.time_run)} seconds")
		print(f"Copy your {self.output_file_path} to SD and insert to controller")
		print("")


	def add_extra_byte(self,input_hex:str):
		"""
		Simple function that adds zero if only one byte is returned
		Check an len of input str and using string format add an zeros
		or return orignal value.
		"""
		if(len(input_hex) < 2):
			return f"0{input_hex}"
		else:
			return input_hex
	pass
	def set_color(self,r:int,g:int,b:int):
		"""
		converts an rgb to bin format.
		So at first get value from user then convert it to hex and remove 0x 
		prefix. Then convert it to upper case.
		using an add_extra_byte add an extra zero if needed. so it converts an
		an 0 => 00 then using string format make final string an save it to bin output.
		"""
		if(self.debug):
			self.output_file.write(bytes(f';user defined color from hex {r} {g} {b}\n','UTF-8')) # write to file
		red=str(hex(int(r))).replace("0x","").upper()
		green=str(hex(int(g))).replace("0x","").upper()
		blue=str(hex(int(b))).replace("0x","").upper()
		red=self.add_extra_byte(red)
		green=self.add_extra_byte(green)
		blue=self.add_extra_byte(blue)
		output_string=f"reg clr:{red}{green}{blue}\n"
		self.output_file.write(bytes(output_string,'UTF-8'))
	pass
	def set_hex_color(self,hex:str):
		if(self.debug):
			self.output_file.write(bytes(f';user defined color from hex {hex} \n','UTF-8')) # write to file
		output_string=f"reg clr:{hex.upper()}\n"
		self.output_file.write(bytes(output_string,'UTF-8'))
	pass

	def freeze(self):
		self.output_file.write(bytes("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF\n",'UTF-8'))
	pass


		

		

		



