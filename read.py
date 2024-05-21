import cv2
import pytesseract
import numpy as np
import os
import gpio as GPIO
from PIL import Image
import time
import vlc
import re
from time import sleep
from datetime import datetime
from os import path
import subprocess
import sys
import pyttsx3
from pydub import AudioSegment
sys.path.insert(0, '/home/rock/Desktop/Hearsight/')
from play_audio import GTTSA
play_machine_voice = GTTSA()
engine = pyttsx3.init()

a = "/home/rock/Desktop/Hearsight/lang.txt"
#from English.machine_voice.machine_voice import MachineVoices

#machineVoice_obj = MachineVoices()

image_path = "/home/rock/Desktop/Hearsight/English/read/01.jpg"
dst1_path = "/home/rock/Desktop/Hearsight/English/read/dst1.png"
dst2_path = "/home/rock/Desktop/Hearsight/English/read/dst2.png"
#READ_FILES = "/home/rock/Desktop/Hearsight/English/read/read_files/"

#GPIO.setup(450, GPIO.IN)
#GPIO.setup(421, GPIO.IN)
GPIO.setup(447, GPIO.IN)
GPIO.setup(448, GPIO.IN)

#def get_name():
#    base_name = "page"
#    existing_files = os.listdir(READ_FILES)
#    existing_files = [file for file in existing_files if os.path.isfile(os.path.join(READ_FILES, file))]
#    existing_numbers = []
#    for file_name in existing_files:
#        if file_name.startswith(base_name):
#            try:
#                number = int(file_name[len(base_name):].split('.')[0])  # Extract number before any extension
#                existing_numbers.append(number)
#            except ValueError:
#                pass
#    if existing_numbers:
#        next_number = max(existing_numbers) + 1
#    else:
#        next_number = 0
#    new_name = f"{base_name}{next_number}"
#    return new_name

def get_audio_duration(filename):
    
    audio = AudioSegment.from_file(filename)
    duration_in_seconds = len(audio) / 1000  # Convert milliseconds to seconds
    return duration_in_seconds

    
def play_machine_A(voice, speed = 1.6):
          
    MACHINE_VOICE_DIR = f"/home/rock/Desktop/Hearsight/audios/English_audio/"
    
    try:
        os.path.exists(MACHINE_VOICE_DIR)
        print(voice)
        filename = os.path.join(MACHINE_VOICE_DIR, voice)
        media = vlc.MediaPlayer(filename)
        media.play()
        media.set_rate(speed)  # Set the playback speed
        duration = get_audio_duration(filename)
        time.sleep(float(duration) / speed)  # Adjust sleep time for playback speed
        media.stop()
        media.release()
    except Exception as e:
        print(f"Audio :{voice} not found")
        pass
        
#def custom_sort_key(word):
#
#    parts = re.split(r'(\d+)', word)
#    
#    numerical_part = int(parts[1]) if len(parts) > 1 else 0
#    
#    return (parts[0], numerical_part)

# Sort the words with numbers

#class MachineVoiceHandler:
#    def __init__(self, machine_voice_obj):
#        self.machineVoice_obj = machine_voice_obj
#
#    def handle_machine_voice_features(self):
#        counts = 1
#        play_machine_voice.play_machine_audio("press_feature_button.mp3")
#        while True:
#            input_state1 = GPIO.input(450)
#            input_state2 = GPIO.input(421)
#            input_state3 = GPIO.input(447)
#            input_state4 = GPIO.input(448)
#
#            if input_state1:
#                counts = (counts + 1) % 2
#                play_machine_voice.play_machine_audio("male_voices.mp3" if counts == 0 else "female_voices.mp3")
#
#            if input_state2:
#                counts = (counts - 1) % 2
#                play_machine_voice.play_machine_audio("male_voices.mp3" if counts == 0 else "female_voices.mp3")
#
#            if input_state3 and counts == 0:  # change male voices
#                play_machine_voice.play_machine_audio("feature_confirmed.mp3")
#                self.machineVoice_obj.change_voice("male")
#                play_machine_voice.play_machine_audio("Thank You.mp3")
#                break
#
#            if input_state3 and counts == 1:  # change female voices
#                play_machine_voice.play_machine_audio("feature_confirmed.mp3")
#                self.machineVoice_obj.change_voice("female")
#                play_machine_voice.play_machine_audio("Thank You.mp3")
#                break
#
#            if input_state4:  # Exit feature
#                play_machine_voice.play_machine_audio(f"feature_exited.mp3")  # yet to create
#                play_machine_voice.play_machine_audio("Thank You.mp3")

