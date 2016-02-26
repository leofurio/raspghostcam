import RPi.GPIO as GPIO
Import time
import subprocess

PIN_BUTTON = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_BUTTON, GPIOIN, pull_up_down=GPIO.PUD_UP)
set = 0
while True:
    input_state = GPIO.input(PIN_BUTTON)
    if input_state == False and set == 0:
        p=subprocess.Popen( "/home/pi/ghostcamera.sh",shell=True,preexec_fn=os.setsid) 
        time.sleep(1)
        set =1
    input_state = GPIO.input(PIN_BUTTON)
    if input_state == False and set == 1:
        os.killpg(p.pid, signal.SIGTERM)
        time.sleep(1)
        set =0
