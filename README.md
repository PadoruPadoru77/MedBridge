# MedBridge
MedBridge is a Medical Assistance Device I created with my partner Adam Tompkins during the summer of 2025 for our class ECE 510 at IIT. The goal was to create a medical assistant device for patients with ALS to have a sense of quality in their remaining life.

### ABSTRACT:<br/>
This project introduces MedBridge, an affordable, voice-activated assistive device designed to restore autonomy and improve safety for individuals with limited mobility. Using a Raspberry Pi 4 and the offline Vosk speech recognition engine, MedBridge allows patients to perform essential tasks, such as calling for help or controlling aspects of their environment, through simple voice commands or physical inputs. The system operates entirely offline to ensure user privacy and functions reliably even in noisy environments. With components like a buzzer for nurse alerts, a push-button panic switch, and optional lighting control via LEDs, MedBridge is designed to be intuitive and adaptable for users with varying speech clarity and physical ability. Unlike commercial systems that cost thousands of dollars, MedBridge delivers comparable core functionality using open-source tools and modular hardware. Future enhancements include 3D-printed enclosures, expanded voice command capabilities, and integration of lightweight Large Language Models for more natural communication. MedBridge ultimately aims to empower patients by giving them greater control over their environment and a faster, simpler way to reach caregivers when needed.

### PROJECT SUMMARY & PURPOSE:<br/>
Medbridge is a modular, low-cost assistive platform built to restore environmental control, communication, and health monitoring for individuals with limited mobility. Examples include patients affected by amyotrophic lateral sclerosis (ALS), spinal cord injuries, stroke, and other neuromuscular conditions. While ALS provides a clear use case, affecting about 1.7–2.2 per 100,000 people each year, Medbridge’s flexible design supports any user who can speak or use a simple physical interface.
At its heart, Medbridge uses a Raspberry Pi 4 single-board computer because of its processing power, memory, and general-purpose I/O capabilities. The device runs entirely offline to protect patient privacy and ensure reliable operation even when internet service is unavailable. An open-source Vosk speech-recognition engine transcribes voice commands in under 200 ms on the Pi’s quad-core ARM CPU. A Python intent parser then reads Vosk’s JSON output and issues GPIO commands to control lighting relays or activate a bedside buzzer when the user says, “lights on” or “help me.” For users with unclear speech, a large push-button panic switch provides a manual fallback to send immediate alerts.
Medbridge’s hardware bundle includes a plug-and-play USB microphone, an audio amplifier with speaker for text-to-speech feedback, and optional modules such as eye-gaze trackers or flex-sensor gloves to broaden accessibility. Integrated health sensors, such as heart rate and temperature probes, continuously monitor vital signs. If any measurement strays beyond safe limits, the system automatically sends SMS or email alerts to caregivers. A companion mobile app displays real-time vitals and conversation logs, so caregivers can respond quickly without compromising patient confidentiality.
By keeping the total cost under $100, Medbridge offers a dramatic price advantage over commercial speech-generating devices and proprietary nurse-call systems, which often exceed several thousand dollars and require ongoing subscriptions. Its open-platform architecture makes it easy for hospitals, long-term care facilities, nonprofits, and individual caregivers to customize and deploy. Future improvements include optional cloud synchronization for remote monitoring, machine-learning based language prediction to speed input, and eventual brain-computer interface integration. Medbridge closes a crucial gap in assistive technology by combining robust offline operation, multiple input methods, and extreme affordability to extend autonomy and dignity to all mobility-impaired patients.

### HARDWARE DESCRIPTION:<br/>
- Raspberry Pi 4 - MCU for this project<br/>
- Active Buzzer - Used to mimic a call for help for nurses to attend to patients<br/>
- LEDS - Used to mimic controllable room lights<br/>
- USB Microphone - Used to pick up audio for voice recognition functionality<br/>
- Speaker with AUX cable - Used to give audio feedback when voice commands are used<br/>
- Raspberry Pi Touch Screen - Used to provide an interactive GUI for any users to control the device<br/>
- Push buttons - Used to act as manual control for the device for all users<br/>
- 220 Ohm Resistors - Resistors for push buttons and LEDS to control the current going through them<br/>
- wires - Used to connect all the modules<br/>

### LAYOUT:<br/>
![image_2025-07-05_154214456](https://github.com/user-attachments/assets/51ee4524-2a72-4b59-a0c4-a1b7142299a5)

### SOFTWARE DESCRIPTION:<br/>
- Python - Main programming language<br/>
- Vosk - Speech-to-text translator<br/>
- pyttsx3 - text-to-speech translator<br/>

### NOTES:<br/>
- Exact configuration of wire placements on the GPIO of the Pi is written in the comments of the code, any GPIO port works, as long as its configurable<br/>
- Checkout our IEEE paper for more details of this project!<br/>
- We wanted to make this project easy to understand an replicate, there is room for further improvement such as adding eye tracking functionality, however due to time constraints, this is what we could accomplish.<br/>



