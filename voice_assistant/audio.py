 #voice_assistant/audio.py
import speech_recognition as sr # type: ignore
import pygame # type: ignore
import time
import logging
import pydub # type: ignore
from io import BytesIO
from pydub import AudioSegment # type: ignore
from voice_assistant.config import Config
import threading
import datetime
from voice_assistant.person_classifier import Person_classifier
from colorama import Fore, init # type: ignore
#############
#SETUP COLORAMA AND LOGGING
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize colorama
init(autoreset=True)


# voice_assistant/main.py

import logging
from voice_assistant.transcription import transcribe_audio
from voice_assistant.response_generation import generate_response
from voice_assistant.text_to_speech import text_to_speech
from voice_assistant.config import Config
from voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key
from voice_assistant.voice_deepfake_detector import detect_fake
#from voice_assistant.database import login_or_register,close_connection


###################################################
import threading

# Define an event to control the listener's behavior
#stop_listening_event = threading.Event()
#
#def listen_for_wake_word(recognizer, microphone, wake_word):
#    while not stop_listening_event.is_set():
#        try:
#            with microphone as source:
#                audio = recognizer.listen(source, phrase_time_limit=2)
#                try:
#                    text = recognizer.recognize_google(audio, language="en-US")
#                    if text.lower() == wake_word:
#                        print("Wake word detected!")
#                        # Stop listening for wake word
#                        stop_listening_event.set()
#                        record_audio(Config.INPUT_AUDIO)  # Call the record_audio function
#                except sr.UnknownValueError:
#                    pass
#                except sr.RequestError:
#                    pass
#        except sr.WaitTimeoutError:
#            pass
#
#def listener_main():
#    recognizer = sr.Recognizer()
#    microphone = sr.Microphone()
#    wake_word = "hey alex"
#
#    # Start the wake word listener in a separate thread
#    wake_word_listener = threading.Thread(target=listen_for_wake_word, args=(recognizer, microphone, wake_word))
#    wake_word_listener.daemon = True
#    wake_word_listener.start()
#
#    # Keep the main thread running to keep the program alive
#    while True:
#        if stop_listening_event.is_set():
#            break

