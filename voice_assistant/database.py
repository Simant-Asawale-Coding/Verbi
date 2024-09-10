import sqlite3
import hashlib
from voice_assistant.audio import record_password, record_userid
from voice_assistant.transcription import transcribe_audio
from voice_assistant.api_key_manager import get_transcription_api_key
from voice_assistant.config import Config
import string

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table for users if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY, 
                    password TEXT)''')

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to register new user
def register_user():
    print('please enter your USER ID: ')
    record_userid(Config.USER_LOCAL)
    # Get the API key for transcription
    transcription_api_key = get_transcription_api_key()
    # Transcribe the audio file
    user_id = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.USER_LOCAL, Config.LOCAL_MODEL_PATH)
    user_id = user_id.translate(str.maketrans('', '', string.punctuation)).replace(" ", "").upper()
    print('This is how your USER ID looks: ', user_id)

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        print("User ID already exists. Try logging in.")
        return
    else:
        #password = input("Set a password: ")
        print('please set your password: ')
        record_password(Config.PASSWORD_LOCAL)
       
        # Transcribe the audio file
        user_password = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.PASSWORD_LOCAL, Config.LOCAL_MODEL_PATH)
        user_password = user_password.translate(str.maketrans('', '', string.punctuation)).replace(" ", "").lower()
        print('This is how your password looks: ', user_password)
        hashed_password = hash_password(user_password)
        cursor.execute("INSERT INTO users (user_id, password) VALUES (?, ?)", (user_id, hashed_password))
        conn.commit()
        print("Registration successful! You can now log in.")
        return True
            
        
        

# Function to authenticate existing user
def authenticate_user():
    print('please speak your USER ID next: ')
    record_userid(Config.USER_LOCAL)
    # Get the API key for transcription
    transcription_api_key = get_transcription_api_key()
    # Transcribe the audio file
    user_id = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.USER_LOCAL, Config.LOCAL_MODEL_PATH)
    user_id = user_id.translate(str.maketrans('', '', string.punctuation)).replace(" ", "").upper()
    print('This is how your USER ID looks: ', user_id)


    record_password(Config.PASSWORD_LOCAL)
    # Transcribe the audio file
    user_password = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.PASSWORD_LOCAL, Config.LOCAL_MODEL_PATH)
    user_password = user_password.translate(str.maketrans('', '', string.punctuation)).replace(" ", "").lower()
    print('This is how your password looks: ', user_password)
    
    hashed_password = hash_password(user_password)
    
    cursor.execute("SELECT * FROM users WHERE user_id = ? AND password = ?", (user_id, hashed_password))
    if cursor.fetchone():
        print(f"Welcome back, {user_id}!")
        # Proceed to run the voice assistant functionality
        return True
    else:
        print("Authentication failed. Invalid username or password.")
        return False

# Function to check if the user is registered
def login_or_register():
    choice = input("Are you a registered user? (yes/no): ").lower()
    
    if choice == 'no':
        registered=register_user()
        if registered==True:
            authenticated=authenticate_user()
            if authenticated==True:
                return True
            else:
                return False
        else:
            
            return False
        
    elif choice == 'yes':

        authenticated=authenticate_user()
        if authenticated==True:
            return True
        else:
            return False
    else:
        print("Invalid choice. Please enter 'yes' or 'no'.")
        login_or_register()



# Close database connection when done
def close_connection():
    conn.close()

