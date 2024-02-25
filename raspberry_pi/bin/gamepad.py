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


	gamepad = initGamepad()

	motor_UART = initUART("motor_controller")
	dome_UART = initUART("dome_controller")

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
	


	x = dir(gamepad)
	for i in x:
		print(i)


	# Rewrite this entire thing, transfer to addAxisMovedHandlers
	# This is a rough mockup
	while True:

		


		axis_data = gamepad.axisMap
		


		direction = ( axis_data[axis_conf["direction"]] * direction_inverse_multiplier )
		turning = ( axis_data[axis_conf["turning"]] * turning_inverse_multiplier )

		dome_right = translate_trigger_value(axis_data[axis_conf["dome_right"]])
		dome_left = translate_trigger_value(axis_data[axis_conf["dome_left"]])
		dome_total = dome_right - dome_left
		if abs(dome_total) < axis_conf["dome_deadzone"]:
			dome_total = 0

		dome_msg = "drive," + str(dome_total) + "@"


		if abs(direction) < axis_conf["direction_deadzone"]:
			direction = 0
		if abs(turning) < axis_conf["turning_deadzone"]:
			turning = 0

		total_motion = abs(direction) + abs(turning)

		if total_motion == 0:
			left_motor = 0
			right_motor = 0

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
			motor_UART.write(msg.encode())
		except Exception as e:
			motor_UART = initUART("motor_controller")
			print(e)

		try:
			dome_UART.write(dome_msg.encode())
		except Exception as e:
			dome_UART = initUART("dome_controller")
			print(e)
				

		time.sleep(0.5)


        
		
if __name__ == "__main__":


	while True:
		try:
			manage_gamepad()
		except Exception as e:
			print(e)
