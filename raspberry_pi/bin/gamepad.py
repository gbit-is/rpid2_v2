import sys
import time
import serial

from common import init_common_config
from common import get_dir_path

config = init_common_config()
lib_dir = get_dir_path("lib_dir")

sys.path.append(lib_dir)



import Gamepad

def initGamepad():

	gamepadType = Gamepad.PS4


	if not Gamepad.available():
        	print('Please connect your gamepad...')
        	while not Gamepad.available():
                	print("waiting for gamepad")
                	time.sleep(1.0)

	gamepad = gamepadType()
	print('Gamepad connected')
	gamepad.startBackgroundUpdates()

	return gamepad

def translate_trigger_value(value):

        value += 1
        value =  value / 2
        return value


def initUART(config_section):
	serial_port = config.get(config_section,"serial_port")
	serial_baud = config.getint(config_section,"serial_baud")

	print("Connecting to mototor controller (UART)")

	uart_not_ready = True

	while uart_not_ready:
		try:
			UART = serial.Serial (serial_port, serial_baud)    #Open port with baud rate
			uart_not_ready = False
			
		except Exception as e:
			print("Unable to connect to motor controller (UART)")
			print("Error is:")
			print(e)
			print("will retry in N seconds")
			time.sleep(2)

	print("Connected to motor controller")
	return UART


	

def manage_gamepad():

	global gamepad
	global axis_conf
	global direction_inverse_multiplier
	global turning_inverse_multiplier


	gamepad = initGamepad()

	axis_conf = {
		"direction"		:	config.getint("controller_map","direction"),
		"direction_invert"	:	config.getboolean("controller_map","direction_invert"),
		"direction_deadzone"	:	config.getfloat("controller_map","direction_deadzone"),
		"turning"		:	config.getint("controller_map","turning"),
		"turning_invert"	:	config.getboolean("controller_map","turning_invert"),
		"turning_deadzone"	:	config.getfloat("controller_map","turning_deadzone"),
		"turning_multiplier"	:	config.getfloat("controller_limits","turning_multiplier"),
		"max_throttle"		:	config.getfloat("motor_limits","max_throttle"),
		"throttle_multiplier"	:	config.getfloat("motor_limits","throttle_multiplier"),
		"dome_right"		:	config.getint("controller_map","dome_right" ),
		"dome_left"		:	config.getint("controller_map","dome_left"),
		"dome_deadzone"		:	config.getfloat("controller_map","dome_deadzone")
	}


	if axis_conf["direction_invert"]:
		direction_inverse_multiplier = -1
	else:
		direction_inverse_multiplier = 1
	if axis_conf["turning_invert"]:
		turning_inverse_multiplier = -1
	else:
		turning_inverse_multiplier = 1
	
	#button_name_data = gamepad.buttonIndex
	#button_names = { }
	#for entry in button_name_data:
		#button_names[button_name_data[entry]] = entry

		

	gamepad.addAxisMovedHandler(axis_conf["direction"],manage_main_motors)
	gamepad.addAxisMovedHandler(axis_conf["turning"],manage_main_motors)

	gamepad.addAxisMovedHandler(axis_conf["dome_left"],manage_dome_motor)
	gamepad.addAxisMovedHandler(axis_conf["dome_right"],manage_dome_motor)

	
def manage_dome_motor(value,index):

	global dome_uart

	axis_data = gamepad.axisMap

	dome_right = translate_trigger_value(axis_data[axis_conf["dome_right"]])
	dome_left = translate_trigger_value(axis_data[axis_conf["dome_left"]])
	dome_total = dome_right - dome_left
	if abs(dome_total) < axis_conf["dome_deadzone"]:
		dome_total = 0

	dome_msg = "drive," + str(dome_total) + "@"

	try:
		dome_uart.write(dome_msg.encode())
	except Exception as e:
		dome_uart = initUART("dome_controller")
		print(e)

	



	
def manage_main_motors(value,index):

	global motor_uart

	axis_data = gamepad.axisMap

	direction = ( axis_data[axis_conf["direction"]] * direction_inverse_multiplier )
	turning = ( axis_data[axis_conf["turning"]] * turning_inverse_multiplier )

	if abs(direction) < axis_conf["direction_deadzone"]:
		direction = 0
	if abs(turning) < axis_conf["turning_deadzone"]:
		turning = 0

	total_motion = abs(direction) + abs(turning)

	if total_motion == 0:
		left_motor, right_motor = 0, 0

	elif turning == 0:
		left_motor = direction
		right_motor = direction
	elif direction == 0:
		left_motor = turning
		right_motor = turning * -1
	else:
		turning_modifier = turning * axis_conf["turning_multiplier"]
		left_motor = direction - turning_modifier
		right_motor = direction + turning_modifier

	left_motor = left_motor * axis_conf["throttle_multiplier"]
	right_motor = right_motor * axis_conf["throttle_multiplier"]

	if left_motor > axis_conf["max_throttle"]:
		left_motor = axis_conf["max_throttle"]
	elif left_motor < ( axis_conf["max_throttle"] * -1 ):
		left_motor = axis_conf["max_throttle"] * -1

	if right_motor > axis_conf["max_throttle"]:
		right_motor = axis_conf["max_throttle"]
	elif right_motor < ( axis_conf["max_throttle"] * -1 ):
		right_motor = axis_conf["max_throttle"] * -1

	msg = "|" + str(left_motor) + "," + str(right_motor) + "@"
	try:
		motor_uart.write(msg.encode())
	except Exception as e:
		motor_uart = initUART("motor_controller")
		print(e)





        
		
if __name__ == "__main__":

	motor_uart = initUART("motor_controller")
	dome_uart = initUART("dome_controller")


	manage_gamepad()
	exit()
	while True:
		try:
			manage_gamepad()
		except Exception as e:
			print(e)
