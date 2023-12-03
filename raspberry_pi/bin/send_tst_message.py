from common import *
import sys


if len(sys.argv) > 1:
	send_to_mq(sys.argv[1])
else:

	print("Enter a message to send to MQ bus")
	x = input()
	send_to_mq(x)



