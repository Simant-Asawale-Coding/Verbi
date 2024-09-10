import joblib
import tensorflow
import librosa
import numpy as np
from tensorflow.keras.models import load_model

#def Person_classifier(path_to_audio):
#
#    model = joblib.load(r"C:\Users\simant.asawale\Desktop\POC1-NEW\Verbi\classifying_model\audio_classification_nb.pkl")
#    encoder = joblib.load(r"C:\Users\simant.asawale\Desktop\POC1-NEW\Verbi\classifying_model\label_encoder.pkl")
#    # Path to your audio file
#    filename = path_to_audio
#    
#    
#    
#    # Load audio file and extract features
#    audio, sample_rate = librosa.load(filename, sr=None, res_type='kaiser_fast')
#    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
#    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
#    
#    
#    # Reshape features for prediction
#    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
#    
#    
#    # Make a prediction
#    predictions = model.predict(mfccs_scaled_features)
#    predicted_class_index = np.argmax(predictions, axis=0)
#    prediction=encoder.inverse_transform(predicted_class_index)
#    return prediction

model = joblib.load(r"C:\Users\simant.asawale\Desktop\POC1-NEW\Verbi\classifying_model\final_audio_classification_nb.pkl")
encoder = joblib.load(r"C:\Users\simant.asawale\Desktop\POC1-NEW\Verbi\classifying_model\final_label_encoder.pkl")

def Person_classifier(path_to_audio):

   
    
    filename = path_to_audio
 
    # Load audio file and extract features
    audio, sample_rate = librosa.load(filename, sr=None, res_type='kaiser_fast')
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    
    # Check the shape of the features
    print("Feature shape:", mfccs_scaled_features.shape)
    
    # Reshape features for prediction
    mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)
    
    # Check the shape of the reshaped features
    #print("Reshaped feature shape for prediction:", mfccs_scaled_features.shape)
    
    ######below code for naive bayes model
    # Make a prediction
    predictions = model.predict(mfccs_scaled_features)
    
    # Check the predictions
    #print("Predictions shape:", predictions.shape)
    #print("Predictions:", predictions)
    
    # Convert prediction to label
    predicted_label = encoder.inverse_transform(predictions)
    
    print("Predicted Label:", predicted_label)
    print('from labels: ', predicted_label[0])

    return predicted_label[0]


###### below code for keras model
    #predictions = model.predict(mfccs_scaled_features)
#
    ## Check the predictions
    #print("Predictions shape:", predictions.shape)
    #print("Predictions:", predictions)
#
    ## Convert prediction probabilities to class indices
    #predicted_class_index = np.argmax(predictions, axis=1)
#
    ## Convert class index to label
    #predicted_label = encoder.inverse_transform(predicted_class_index)
#
    #print("Predicted Label:", predicted_label)
#
    #return predicted_label
