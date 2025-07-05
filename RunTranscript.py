import sounddevice as sd
import queue
import sys
import json
import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
import threading
from vosk import Model, KaldiRecognizer
import pyttsx3

#-------------GPIO Setup-------------------
GPIO.setmode(GPIO.BCM)
LED_PIN = 17 #Use GPIO physical pin 11
BUTTON_PIN = 4 #Use GPIO physical pin 7
BUTTON_BRIGHTNESS_UP_PIN = 27 #Use GPIO physical pin 13
BUTTON_BRIGHTNESS_DOWN_PIN = 22 #Use GPIO physical pin 15
BUTTON_HELP_PIN = 23 #Use GPIO physical pin 16
BUZZER = 24 #Use GPIO physical pin 18
AWAKE_PIN = 25 #Use GPIO physical pin 22

GPIO.setup(LED_PIN, GPIO.OUT) #LED Pin
GPIO.setup(AWAKE_PIN, GPIO.OUT) #LED Pin
GPIO.setup(BUZZER, GPIO.OUT) #LED Pin
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Button LED ON/OFF Pin
GPIO.setup(BUTTON_BRIGHTNESS_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Button LED Increase Pin
GPIO.setup(BUTTON_BRIGHTNESS_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Button LED Decrease Pin
GPIO.setup(BUTTON_HELP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Button HELP
GPIO.output(AWAKE_PIN, GPIO.LOW) #Initialise AWAKE LED to 0
pwm = GPIO.PWM(LED_PIN, 1000)
pwm.start(0) #Initialise LED to have no brightness
GPIO.output(BUZZER, GPIO.LOW) #Initialise buzzer to have no noise

#-------------Vosk Model-------------------
model_path = "VoskModels/vosk-model-small-en-us-0.15"
q = queue.Queue()

model = Model(model_path)
rec = KaldiRecognizer(model, 16000)

#-------------------TTS---------------------
tts = pyttsx3.init()
tts.setProperty('rate', 150) #speaking speed
tts.setProperty('volume', 1.0)

#-------------Global Variables Declaration----------
led_on = False #Debounce
led_brightness = 100 #Brightness for pwm 100-0
is_AWAKE = False 

WAKE_WORD = "hey bridge"
COMMAND_TIMEOUT = 10 #Set timeout length before device goes back to sleep

last_command_time = 0 #Variable to measure time



#----------------Constructors---------------
def toggle_led(dummy): #Need dummy variable as GPIO.add_event_detect requires constructor to have at least 1 input.
	global led_on
	global led_brightness
	led_on = not led_on
	if led_on:
		pwm.ChangeDutyCycle(led_brightness)
	else:
		pwm.ChangeDutyCycle(0)
	print("LED is:", "ON" if led_on else "OFF", "-Setting brightness to:", led_brightness if led_on else "0", "%")

def toggle_Is_AWAKE(dummy):
	global is_AWAKE
	is_AWAKE = not is_AWAKE
	if is_AWAKE:
		GPIO.output(AWAKE_PIN, GPIO.HIGH)
	else:
		GPIO.output(AWAKE_PIN, GPIO.LOW)
	print("AWAKE LED is", "ON" if led_on else "OFF")
	
def increase_brightness(dummy):
	global led_brightness
	global led_on
	led_on = True #Set it so there is no debounce when toggling LED after this call
	led_brightness = led_brightness + 20
	if led_brightness >= 100:
		led_brightness = 100
	pwm.ChangeDutyCycle(led_brightness)
	print("Setting Brightness to :", led_brightness, "%")
	
def decrease_brightness(dummy):
	global led_brightness
	global led_on
	led_brightness = led_brightness - 20
	if led_brightness <= 0:
		led_brightness = 0
		led_on = True #Set it so there is no debounce when toggling LED after this call
	pwm.ChangeDutyCycle(led_brightness)
	print("Setting Brightness to :", led_brightness, "%")

def help_ASSIST(dummy):
	print("Calling for Assistance now!")
	GPIO.output(BUZZER, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(BUZZER, GPIO.LOW)
	
#--------Button inputs-------------
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=toggle_led, bouncetime=300)
GPIO.add_event_detect(BUTTON_BRIGHTNESS_UP_PIN, GPIO.RISING, callback=increase_brightness, bouncetime=300)
GPIO.add_event_detect(BUTTON_BRIGHTNESS_DOWN_PIN, GPIO.RISING, callback=decrease_brightness, bouncetime=300)
GPIO.add_event_detect(BUTTON_HELP_PIN, GPIO.RISING, callback=help_ASSIST, bouncetime=300)

#--------------GUI SETUP--------------------
	
def show_help():
	messagebox.showinfo("About", "MEDBridge Device Functions:\n\n"
								"- Toggle LED:\n"
								"- Increase Brightness:\n"
								"- Decrease Brightness:\n"
								"- Call for Help:\n")
	
def run_gui():
	root = tk.Tk()
	root.title("MEDBridge Assistance Device")
	root.geometry("630x400")
	root.configure(bg="black")
	
	def on_close():#Add closing defination here so that seperate thread can run it
		root.destroy()
	
	#--------Toggle Lights Button----------
	toggle_LIGHTS_REF = Image.open("Lights_On-Off.png")
	toggle_LIGHTS_REF = toggle_LIGHTS_REF.resize((64, 64))
	toggle_LIGHTS_ICON = ImageTk.PhotoImage(toggle_LIGHTS_REF)

	increase_LIGHTS_REF = Image.open("Lights_On.png")
	increase_LIGHTS_REF = increase_LIGHTS_REF.resize((64, 64))
	increase_LIGHTS_ICON = ImageTk.PhotoImage(increase_LIGHTS_REF)

	decrease_LIGHTS_REF = Image.open("Lights_Off.png")
	decrease_LIGHTS_REF = decrease_LIGHTS_REF.resize((64, 64))
	decrease_LIGHTS_ICON = ImageTk.PhotoImage(decrease_LIGHTS_REF)

	alarm_REF = Image.open("Alarm.png")
	alarm_REF = alarm_REF.resize((64, 64))
	alarm_ICON = ImageTk.PhotoImage(alarm_REF)

	about_REF = Image.open("About.png")
	about_REF = about_REF.resize((64, 64))
	about_ICON = ImageTk.PhotoImage(about_REF)

	#First Row
	btn1=tk.Button(root, text="Toggle LED", image=toggle_LIGHTS_ICON, compound="top", bg="blue", activebackground="blue", command=lambda: toggle_led(1)) #Lamda needed to pass dummy variable into constructor, else tk will run command without input and throw error
	btn1.place(x=100, y=20, width=150, height=150)
	btn2=tk.Button(root, text="Increase Brightness", image=increase_LIGHTS_ICON, compound="top", bg="green", activebackground="green", command=lambda: increase_brightness(1))
	btn2.place(x=270, y=20, width=150, height=150)
	
	#Second Row
	btn3=tk.Button(root, text="Decrease Brightness", image=decrease_LIGHTS_ICON, compound="top", bg="red", activebackground="red", command=lambda: decrease_brightness(1))
	btn3.place(x=270, y=190, width=150, height=150)
	btn4=tk.Button(root, text="Call For Help", image=alarm_ICON, compound="top", bg="yellow", activebackground="yellow", command=lambda: help_ASSIST(1))
	btn4.place(x=100, y=190, width=150, height=150)

	#About Button
	btn5=tk.Button(root, text="About", image=about_ICON, compound="top", command=show_help)
	btn5.place(x=440, y=95, width=150, height=150)

	root.protocol("WM_DELETE_WINDOW", on_close)
	root.mainloop()

#-------------Audio Callback---------------
def callback(indata, frames, time, status):
	if status:
		print(status, file=sys.stderr)
	q.put(bytes(indata))

#-------------Main Loop--------------------
try:
	threading.Thread(target=run_gui).start() #Run GUI on seperate thread
	
	with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
		print("Say something! Comands 'lights on/off'!")
		print("Press button to toggle lights!")
		while True:
			data = q.get()
			if rec.AcceptWaveform(data):
				result = json.loads(rec.Result())
				command = result.get("text", "")
				print("Recognized:", command)
				
				#-------Wake up function----------
				if is_AWAKE:
					#---------Voice Commands-----------
					if "lights on" in command:
						print("Turning ON lights")
						pwm.ChangeDutyCycle(led_brightness)
						tts.say("Turning on the lights")
						tts.runAndWait()
						last_command_time = time.time() #Reset last command time
						
					elif "lights off" in command:
						print("Turning OFF lights")
						pwm.ChangeDutyCycle(0)
						tts.say("Turning off the lights")
						tts.runAndWait()
						last_command_time = time.time() #Reset last command time

					elif "decrease brightness" in command:
						decrease_brightness(1)
						tts.say("Decreasing brightness")
						tts.runAndWait()
						last_command_time = time.time() #Reset last command time

					elif "increase brightness" in command:
						increase_brightness(1)
						tts.say("Increasing brightness")
						tts.runAndWait()
						last_command_time = time.time() #Reset last command time

					elif "help" in command:
						help_ASSIST(1)
						tts.say("Help is called an on the way")
						tts.runAndWait()
						last_command_time = time.time() #Reset last command time

				elif WAKE_WORD in command:
					print("Wake word Detected! Listening for commands!")
					toggle_Is_AWAKE(1)
					tts.say("How may I assist you")
					tts.runAndWait()
					last_command_time = time.time()
			
			#----------Go back to sleep after COMMAND_TIMEOUT lapse-----------
			if is_AWAKE and (time.time() - last_command_time > COMMAND_TIMEOUT):
				print("Command timeout. Returning to sleep mode")
				toggle_Is_AWAKE(1)



except KeyboardInterrupt:
	print("Stopping...")
	
finally:
	pwm.stop()
	GPIO.cleanup()
					