#    def __init__(self):
#        self.languages = {"Hindi": "hin", "English": "eng", "Tamil": "tam", "Malayalam": "mal", "Telugu": "tel", "Kannada": "kan"}
#                
#    def handle_lang(self):
#        play_machine_voice.play_machine_audio("press_feature_button.mp3")
#        counts = -1
#        selected_language = None
#        
#        while True:
#            input_state1 = GPIO.input(450)
#            input_state2 = GPIO.input(421)
#            input_state3 = GPIO.input(447)
#            input_state4 = GPIO.input(448)
#            
#            if input_state1:
#                direction = 1
#                counts = (counts + direction) % len(self.languages)
#                selected_language = list(self.languages.keys())[counts]
#                print(counts)
#                self.play_machine_voice.play_machine_audio("{}.mp3".format(selected_language))
#
#            if input_state2:
#                direction = -1
#                counts = (counts + direction) % len(self.languages)
#                selected_language = list(self.languages.keys())[counts]
#                print(counts)
#                self.play_machine_voice.play_machine_audio("{}.mp3".format(selected_language))
#
#            if input_state3:
#                self.play_machine_voice.play_machine_audio("feature_confirmed.mp3")
#                language_code = self.languages[selected_language]
#                print(f"Selected Language: {selected_language}, Language Code: {language_code}")
#                self.play_machine_voice.play_machine_audio("Thank You.mp3")
#                break
#
#            if input_state4:
#                self.play_machine_voice.play_machine_audio(f"feature_exited.mp3")
#                self.play_machine_voice.play_machine_audio("Thank You.mp3")
#                break

#    def __init__(self):
#        self.languages = {"Hindi": "hin", "English": "eng", "Tamil": "tam", "Malayalam": "mal", "Telugu": "tel", "Kannada": "kan"}


class TextRecognition:
#    def __init__(self, image_path, dst1_path, dst2_path, audio_folder):
    def __init__(self, image_path, dst1_path, dst2_path):
        self.image_path = image_path
        self.dst1_path = dst1_path
        self.dst2_path = dst2_path
#        self.language_code = language_code
#        self.audio_folder = audio_folder

    def read_file(self):
#        txt_files = []
#        for root, dirs, files in os.walk(READ_FILES):
#            for file in files:
#                txt_files.append(file)
#        txt_files = sorted(txt_files, reverse = True)
#        length = len(txt_files)
#        print("Length: ",length)
        
#        if length >= 1000:
#            play_machine_voice.play_machine_audio("file_limit_exceeded_please_delete_some_files.mp3")
#            play_machine_voice.play_machine_audio("total_files.mp3")
#            
#            if length >= 110 and length <= 999:
#                hun = str(length)[0]
#                tens = str(length)[1:]
#                play_machine_A(f"number_{hun}.mp3")
#                play_machine_A(f"number_100.mp3")
#                if tens != "00":
#                    play_machine_A(f"and.mp3")
#                    play_machine_A(f"number_{tens}.mp3")
#            else:  
#                play_machine_A(f"number_{length}.mp3")
#                
#            play_machine_voice.play_machine_audio("Thank You.mp3")
#            return
    
        cap = cv2.VideoCapture(1)  # Change the camera index as needed
        if not cap.isOpened():
