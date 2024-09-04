 #voice_assistant/audio.py
import speech_recognition as sr
import pygame
import time
import logging
import pydub
from io import BytesIO
from pydub import AudioSegment

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
                logging.info("Calibrating for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=calibration_duration)
                logging.info("Recording started")
                # Listen for the first phrase and extract it into audio data
                audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info("Recording complete")
                # Convert the recorded audio data to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = pydub.AudioSegment.from_wav(BytesIO(wav_data))
                mp3_data = audio_segment.export(file_path, format="WAV", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
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
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
    except pygame.error as e:
        logging.error(f"Failed to play audio: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while playing audio: {e}")

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
 
 