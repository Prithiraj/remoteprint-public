from subprocess import PIPE, Popen
from app_ver_stable.starmarkupengine.tags import DrawerOpenModes
from app_ver_stable.utilities.validate import Validate
import subprocess
import tempfile
import os
import json
class PrintSupport:
	def __init__(self):
		pass
   
	@classmethod	
	def getCPSupportedOutput(cls, value=None):
		try:
			pipe = Popen('/usr/local/bin/cputil mediatypes-mime "text/vnd.star.markup"', shell=True, stdout=PIPE).stdout
			data = pipe.read()
			pipe.flush()
			pipe.close()
			item = json.loads(data.decode())
			return item
		except Exception as e:
			raise e	
	
	@classmethod
	def renderMarkupJob(cls, filename, printing, queue, design):	
		try:
			with open(filename, 'w+') as f:
				f.write(design.markup)
				f.write("[cut]")
				
		except Exception as e:
			raise e	

	@classmethod
	def getCPConvertedJob(cls, inputFile, outputFormat, deviceWidth, outputFile, ticketDesign):
		cputilpath = "/usr/local/bin/cputil"
		options = ""
		if deviceWidth <= (58 * 8):
			options = options+"thermal2"
		elif deviceWidth <= (72*8):
			options = options + "thermal3"
		elif deviceWidth <= (82*8):
			options = options + "thermal82"
		elif deviceWidth <= (112*8):
			options = options + "thermal4"
		

		drawer_open_at = ticketDesign.drawer_open_at
		buzzers_at_start = ticketDesign.buzzers_at_start
		buzzers_at_end = ticketDesign.buzzers_at_end
  
		drawer_command = f"drawer-{drawer_open_at.lower()}"
		cmd_buzzers_at_start = f"buzzer-start {buzzers_at_start}"
		cmd_buzzers_at_end = f"buzzer-end {buzzers_at_end}"
   
      
		options = options + " scale-to-fit dither " + drawer_command + " " + cmd_buzzers_at_start + " " + cmd_buzzers_at_end
		commandString = cputilpath + " " + options + " decode " + outputFormat+ " " + inputFile + " " + outputFile.name
		result = subprocess.check_output([commandString], shell=True)
		# return commandString
  
		# os.system(commandString)
   