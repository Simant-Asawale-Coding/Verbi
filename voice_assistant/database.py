import sqlite3
import hashlib
from voice_assistant.audio import record_password, record_userid, record_satisfaction
from voice_assistant.transcription import transcribe_audio
from voice_assistant.api_key_manager import get_transcription_api_key
from voice_assistant.config import Config
from voice_assistant.person_classifier import Person_classifier
import string



# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users_new.db')
cursor = conn.cursor()

# Create table for users_new if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users_new (
                    user_id TEXT PRIMARY KEY,user_name TEXT, 
                    password TEXT)''')

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Function for recording user id
def record_user_id():
    registered_user=False
    while not registered_user:
        
        print('please speak your USER ID: ')
        record_userid(Config.USER_LOCAL)
        # Get the API key for transcription
        transcription_api_key = get_transcription_api_key()
        # Transcribe the audio file
        user_id = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.USER_LOCAL, Config.    LOCAL_MODEL_PATH)
        user_id = user_id.translate(str.maketrans('', '', string.punctuation)).replace(" ", "").upper()
        print('This is how your USER ID looks: ', user_id)
        user_id_flag=user_satisfaction()
        if user_id_flag==False:
            registered_user=False
        else:
            registered_user=True
    
    return user_id

def record_user_name():
    user_name_recorder=False
    while not user_name_recorder:
        user_name=input('Please enter your name: ')
        user_name=user_name.lower().capitalize()    
        print('This is how your name looks: ', user_name)
        user_name_satisfaction=user_satisfaction()
        if user_name_satisfaction==False:
            user_name_recorder=False
        else:
            user_name_recorder=True
    return user_name
        

def record_user_password():
    registered_password=False
    while not registered_password:
        
        #password = input("Set a password: ")
        print('please speak your password: ')
        record_password(Config.PASSWORD_LOCAL)
        # Get the API key for transcription
        transcription_api_key = get_transcription_api_key()
        # Transcribe the audio file
        user_password = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.PASSWORD_LOCAL, Config.LOCAL_MODEL_PATH)
        user_password = user_password.translate(str.maketrans('', '', string.punctuation)).replace(" ", "").lower()
        print('This is how your password looks: ', user_password)
        user_password_flag=user_satisfaction()

        if user_password_flag== False:
            registered_password=False
        else:
            registered_password=True
    
    return user_password

def user_satisfaction():
    print('is it correct?')
    record_satisfaction(Config.SATISFACTION_LOCAL)
    transcription_api_key = get_transcription_api_key()
    # Transcribe the audio file
    user_response = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.SATISFACTION_LOCAL, Config.LOCAL_MODEL_PATH)
    if 'yes' in user_response.lower():
        print('YES')
        return True
    else:
        print('NO')
        return False
    
def user_satisfaction2():
    print('are you a registered user?')
    record_satisfaction(Config.SATISFACTION_LOCAL)
    transcription_api_key = get_transcription_api_key()
    # Transcribe the audio file
    user_response = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.SATISFACTION_LOCAL, Config.LOCAL_MODEL_PATH)
    if 'yes' in user_response.lower():
        print('YES')
        return True
    else:
        print('NO')
        return False

# Function to register new user
def register_user():
    #print('please enter your USER ID: ')
    #record_userid(Config.USER_LOCAL)
    ## Get the API key for transcription
    #transcription_api_key = get_transcription_api_key()
    ## Transcribe the audio file
    #user_id = transcribe_audio(Config.TRANSCRIPTION_MODEL, transcription_api_key, Config.USER_LOCAL, Config.#LOCAL_MODEL_PATH)
    #user_id = user_id.translate(str.maketrans('', '', string.punctuation)).replace(" ", "").upper()
    #print('This is how your USER ID looks: ', user_id)
    
    user_id=record_user_id()
    user_name=record_user_name()
    user_name=user_name+'('+user_id+')'
    cursor.execute("SELECT * FROM users_new WHERE user_id = ?", (user_id,))
    if cursor.fetchone():
        print("User ID already exists. Try logging in.")
        return False    
    else:
        user_password=record_user_password()
        hashed_password = hash_password(user_password)
        cursor.execute("INSERT INTO users_new (user_id,user_name,password) VALUES (?, ?, ?)", (user_id, user_name, hashed_password))
        conn.commit()
        print("Registration successful! You can now log in.")
        return True
            
        
        

# Function to authenticate existing user
def authenticate_user():
    user_id=record_user_id()
    user_label=Person_classifier(Config.USER_LOCAL)
    if user_label=='Simant(AS3473)':
        Config.simant=Config.simant+1
    elif user_label=='Swarali(AS3469)':
        Config.swarali=Config.swarali+1
    elif user_label=='Aditya(AS3475)':
        Config.aditya=Config.aditya+1
    print('Simant:',Config.simant,' Swarali:',Config.swarali,' Aditya:',Config.aditya)

    


    user_password=record_user_password()
    user_label=Person_classifier(Config.PASSWORD_LOCAL)
    if user_label=='Simant(AS3473)':
        Config.simant=Config.simant+1
    elif user_label=='Swarali(AS3469)':
        Config.swarali=Config.swarali+1
    elif user_label=='Aditya(AS3475)':
        Config.aditya=Config.aditya +1
    print('Simant:',Config.simant,' Swarali:',Config.swarali,' Aditya:',Config.aditya)
    
    
    hashed_password = hash_password(user_password)
    user_name_verification = cursor.execute("SELECT user_name FROM users_new WHERE user_id = ? AND password = ?", (user_id, hashed_password,)).fetchone()
    print(user_name_verification[0])
    cursor.execute("SELECT * FROM users_new WHERE user_id = ? AND password = ?", (user_id,hashed_password,))
    if cursor.fetchone():
        if Config.simant >=2:
            Config.user_id='Simant(AS3473)'
            if user_name_verification[0]==Config.user_id:
                print(f"Welcome back, {user_id}!")
                # Proceed to run the voice assistant functionality
                return True
            else:
                print('Sorry you are not ',user_name_verification[0],'. Please try again.')
                return False

        elif Config.swarali >=2:
            Config.user_id='Swarali(AS3469)'
            if user_name_verification[0]==Config.user_id:
                print(f"Welcome back, {user_id}!")
                # Proceed to run the voice assistant functionality
                return True
            else:
                print('Sorry you are not ',user_name_verification[0],'. Please try again.')
                return False
        elif Config.aditya >=2:
            Config.user_id='Aditya(AS3475)'
            if user_name_verification[0]==Config.user_id:
                print(f"Welcome back, {user_id}!")
                # Proceed to run the voice assistant functionality
                return True
            else:
                print('Sorry you are not ',user_name_verification[0],'. Please try again.')
                return False
        else:
            return False
    else:
        print("Authentication failed. Invalid username or password.")
        return False

# Function to check if the user is registered
def login_or_register():
    choice = user_satisfaction2()
    
    if choice == False:
        #registered=register_user()
        #if registered==True:
        #    authenticated=authenticate_user()
        #    if authenticated==True:
        #        return True
        #    else:
        #        return False
        #else:
        registered=False
        while not registered:
            registered=register_user()
            
        authenticated=False
        while not authenticated:
            authenticated=authenticate_user()
            
        return True
        
    elif choice == True:

        #authenticated=authenticate_user()
        #if authenticated==True:
        #    return True
        #else:
        #    return False
        authenticated=False
        while not authenticated:
            authenticated=authenticate_user()
            
        return True
    else:
        print("Invalid choice. Please select 'yes' or 'no'.")
        login_or_register()



# Close database connection when done
def close_connection():
    conn.close()

