## Import required libraries
#import google.generativeai as genai
#import os
#import PIL.Image # Import Pillow library
#
#key = 'AIzaSyBaR3sjzPM73-E7ClbJrhStdmDPvJdrmyE' # Set up API key for Google Generative AI
#genai.configure(api_key=key)
#
#model = genai.GenerativeModel('models/gemini-1.5-flash-latest') # Initialize the model
#
#response = model.generate_content("The opposite of hot is") # Generate text with a prompt
#print(response.text)
#
#img = PIL.Image.open('/content/your_image_file.png') # Load and display an image
#
#img.show()  # To display the image
#
#response = model.generate_content([
#    "Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", 
#    img
#], stream=True) # Generate content from an image and prompt
#
#response.resolve()  # Wait for response
#
#print(response.text) # Print the generated content

#*****
#import google.generativeai as genai
#import os
#import PIL.Image  # Import Pillow library
#import cv2
#import logging  # Import logging library
#import gpio as GPIO
#
#GPIO.setup([447, 448], GPIO.IN)  # Set up GPIO pins
#
## Capture live image from the camera
#def capture_image():
#    cam = cv2.VideoCapture(1)  # Use the camera device
#    result, frame = cam.read()
#    if result:
#        cv2.imwrite("captured_image.jpg", frame)
#        cam.release()
#        cv2.destroyAllWindows()
#        return "captured_image.jpg"
#    else:
#        logging.error("Failed to capture image")
#        cam.release()
#        return None  # Return None in case of failure
#
## Set up API key for Google Generative AI
#key = 'AIzaSyBaR3sjzPM73-E7ClbJrhStdmDPvJdrmyE'
#genai.configure(api_key=key)
#
## Initialize the model
#model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
#
## Function to analyze the image and extract text
#def analyze_image(image_path):
#    try:
#        # Open the image using PIL
#        img = PIL.Image.open(image_path)
#
#        # Generate content from the image and prompt
#        response = model.generate_content([
#            "Identify the language of the text in this image, provide me only language code and extract the text content accurately atlast separate language code and accurate text content.", 
#            img
#        ], stream=True)
#
#        response.resolve()  # Wait for response
##        print(response)
##        print(response.text)  # Print the generated content
#        response_text = response.text.strip()  # Get the response text and remove leading/trailing whitespace
#
#        # Split the response text by newlines
#        parts = response_text.split('\n', 1)  # Split into two parts only, at the first newline
#        if len(parts) > 1:
#            language_code = parts[0].strip()  # The first part is the language code
#            extracted_text = parts[1].strip()  # The second part is the extracted text
#            print(f"Language Code: {language_code}")
#            print(f"Extracted Text: {extracted_text}")
#        else:
#            print("Unexpected response format. Please check the output.")
#    except Exception as e:
#        logging.error(f"Error analyzing the image: {e}")
#
## Capture an image
#img_path = capture_image()
#
#if img_path:  # Proceed if image is captured successfully
#    analyze_image(img_path)  # Analyze the captured image
#else:
#    print("Image capture failed. Please try again.")
#
## Main loop for GPIO input handling
#while True:
#    button_447_pressed = GPIO.input(447)
#    button_448_pressed = GPIO.input(448)
#    if button_447_pressed == True:
#        img_path = capture_image()
#        if img_path:  # Analyze the newly captured image
#            analyze_image(img_path)
#    elif button_448_pressed == True:
#        os._exit(0)
#**********

import gpio as GPIO
import cv2
import logging
import sys
import time
import requests
import vlc
import os
import subprocess
from queue import Queue
from pydub import AudioSegment
import PIL.Image
from gtts import gTTS
sys.path.insert(0, '/home/rock/Desktop/HS/')
from visionary_ai_stream.visionary_AI_stream2 import VisionaryAI
from env.camera import cap
from env.play_audio import GTTSA

play_audio = GTTSA()
GPIO.setup([447, 448], GPIO.IN)  # Setup GPIO for buttons
vi_obj = VisionaryAI()

