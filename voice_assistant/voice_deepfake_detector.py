# voice_assistant/deepfake_detector.py

import numpy as np
import librosa
import joblib

# Load the pre-trained model
model_path = r'C:\Users\simant.asawale\Desktop\POC1-NEW\Verbi\deepfake model\deepfake_classification.joblib'
model = joblib.load(model_path)

def detect_fake(filename):
    sound_signal, sample_rate = librosa.load(filename, res_type="kaiser_fast")
    mfcc_features = librosa.feature.mfcc(y=sound_signal, sr=sample_rate, n_mfcc=40)
    mfccs_features_scaled = np.mean(mfcc_features.T, axis=0)
    mfccs_features_scaled = mfccs_features_scaled.reshape(1, -1)
    result_array = model.predict(mfccs_features_scaled)
    result_classes = ["FAKE", "REAL"]
    result = np.argmax(result_array[0])
    return result_classes[result]
