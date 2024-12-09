import cv2
from tensorflow.keras.models import load_model
import numpy as np

# Load pre-trained Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load pre-trained CNN model for emotion recognition
emotion_model = load_model('emotion_detection_model.h5')  # Path to your pre-trained emotion detection model

# Define emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']


# Function to detect face and emotions
def detect_face_and_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Resize the image to the input size of the model
        roi_gray_resized = cv2.resize(roi_gray, (48, 48))
        roi_gray_resized = np.expand_dims(roi_gray_resized, axis=-1)
        roi_gray_resized = np.expand_dims(roi_gray_resized, axis=0)

        # Predict emotion
        predicted_emotion = np.argmax(emotion_model.predict(roi_gray_resized))

        # Draw rectangle and print emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, emotion_labels[predicted_emotion], (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame


# Main function for capturing video from webcam
def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame = detect_face_and_emotion(frame)
        cv2.imshow('Emotion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
