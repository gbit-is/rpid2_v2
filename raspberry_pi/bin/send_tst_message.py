from common import *
import sys



#send_to_mq(sys.argv[1])
print("Enter a message to send to MQ bus")
x = input()
send_to_mq(x)



