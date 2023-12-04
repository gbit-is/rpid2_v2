### rpid2_v2
The [original](https://github.com/gbit-is/rpid2) RPI-D2 project was a bit of a mess, starting from scratch

### Somewhat almost ready features

- Use any* usb gamepad controller for main motors and dome
- handles audio, manual audio triggers and automatic generation **
- web interface for controlling various parameters **
- Drop-in dome positioning system (no modifications needed to the mrbaddeley V3 body) ***
- automatic dome homing ****
- automatic dome roaming ****



\* okay, not any controller, I have tried 4 and 3 worked (I think the forth one was simply broken though)   
\** Existing in version 1, plan on at least partially rewriting it for version 2    
\*** Still a work in progress, proof of concept has been created but needs some polishing before publishing  
\**** Not started on this part 

### Next steps

I have started work on creating a CAN bus system to communicate between the raspberry pi and other controllers, the idea is that the raspberry pi communicates directly to the motor control with a direct and dedicated UART connection but that all other communications happen via a CAN bus/MQ system. The upside to this is:

CAN:
- Reduced wiring to dome, only power and 2 CAN bus wires will be needed for the dome
- simple wiring from the raspberry pi to any number of secondary controllers
- simple to add any centrally controlled lights, servos. etc

MQ: (beanstalkd)
- Using a lightweight MQ system enables the system to aqquire data from multiple sources and push it to the CAN bus easily
- .... although this might be overkill and cause lag, that will have to be determined once I get a prototype ready


### Further goals
This project started as a way to use various gamepads to control a R2D2 and to generate audio

Since then it also became a dome positioning system and I have started protoyping dome lights as well, who knows where this will end up going 

## Parts list:

Main control:
- Gamepad: Any-ish gamepad with a USB reciever
- Raspberry pi: I am using a raspberry pi 3B without issue

Motor control:
- Any PWM motor controller should work, I am using 2X cytron md30c (chosen for price and avaivability)
- Raspberry Pi Pico (or any other board capable of running circuitpython, has usb_cdc support and at least 4 digital pins)

Dome control:
- Raspberry Pi Pico (I would not recomend using other boards for this, the libraries used here can be more of a hazzle)
- logic level shifter with at least 3 channels
- Hall effect sensor ( I am using the LJ18A3-8-Z/BX )
- Large rotary encoder ( I am using the 38S6G5-B-G24N ( 50 step version) which gives me a resolution of roughly 0.4°)
