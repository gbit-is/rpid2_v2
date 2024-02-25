from flask import Flask,request,render_template
from common import *
import serial
from common import init_common_config
import time
config = init_common_config()



config = init_common_config()
kvs = init_kvs() # initalise KVS, make sure the KVS is populated 

def init_uart():

	serial_port = config.get("dome_controller","serial_port_read")
	serial_baud = config.getint("dome_controller","serial_baud")
	try:
		uart = serial.Serial (serial_port, serial_baud)
		return uart,True
	except Exception as e:
		print(e)
		return None, False


def manage_uart(uart,option):

	serial_port = config.get("dome_controller","serial_port_read")
	serial_baud = config.getint("dome_controller","serial_baud")
	
	if option == "connect":
		uart, response = init_uart()
		return uart, response

	elif option == "read":
		size = uart.in_waiting
		data = uart.read(size).decode().split("\n")
		
		for line in reversed(data):
			if line.startswith("pos:"):
				rotation = line.split(":")[1].split(".")[0]
				rotation = int(rotation)
				print(rotation)
				return uart, rotation
		




def validateKvsValue(key,value):

	if key in config["kvs_variables"]:
		valueType = config["kvs_variables"][key]
			
		if valueType == "bool":
			if value in [ "True","False" ]:
				return True
			else:
				return False


		elif valueType == "num":
			try:
				value = float(value)
				return True
			except:
				return False
			
	else:
		return True


app = Flask(__name__)


app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def hello_world():

	kvs = init_kvs() 

	audioLoopEnabled = kvs["audio_loop_enabled"].decode()
	audio_loop_interval_low = kvs["audio_loop_interval_low"].decode()
	audio_loop_interval_high = kvs["audio_loop_interval_high"].decode()

	if audioLoopEnabled == "True":
		audioChecked_var = "checked"
	else:
		audioChecked_var = ""

	return render_template('index.html', audioChecked=audioChecked_var,audioLowInterval_value=audio_loop_interval_low,audioHighInterval_value=audio_loop_interval_high)



@app.route("/config/<parameter>", methods = ['POST','GET'])
def manageConfig(parameter):
	kvs = init_kvs()

	keys = [ ]	
	for key in kvs.keys():
		keys.append(key.decode())

	if parameter not in keys:
		return "parameter not in KVS",404


	if request.method == 'POST':
		data = request.data.decode()
		if len(data) == 0:
			return "body recieved is empty",400
		else:
			
			valid = validateKvsValue(parameter,data)
			
			if valid:

				try:
					kvs[parameter] = data
					return "ack", 200
				except Exception as e:
					return e, 500
			else:
				return "unable to validate k:v pair", 418
		
		
	elif request.method == 'GET':
		data = kvs[parameter].decode()
		return data



 


 
if __name__ == '__main__':

	c = 0
	l = 5

	uart, foo = manage_uart(None,"connect")
	while c < l:
		manage_uart(uart,"read")
		c += 1
		time.sleep(2)
		
	
 
	#app.run(host="0.0.0.0")
	pass


