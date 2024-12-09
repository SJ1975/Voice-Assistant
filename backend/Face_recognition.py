import face_recognition
import cv2
# Define a function for face recognition
def recognize_face():
    # Load a sample picture and learn how to recognize it.
    known_image = face_recognition.load_image_file("backend/JayNew.jpeg")  # Replace "your_image.jpg" with the path to your image
    known_encoding = face_recognition.face_encodings(known_image)[0]

    # Initialize webcam
    webcam = cv2.VideoCapture(0)

    # Check if webcam is opened
    if not webcam.isOpened():
        print("Error: Could not open webcam")
        return False

    while True:
        # Capture frame-by-frame
        ret, frame = webcam.read()

        # Find all face locations and face encodings in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Check if any face is detected
        if len(face_encodings) > 0:
            # Compare the detected face with the known face
            match = face_recognition.compare_faces([known_encoding], face_encodings[0])

            if match[0]:
                print("Face recognized.")
                return True

        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release webcam
    webcam.release()
    cv2.destroyAllWindows()
    return False

# Call the face recognition function before starting the main loop
if recognize_face():
    # Start the main loop
    print("Starting the assistant...")

    # Add your main loop code here
    # The main loop will only start if your face is detected or identified
else:
    print("Face not recognized. Exiting the program.")
