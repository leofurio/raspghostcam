import ftplib
import time
import picamera
import datetime
import Adafruit_DHT
import RPi.GPIO as GPIO


PIN_DHT = 4
DHT_MODEL = 11
GPIO.setmode(GPIO.BCM)
old_hum = 45
old_temp = 21

login='USER'
password='PASSWORD'
ftpurl= 'FTPURL'
folder='FTPFOLDER'

def capture_frame(txt):
    with picamera.PiCamera() as cam:
        time.sleep(2)
        cam.vflip = True
        cam.start_preview()
        cam.annotate_text = str(txt)
        #cam.led = False
        cam.capture('/home/pi/Desktop/imageftp.jpg')


def getDht(model,pin):
	return Adafruit_DHT.read_retry(model,pin)

input_state = GPIO.input(PIN_BUTTON)

while True:
	start = time.time()
	humidity, temperature = getDht(DHT_MODEL,PIN_DHT)
	if temperature != old_temp or humidity != old_hum :
		old_temp = temperature
		old_hum = humidity
		capture_frame('Humidity:'+str(humidity)+'\n Temperature:'+ str(temperature))
		session = ftplib.FTP(ftpurl,login,password)
		file = open('/home/pi/Desktop/imageftp.jpg','rb') # file to send
		today = datetime.datetime.now()
		strToday = today.strftime('%d-%m-%Y-%H-%M-%S')
		session.rename(folder+'imageftp.jpg', folder+'imageftp'+strToday+'.jpg')
		session.storbinary('STOR '+folder+'imageftp.jpg', file)# send the file
		file.close()# close file and FTP
		session.quit()
	time.sleep(0.2)