###################################################
def listen_audio(file_path, timeout=30, phrase_time_limit=3, retries=999, energy_threshold=4000, pause_threshold=1, phrase_threshold=0.1, dynamic_energy_threshold=True, calibration_duration=1):
    """
    Record audio from the microphone and save it as an MP3 file.
    
    Args:
    file_path (str): The path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    retries (int): Number of retries if recording fails.
    energy_threshold (int): Energy threshold for considering whether a given chunk of audio is speech or not.
    pause_threshold (float): How much silence the recognizer interprets as the end of a phrase (in seconds).
    phrase_threshold (float): Minimum length of a phrase to consider for recording (in seconds).
    dynamic_energy_threshold (bool): Whether to enable dynamic energy threshold adjustment.
    calibration_duration (float): Duration of the ambient noise calibration (in seconds).
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = energy_threshold
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = phrase_threshold
    recognizer.dynamic_energy_threshold = dynamic_energy_threshold
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                logging.info(Fore.YELLOW+"listening started" + Fore.RESET)
                # Listen for the first phrase and extract it into audio data
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info(Fore.LIGHTGREEN_EX+"listening complete" + Fore.RESET)
                # Convert the recorded audio data to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = pydub.AudioSegment.from_wav(BytesIO(wav_data))
                mp3_data = audio_segment.export(file_path, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                
                
                # Get the API key for transcription
                transcription_api_key = get_transcription_api_key()
                # Transcribe the audio file
                user_input = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.LISTEN_AUDIO, Config.LOCAL_MODEL_PATH)
                # Check if the user wants to exit the program
                print(user_input)

                
                
                if "ivy" in user_input.lower() or "iv" in user_input.lower():
                    logging.info(Fore.BLUE+'Wake up word detected' + Fore.RESET)
                    
                    
                    user_label=Person_classifier(file_path)
                    deepfake_label= detect_fake(file_path)
                        
                        
                    if deepfake_label == "FAKE":
                        Config.deepfake=Config.deepfake+1
                        Config.ivy_deepfake=Config.ivy_deepfake+1
                    if user_label=='Simant(AS3473)':
                        Config.simant=Config.simant+1
                        Config.ivy_simant=Config.ivy_simant+1
                    elif user_label=='Swarali(AS3469)':
                        Config.swarali=Config.swarali+1
                        Config.ivy_swarali=Config.ivy_swarali+1
                    elif user_label=='Aditya(AS3475)':
                        Config.aditya=Config.aditya+1
                        Config.ivy_aditya=Config.ivy_aditya+1

                    if Config.authenticated==False:
                        print('Simant:',Config.simant,' Swarali:',Config.swarali,' Aditya:',Config.aditya)
                        print('IVY Simant:',Config.ivy_simant,' IVY Swarali:',Config.ivy_swarali,' IVY Aditya:',Config.ivy_aditya)
                        print('deepfake or real: ',deepfake_label)
                    #if user_label==Config.User :
                        
                        #logging.info(Fore.LIGHTCYAN_EX+'Welcome '+ user_label.capitalize() + Fore.RESET)
        #            chat_history = [
        #    {"role": "system", "content": """ You are a helpful Assistant called Ivy. 
        #     You are friendly and fun and you will help the users with their requests.
        #     Your answers are short and concise, on point and few worded. Also u generate text as if u are talking, no need of adding special expressions for the users to read and understand the tone and no special symbols too. Talk in a gentle and friendly way. u only generate 4 to 5 word replies. """}
        #]
        #            # Append the user's input to the chat history
        #            chat_history.append({"role": "user", "content": user_input})
        #                # Get the API key for response generation
        #            response_api_key = get_response_api_key()
        #            # Generate a response
        #            response_text = generate_response(Config.RESPONSE_MODEL, response_api_key, chat_history, Config.    LOCAL_MODEL_PATH)
        #            # Append the assistant's response to the chat history
        #            chat_history.append({"role": "assistant", "content": response_text})
        #            # Determine the output file format based on the TTS model
        #            if Config.TTS_MODEL == 'openai' or Config.TTS_MODEL == 'elevenlabs' or Config.TTS_MODEL == 'melotts' or     Config.TTS_MODEL == 'cartesia':
        #                output_file = 'output.mp3'
        #            else:
        #                output_file = 'output.wav'
        #            # Get the API key for TTS
        #            tts_api_key = get_tts_api_key()
        #            # Convert the response text to speech and save it to the appropriate file
        #            text_to_speech(Config.TTS_MODEL, tts_api_key, response_text, output_file, Config.LOCAL_MODEL_PATH)
        #            # Play the generated speech audio
        #            if Config.TTS_MODEL=="cartesia":
        #                pass
        #            else:
        #                play_audio(output_file)
                    
                    return True #, chat_history
                
        except sr.WaitTimeoutError:
            logging.warning(f"Listening timed out, retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")
            break
    else:
        logging.error("Recording failed after all retries")