#            play_machine_voice.play_machine_audio("camera_is_not_working_so_switch_off_the_HearSight_device_for_some_time_and_then_start_it_again.mp3")
#            play_machine_voice.play_machine_audio("check_your_connection_and_proceed.mp3")
            play_machine_voice.play_machine_audio("hold_on_connection_in_progress_initiating_shortly.mp3")
            play_machine_voice.play_machine_audio("Thank You.mp3")
            subprocess.run(["reboot"])
#            play_machine_voice.play_machine_audio("press your feature button now.mp3")
#            play_machine_voice.play_machine_audio("otherwise.mp3")
#            play_machine_voice.play_machine_audio("press exit button.mp3")
#            play_machine_voice.play_machine_audio("Thank You.mp3")
#        return
        cap.release()
        cv2.destroyAllWindows()
    
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
            os.remove(self.dst1_path)
            os.remove(self.dst2_path)
    
    # Capture the image using OpenCV (cv2)
#        cap = cv2.VideoCapture(1)
#        ret, frame = cap.read()
#        if not ret:
#            play_machine_voice.play_machine_audio("image_capture_failed_so_retake_it_again.mp3")
#            play_machine_voice.play_machine_audio("press your feature button now.mp3")
#            play_machine_voice.play_machine_audio("otherwise.mp3")
#            play_machine_voice.play_machine_audio("press exit button.mp3")
#            return
#        cv2.imshow("Captured Image", frame)
#        # Wait for 10 seconds (10000 milliseconds)
#        cv2.waitKey(10000)
#        cv2.imwrite(image_path, frame)
#        cap.release()
#        cv2.destroyAllWindows()

        # Set the video capture duration (in seconds)
        capture_duration = 5
        # Initialize video capture
        cap = cv2.VideoCapture(1)
        # Get the current time in seconds
        start_time = cv2.getTickCount() / cv2.getTickFrequency()
        while True:
            # Capture a frame
            ret, frame = cap.read()
            if not ret:
                print("Video capture failed.")
                play_machine_voice.play_machine_audio("image_capture_failed_so_retake_it_again.mp3")
                break
            # Display the video frame
            cv2.imshow("Video Capture", frame)
            # Calculate the elapsed time in seconds
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            elapsed_time = current_time - start_time
            # Check if the capture duration has been reached
            if elapsed_time >= capture_duration:
                # Save the captured image to the specified location
                cv2.imwrite(self.image_path, frame)
                break
            # Check for key press to exit (e.g., press 'q' key)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release video capture and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        if os.path.exists(self.image_path):
            play_machine_voice.play_machine_audio("Image_captured.mp3")

            fname = self.image_path
            bgray = cv2.imread(fname)[..., 0]
            th, threshed = cv2.threshold(bgray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            cv2.imwrite(self.dst2_path, threshed)
            img = cv2.imread(self.image_path)
            I = Image.open(fname)
            I.show()
            img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            kernel = np.ones((1, 1), np.uint8)
            img = cv2.dilate(img, kernel, iterations=1)
            img = cv2.erode(img, kernel, iterations=1)
            img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            cv2.imwrite(self.dst1_path, img)
            i = Image.open(self.dst1_path)
            play_machine_voice.play_machine_audio("Processing.mp3")
            with open(a,'r') as file:
                language_code = file.read()
            print(language_code)
            if language_code == "":
    #                language_code = "eng"
                language_code = "English"
                with open(a,'w') as file:
                    file.write(language_code)
                print(language_code)
            with open(a,'r') as file:
                language_code = file.read()
            print(language_code)
            if language_code == "English":
                print(language_code)
                code = "eng"
                print(code)
            if language_code == "Hindi":
                print(language_code)
                code = "hin"
                print(code)
            if language_code == "Tamil":
                print(language_code)
                code = "tam"
                print(code)
            if language_code == "Malayalam":
                print(language_code)
                code = "mal"
                print(code)
            if language_code == "Telugu":
                print(language_code)
                code = "tel"
                print(code)
            if language_code == "Kannada":
                print(language_code)
                code = "kan"
                print(code)
            
    #            result = pytesseract.image_to_string(img, lang="eng")
    #            result = pytesseract.image_to_string(img, lang = language_code)# Replace "eng" with the variable language_code
            result = pytesseract.image_to_string(img, lang = code)# Replace "eng" with the variable language_code
            play_machine_voice.play_machine_audio("Processing.mp3")

            print('espeak len = ', len(result))
            res = result.replace('"', ' ')
            res = res.replace('“', ' ')
            result = "\"" + str(res) + "\""
            print("result: ", result)
#            engine.setProperty('voice', 'english_rp+f3')
#            engine.setProperty('rate', 120)
            engine.setProperty('voice', 'en-gb')
            engine.setProperty('rate', 140)
            engine.say(result)
            engine.runAndWait()
            time.sleep(1)
            if str(res).isspace() == True:
                play_machine_voice.play_machine_audio("Unclear Image.mp3")
                cv2.destroyAllWindows()
                os.remove(self.image_path)
                os.remove(self.dst1_path)
                os.remove(self.dst2_path)
                sys.exit()
            else:
                with open("/home/rock/Desktop/Hearsight/English/read/read_files/read.txt", "w") as file:
                    file.write(result)
                play_machine_voice.play_machine_audio("for_replay_press_confirm.mp3")
                while True:
                    if GPIO.input(447)==True:
            #                play_machine_voice.play_machine_audio("feature_confirmed.mp3")
                        with open("/home/rock/Desktop/Hearsight/English/read/read_files/read.txt", "w") as file:
                            file.write(result)
                        print('espeak len = ', len(result))
                        res = result.replace('"', ' ')
                        res = res.replace('“', ' ')
                        result = "\"" + str(res) + "\""
                        print("result: ", result)
#                        engine.setProperty('voice', 'english_rp+f3')
#                        engine.setProperty('rate', 120)
                        engine.setProperty('voice', 'en-gb')
                        engine.setProperty('rate', 140)
                        engine.say(result)
                        engine.runAndWait()
                        time.sleep(1)
                        
                    if GPIO.input(448)==True:
                        play_machine_voice.play_machine_audio("feature_exited.mp3")
                        os.remove("/home/rock/Desktop/Hearsight/English/read/read_files/read.txt")
                        cv2.destroyAllWindows()
                        os.remove(self.image_path)
                        os.remove(self.dst1_path)
                        os.remove(self.dst2_path)
                        break
            
#            if str(res).isspace() == True:
#                play_machine_voice.play_machine_audio("Unclear Image.mp3")
#            else:
#                machineVoice_obj = MachineVoices()  # Create the object here if not done already
#                arr = []
#                arr = result.split()
#                print("array", arr)
#                output = get_name()
#                file_name = f"/home/rock/Desktop/Hearsight/English/read/read_files/{output}.txt"
#                with open(file_name, "w") as file:
#                    file.write(result)
#                print(f"Text has been written to {file_name}")

#                machineVoice_obj.speak_file(file_name)
                            
#                play_machine_voice.play_machine_audio("file_name_saved_as.mp3")
            
#                num = int((output.replace('page','')).replace(".txt",""))
            
#                play_machine_voice.play_machine_audio("page.mp3")
#                if length >= 110 and length <= 999:
#                    hun = str(length)[0]
#                    tens = str(length)[1:]
#                    play_machine_A(f"number_{hun}.mp3")
#                    play_machine_A(f"number_100.mp3")
#                    if tens != "00":
#                        play_machine_A(f"and.mp3")
#                        play_machine_A(f"number_{tens}.mp3")                
#                else:  
#                    play_machine_A(f"number_{num}.mp3")
#                
#                play_machine_voice.play_machine_audio("total_files.mp3")
#                
#                length = len(txt_files) + 1
#                
#                if length >= 110 and length <= 999:
#                    hun = str(length)[0]
#                    tens = str(length)[1:]
#                    play_machine_A(f"number_{hun}.mp3")
#                    play_machine_A(f"number_100.mp3")
#                    if tens != "00":
#                        play_machine_A(f"and.mp3")
#                        play_machine_A(f"number_{tens}.mp3")
#                    
#                else:  
#                    play_machine_A(f"number_{length}.mp3")
                
#                play_machine_voice.play_machine_audio("Thank You.mp3")

#            cv2.destroyAllWindows()
#            os.remove(self.image_path)
#            os.remove(self.dst1_path)
#            os.remove(self.dst2_path)
        else:
#            play_machine_voice.play_machine_audio("camera_is_not_working_so_switch_off_the_HearSight_device_for_some_time_and_then_start_it_again.mp3")
#            play_machine_voice.play_machine_audio("check_your_connection_and_proceed.mp3")
            play_machine_voice.play_machine_audio("hold_on_connection_in_progress_initiating_shortly.mp3")
            play_machine_voice.play_machine_audio("Thank You.mp3")
            subprocess.run(["reboot"])
#            play_machine_voice.play_machine_audio("press your feature button now.mp3")
#            play_machine_voice.play_machine_audio("otherwise.mp3")
#            play_machine_voice.play_machine_audio("press exit button.mp3")
#            play_machine_voice.play_machine_audio("Thank You.mp3")
            
#def delete_file(name_to_delete):
#    
#    base_folder = READ_FILES
#
#    for root, dirs, files in os.walk(base_folder):
#        for file in files:
#            if name_to_delete in file:
#                file_path = os.path.join(root, file)
#                os.remove(file_path)
#                print(f"Deleted file: {file_path}")

#def file_handler(action):
#    
#    if len(READ_FILES) == 0 and action == "remove": 
#        play_machine_voice.play_machine_audio(f"no_files_to_remove.mp3")
#    else:
#        txt_files = []
#        for root, dirs, files in os.walk(READ_FILES):
#            for file in files:
#                txt_files.append(file)
#                
#        txt_files = sorted(txt_files, key = custom_sort_key,reverse = True)
#        txt_files = sorted(txt_files, reverse = True)
#        print(txt_files)
#        play_machine_voice.play_machine_audio("press_feature_button.mp3")
#        if len(txt_files) == 0:
#            play_machine_voice.play_machine_audio("no_text_files_available.mp3")
#            play_machine_voice.play_machine_audio("Thank You.mp3")
#            play_machine_voice.play_machine_audio("press_feature_button.mp3")
#            return
#        play_machine_voice.play_machine_audio("press_feature_button.mp3")
#        count = -1
#        while True:
#            if GPIO.input(450)==True:
#                direction = 1
#                count = (count + direction) % len(txt_files)
#                print(count)
#                print(txt_files[count])
#                page = txt_files[count]
#                num = int((page.replace('page','')).replace(".txt",""))
#                play_machine_voice.play_machine_audio("page.mp3",1.6)
#                    
#                if num >= 110 and num <= 999:
#                    hun = str(num)[0]
#                    tens = str(num)[1:]
#                    play_machine_A(f"number_{hun}.mp3")
#                    play_machine_A(f"number_100.mp3")
#                    if tens != "00":
#                        play_machine_A(f"and.mp3")
#                        play_machine_A(f"number_{tens}.mp3")
#                    
#                else:  
#                    play_machine_A(f"number_{num}.mp3")
#
#            if GPIO.input(421)==True:
#                direction = -1
#                count = (count + direction) % len(txt_files)
#                print(count)
#                print(txt_files[count])
#                page = txt_files[count]
#                num = int((page.replace('page','')).replace(".txt",""))
#                play_machine_voice.play_machine_audio("page.mp3",1.6)
#                if num >= 110 and num <= 999:
#                    hun = str(num)[0]
#                    tens = str(num)[1:]
#                    play_machine_A(f"number_{hun}.mp3")
#                    play_machine_A(f"number_100.mp3")
#                    if tens != "00":
#                        play_machine_A(f"and.mp3")
#                        play_machine_A(f"number_{tens}.mp3")
#                    
#                else:
#                    play_machine_A(f"number_{int(num)}.mp3")
#
#            if GPIO.input(447)==True:
#                play_machine_voice.play_machine_audio("feature_confirmed.mp3")
#                
#                if action == "remove":
#                    delete_file(txt_files[count].replace(".txt",""))
#                    play_machine_voice.play_machine_audio(f"file_removed_successfully.mp3")
#                    play_machine_voice.play_machine_audio("total_files.mp3")
#                    length = len(txt_files) - 1
#                    
#                    if length >= 110 and length <= 999:
#                        hun = str(length)[0]
#                        tens = str(length)[1:]
#                        play_machine_A(f"number_{hun}.mp3")
#                        play_machine_A(f"number_100.mp3")
#                        if tens != "00":
#                            play_machine_A(f"and.mp3")
#                            play_machine_A(f"number_{tens}.mp3")
#                        
#                    else:  
#                        play_machine_A(f"number_{length}.mp3")
#                else:
#                    print(len(txt_files))
#                    file_name = os.path.join(READ_FILES,txt_files[count])
#                    machineVoice_obj.speak_file(file_name)
#                    print(file_name)
#                    with open(file_name, 'r') as file:# Read the content of the file
#                        file_content = file.read()
#                    engine.setProperty('voice', 'english_rp+f3')
#                    engine.setProperty('rate', 120)  # Speed of speech
#                    engine.say(file_content) # Convert the text to speech                 
#                    engine.runAndWait() # Wait for the speech to finish
#                play_machine_voice.play_machine_audio("Thank You.mp3")
#                break

#            if GPIO.input(448)==True:
#                play_machine_voice.play_machine_audio("feature_exited.mp3")
#                break
        
def read_handler():
#    counts = 0
#    play_machine_voice.play_machine_audio("press_feature_button.mp3")
#
#    while True:
#        input_state1 = GPIO.input(450)
#        input_state2 = GPIO.input(421)
#        input_state3 = GPIO.input(447)
#        input_state4 = GPIO.input(448)
#
#        if input_state1:
#            counts = (counts + 1) % 3
#            play_machine_voice.play_machine_audio("delete_file.mp3" if counts == 0 else ("add_file.mp3" if counts == 1 else "read_file.mp3"))
#            print(counts)
#
#        if input_state2:
#            counts = (counts - 1) % 3
#            play_machine_voice.play_machine_audio("delete_file.mp3" if counts == 0 else ("add_file.mp3" if counts == 1 else "read_file.mp3"))
#            print(counts)
#        
#        if input_state3 == True and counts == 0:
#            print(counts)
#            play_machine_voice.play_machine_audio("feature_confirmed.mp3")
#            file_handler("remove")
#        
#        if input_state3 == True and counts == 1:
#            print(counts)
#            play_machine_voice.play_machine_audio("feature_confirmed.mp3")
#            text_recognition = TextRecognition(image_path, dst1_path, dst2_path, audio_folder)
    text_recognition = TextRecognition(image_path, dst1_path, dst2_path)
    text_recognition.read_file()
#            text_recognition = TextRecognition(image_path, dst1_path, dst2_path, language_code)
#            text_recognition.read_file()
            
#        if input_state3 == True and counts == 2:
#            print(counts)
#            play_machine_voice.play_machine_audio("feature_confirmed.mp3")
#            file_handler("read")
#
#        if input_state4 == True:
#            play_machine_voice.play_machine_audio("feature_exited.mp3")
#            play_machine_voice.play_machine_audio("press_feature_button.mp3")
#            break
        
#def select_language():
#    play_machine_voice.play_machine_audio("press_feature_button.mp3")
#    languages = {"Hindi": "hin", "English": "eng", "Tamil": "tam", "Malayalam": "mal", "Telugu": "tel", "Kannada": "kan"}
#    counts = -1
#    selected_language = None
#    
#    while True:
#        input_state1 = GPIO.input(450)
#        input_state2 = GPIO.input(421)
#        input_state3 = GPIO.input(447)
#        input_state4 = GPIO.input(448)
#        
#        if input_state1:
#            direction = 1
#            counts = (counts + direction) % len(languages)
#            selected_language = list(languages.keys())[counts]
#            print(counts)
#            play_machine_voice.play_machine_audio("{}.mp3".format(selected_language))
#
#        if input_state2:
#            direction = -1
#            counts = (counts + direction) % len(languages)
#            selected_language = list(languages.keys())[counts]
#            print(counts)
#            play_machine_voice.play_machine_audio("{}.mp3".format(selected_language))
#
#        if input_state3:
#            play_machine_voice.play_machine_audio("feature_confirmed.mp3")
#            language_code = languages[selected_language]
#            print(f"Selected Language: {selected_language}, Language Code: {language_code}")
#            print(a)
#            os.remove(a)
#            with open(a,'w') as file:
#                file.write(language_code)
#            play_machine_voice.play_machine_audio("Thank You.mp3")
#            play_machine_voice.play_machine_audio("press_feature_button.mp3")
#            break
#            
#        if input_state4:
#            play_machine_voice.play_machine_audio("feature_exited.mp3")
#            play_machine_voice.play_machine_audio("press_feature_button.mp3")
#            break

def main():
#    counts = 1
#    play_machine_voice.play_machine_audio("press_feature_button.mp3")
#
#    while True:
#        input_state1 = GPIO.input(450)
#        input_state2 = GPIO.input(421)
#        input_state3 = GPIO.input(447)
#        input_state4 = GPIO.input(448)
#
#        if input_state1:
#            counts = (counts + 1) % 2
#            print(counts)
#            play_machine_voice.play_machine_audio("change_voice.mp3" if counts == 0 else "stand_read.mp3")
#            play_machine_voice.play_machine_audio("change_voice.mp3" if counts == 0 else ("stand_read.mp3" if counts == 1 else "change_language.mp3"))
#            play_machine_voice.play_machine_audio("change_language.mp3" if counts == 0 else "stand_read.mp3")
#
#        if input_state2:
#            counts = (counts - 1) % 2
#            print(counts)
#            play_machine_voice.play_machine_audio("change_voice.mp3" if counts == 0 else "stand_read.mp3")
#            play_machine_voice.play_machine_audio("change_voice.mp3" if counts == 0 else ("stand_read.mp3" if counts == 1 else "change_language.mp3"))
#            play_machine_voice.play_machine_audio("change_language.mp3" if counts == 0 else "stand_read.mp3")
            
#        if input_state3 == True and counts == 0:
#            play_machine_voice.play_machine_audio("feature_confirmed.mp3")
##            handle_lang()
##            break
#            machine_voice_handler = MachineVoiceHandler(machineVoice_obj)
#            machine_voice_handler.handle_machine_voice_features()

#        if input_state3 == True and counts == 0:
#            play_machine_voice.play_machine_audio("feature_confirmed.mp3")
#            machine_voice_handler = MachineVoiceHandler(machineVoice_obj)
#            machine_voice_handler.handle_machine_voice_features()
#            handle_lang()
#            select_language()
            
            # Continue with the main loop instead of breaking
#            counts = 1  # Reset counts to avoid immediate language change on returning to main

#        if input_state3 == True and counts == 1:
#            play_machine_voice.play_machine_audio("feature_confirmed.mp3")
    read_handler()
#            break
#            change_language = MachineVoiceHandler()
#            change_language.handle_lang()
#            read_handler()
#            
#        if input_state4 == True:
#            play_machine_voice.play_machine_audio("feature_exited.mp3")
#            break

if __name__ == "__main__":
    main()