def log_time(func_name, start_time, end_time):
    duration = end_time - start_time
    print(f"{func_name} executed in {duration:.4f} seconds\n")

class Read:
    def __init__(self):
        self.text_queue = Queue()
        self.image_path = "/home/rock/Desktop/HS/read/frame.jpg"
        self.shutter_sound = "/home/rock/Desktop/HS/audios/English_audio/shutter_sound.mp3"
    
    def get_image_vision(self):
        start_time = time.time()
        subprocess.run(["rm", "-r", self.image_path])
        if not self.internet_connection():
            play_audio.play_machine_audio("Check_your_internet_connection.mp3")
            os._exit(0)
        
        if not cap().isOpened():
            play_audio.play_machine_audio("camera is not working.mp3")
            os._exit(0)
        
        ret, frame = cap().read()
        cap().release()
        
        if not ret:
            play_audio.play_machine_audio("camera is not working.mp3")
            return None    

        cv2.imwrite(self.image_path, frame)
        log_time("camera_interface", start_time, time.time())

        img = PIL.Image.open(self.image_path)
        
        response = vi_obj.model.generate_content([
            "Identify the language of the text in this image. Provide only the language code and extract the text content accurately. Separate language code and content.", 
            img
        ], stream=True)
        response.resolve()
        
        response_text = response.text.strip()
        parts = response_text.split('\n', 1)
        
        if len(parts) > 1:
            language_code = parts[0].strip()
            extracted_text = parts[1].strip()
            
            # Handle case for unclear image
            if extracted_text == "No text found" or extracted_text == "```" or language_code == "und" or language_code == "```" :
                play_audio.play_machine_audio("Unclear Image.mp3")
                return
            
            print(f"Language Code: {language_code}")
            print(f"Extracted Text: {extracted_text}")
            
            self.play_audio_func(language_code, extracted_text, speed=1.5)
        else:
            play_audio.play_machine_audio("Unclear Image.mp3")

    def generate_audio(self, text, lang, filename):
        try:
            tts = gTTS(text=text, lang=lang)
            tts.save(filename)
        except Exception as e:
            logging.error(f"Error generating audio with gTTS: {e}")
            
    def play_audio_func(self, language_code, extracted_text, speed=1.5):
        current_audio = "/home/rock/Desktop/HS/read/voice_current.mp3"
        
        if extracted_text != "No text found.":
            self.generate_audio(extracted_text, language_code, current_audio)
            media = vlc.MediaPlayer(current_audio)
            media.play()
            media.set_rate(speed)  # Set playback speed
            duration = self.get_audio_duration(current_audio) / speed  # Adjust for playback speed

            start_time = time.time()
            while time.time() - start_time < duration:
                if GPIO.input(448):  # Exit button pressed
                    media.stop()
                    os._exit(0)
                time.sleep(0.1)
                
            media.stop()
            media.release()

    def get_audio_duration(self, filename):
        audio = AudioSegment.from_file(filename)
        duration_in_seconds = len(audio) / 1000
        return duration_in_seconds

    def vision(self):
        while True:
            button_447_pressed = GPIO.input(447)
            button_448_pressed = GPIO.input(448)
            if button_447_pressed:
                self.capture_and_process_image()
            elif button_448_pressed:
                os._exit(0)

    def capture_and_process_image(self):
        if self.internet_connection():
            media = vlc.MediaPlayer(self.shutter_sound)
            media.play()
            time.sleep(self.get_audio_duration(self.shutter_sound))         
            start_time = time.time()
            self.get_image_vision()
            log_time("vision", start_time, time.time())
        else:
            os._exit(0)

    def internet_connection(self):
        start_time = time.time()
        try:
            response = requests.get("https://www.google.com", timeout=5)
            log_time("internet_connection_true", start_time, time.time())
            return True
        except requests.ConnectionError:
            play_audio.play_machine_audio("Check_your_internet_connection.mp3")
            log_time("internet_connection_false", start_time, time.time())
            return False

if __name__ == "__main__":
    vi = Read()
    if vi.internet_connection():
        vi.vision()
    else:
        sys.exit()