###################################################
def record_audio(file_path, timeout=10, phrase_time_limit=None, retries=3, energy_threshold=2000, pause_threshold=1, phrase_threshold=0.1, dynamic_energy_threshold=True, calibration_duration=1):
    """
    Record audio from the microphone and save it as an MP3 file.
    
    Args:
    file_path (str): The path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    retries (int): Number of retries if recording fails.
    energy_threshold (int): Energy threshold for considering whether a given chunk of audio is speech or not.
    pause_threshold (float): How much silence the recognizer interprets as the end of a phrase (in seconds).
    phrase_threshold (float): Minimum length of a phrase to consider for recording (in seconds).
    dynamic_energy_threshold (bool): Whether to enable dynamic energy threshold adjustment.
    calibration_duration (float): Duration of the ambient noise calibration (in seconds).
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = energy_threshold
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = phrase_threshold
    recognizer.dynamic_energy_threshold = dynamic_energy_threshold
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                logging.info(Fore.YELLOW+"Calibrating for ambient noise..."  + Fore.RESET)
                recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                logging.info(Fore.RED+"Recording started" + Fore.RESET)
                # Listen for the first phrase and extract it into audio data
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info(Fore.GREEN+"Recording complete" + Fore.RESET)
                # Convert the recorded audio data to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = pydub.AudioSegment.from_wav(BytesIO(wav_data))
                mp3_data = audio_segment.export(file_path, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                file_export='uploads\\'+'Aditya'+timestamp+file_path
                audio_segment.export(file_export, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                return
        except sr.WaitTimeoutError:
            logging.warning(f"Listening timed out, retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")
            break
    else:
        logging.error("Recording failed after all retries")

def play_audio(file_path):
    """
    Play an audio file using pygame.
    
    Args:
    file_path (str): The path to the audio file to play.
    """
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        # Convert the recorded audio data to an MP3 file
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
    except pygame.error as e:
        logging.error(f"Failed to play audio: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while playing audio: {e}")


#RECORD PASSWORD
def record_password(file_path, timeout=20, phrase_time_limit=4, retries=3, energy_threshold=4000, pause_threshold=1, phrase_threshold=0.1, dynamic_energy_threshold=True, calibration_duration=1):
    """
    Record audio from the microphone and save it as an MP3 file.
    
    Args:
    file_path (str): The path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    retries (int): Number of retries if recording fails.
    energy_threshold (int): Energy threshold for considering whether a given chunk of audio is speech or not.
    pause_threshold (float): How much silence the recognizer interprets as the end of a phrase (in seconds).
    phrase_threshold (float): Minimum length of a phrase to consider for recording (in seconds).
    dynamic_energy_threshold (bool): Whether to enable dynamic energy threshold adjustment.
    calibration_duration (float): Duration of the ambient noise calibration (in seconds).
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = energy_threshold
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = phrase_threshold
    recognizer.dynamic_energy_threshold = dynamic_energy_threshold
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                logging.info(Fore.YELLOW+"Calibrating for ambient noise..."  + Fore.RESET)
                recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                logging.info(Fore.BLUE+"Please speak your password clearly..." + Fore.RESET)
                # Listen for the first phrase and extract it into audio data
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info(Fore.GREEN+"Password recording complete" + Fore.RESET)
                # Convert the recorded audio data to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = pydub.AudioSegment.from_wav(BytesIO(wav_data))
                mp3_data = audio_segment.export(file_path, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                #timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_segment.export(file_path, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                
                return
        except sr.WaitTimeoutError:
            logging.warning(f"Listening timed out, retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")
            break
    else:
        logging.error("Recording failed after all retries")

def record_userid(file_path, timeout=20, phrase_time_limit=4, retries=3, energy_threshold=2000, pause_threshold=1, phrase_threshold=0.1, dynamic_energy_threshold=True, calibration_duration=1):
    """
    Record audio from the microphone and save it as an MP3 file.
    
    Args:
    file_path (str): The path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    retries (int): Number of retries if recording fails.
    energy_threshold (int): Energy threshold for considering whether a given chunk of audio is speech or not.
    pause_threshold (float): How much silence the recognizer interprets as the end of a phrase (in seconds).
    phrase_threshold (float): Minimum length of a phrase to consider for recording (in seconds).
    dynamic_energy_threshold (bool): Whether to enable dynamic energy threshold adjustment.
    calibration_duration (float): Duration of the ambient noise calibration (in seconds).
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = energy_threshold
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = phrase_threshold
    recognizer.dynamic_energy_threshold = dynamic_energy_threshold
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                logging.info(Fore.YELLOW+"Calibrating for ambient noise..."  + Fore.RESET)
                recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                logging.info(Fore.BLUE+"Please speak your ID clearly..." + Fore.RESET)
                # Listen for the first phrase and extract it into audio data
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info(Fore.GREEN+"ID recording complete" + Fore.RESET)
                # Convert the recorded audio data to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = pydub.AudioSegment.from_wav(BytesIO(wav_data))
                mp3_data = audio_segment.export(file_path, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                #timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_segment.export(file_path, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])

                return
            
        except sr.WaitTimeoutError:
            logging.warning(f"Listening timed out, retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")
            break
    else:
        logging.error("Recording failed after all retries")

def record_satisfaction(file_path, timeout=15, phrase_time_limit=2, retries=3, energy_threshold=4000, pause_threshold=1, phrase_threshold=0.1, dynamic_energy_threshold=True, calibration_duration=1):

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = energy_threshold
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = phrase_threshold
    recognizer.dynamic_energy_threshold = dynamic_energy_threshold
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                logging.info(Fore.YELLOW+"Calibrating for ambient noise..."  + Fore.RESET)
                recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                logging.info(Fore.WHITE+"Please say " + Fore.BLUE + "yes" + Fore.WHITE + " or" + Fore.BLUE + " no..." + Fore.RESET)
                # Listen for the first phrase and extract it into audio data
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info(Fore.GREEN+"recording complete" + Fore.RESET)
                # Convert the recorded audio data to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = pydub.AudioSegment.from_wav(BytesIO(wav_data))
                mp3_data = audio_segment.export(file_path, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                #timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_segment.export(file_path, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
                return
        except sr.WaitTimeoutError:
            logging.warning(f"Listening timed out, retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")
#import sounddevice as sd
#import soundfile as sf
#import simpleaudio as sa
#import logging
# 
#def record_audio(file_path, timeout=10, phrase_time_limit=None, retries=3, energy_threshold=2000, pause_threshold=1, #hrase_threshold=0.1, dynamic_energy_threshold=True, calibration_duration=1):
#    """
#    Record audio from the microphone and save it as a WAV file.
#   
#    Args:
#    file_path (str): The path to save the recorded audio file.
#    timeout (int): Maximum time to wait for a phrase to start (in seconds).
#    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
#    retries (int): Number of retries if recording fails.
#    energy_threshold (int): Energy threshold for considering whether a given chunk of audio is speech or not.
#    pause_threshold (float): How much silence the recognizer interprets as the end of a phrase (in seconds).
#    phrase_threshold (float): Minimum length of a phrase to consider for recording (in seconds).
#    dynamic_energy_threshold (bool): Whether to enable dynamic energy threshold adjustment.
#    calibration_duration (float): Duration of the ambient noise calibration (in seconds).
#    """
#    for attempt in range(retries):
#        try:
#            logging.info("Recording started")
#            sample_rate = 44100  # Define sample rate
#            duration = timeout + (phrase_time_limit if phrase_time_limit else 0)
#            audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
#            sd.wait()  # Wait until recording is finished
#            logging.info("Recording complete")
#           
#            # Save the recorded audio data to a WAV file
#            sf.write(file_path, audio_data, sample_rate, format='WAV', subtype='PCM_16')
#            logging.info(f"Audio successfully saved to {file_path}")
#            return
#        except Exception as e:
#            logging.error(f"Failed to record audio: {e}")
#   
#    logging.error("Recording failed after all retries")
# 
#def play_audio(file_path):
#    """
#    Play an audio file using simpleaudio.
#   
#    Args:
#    file_path (str): The path to the audio file to play.
#    """
#    try:
#        wave_obj = sa.WaveObject.from_wave_file(file_path)
#        play_obj = wave_obj.play()
#        play_obj.wait_done()
#    except Exception as e:
#        logging.error(f"Failed to play audio: {e}")
# 
## Example usage
#if __name__ == "__main__":
#    logging.basicConfig(level=logging.INFO)
#    record_audio('test.wav', timeout=5)
#    play_audio('test.wav')
 
 