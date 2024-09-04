import joblib
import tensorflow
import librosa
import numpy as np
from tensorflow.keras.models import load_model

def Person_classifier(path_to_audio):

    model = load_model(r"C:\Users\simant.asawale\Desktop\POC1-NEW\Verbi\classifying_model\audio_classification.keras")
    encoder = joblib.load(r"C:\Users\simant.asawale\Desktop\POC1-NEW\Verbi\classifying_model\label_encoder.pkl")
    # Path to your audio file
    filename = path_to_audio
    
    
    
    # Load audio file and extract features
    audio, sample_rate = librosa.load(filename, sr=None, res_type='kaiser_fast')
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    
    
    # Reshape features for prediction
    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
    
    
    # Make a prediction
    predictions = model.predict(mfccs_scaled_features)
    predicted_class_index = np.argmax(predictions, axis=1)
    prediction=encoder.inverse_transform(predicted_class_index)
    return prediction
