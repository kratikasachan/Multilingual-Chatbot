import cv2
import face_recognition
import wikipedia

# Function to fetch information about a monument from Wikipedia
def get_monument_info(monument_name):
    try:
        summary = wikipedia.summary(monument_name)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found, please specify further: {e.options}"
    except wikipedia.exceptions.HTTPTimeoutError:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"An error occurred: {e}"

# Function to detect user with face recognition
def detect_user():
    # Open a video capture object
    video_capture = cv2.VideoCapture(0)
    
    # Loop until a face is detected
    while True:
        ret, frame = video_capture.read()
        if not ret:
            continue
        
        # Convert the frame from BGR to RGB (required by face_recognition)
        rgb_frame = frame[:, :, ::-1]
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)

        if face_locations:
            print("Hello, welcome to the museum!")
            break
        
        # Show the video feed for user detection
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close window
    video_capture.release()
    cv2.destroyAllWindows()

# Main Program
if __name__ == "__main__":
    # Greet the user
    print("Welcome to the Museum Voice Assistant!")
    
    # Detect the user via webcam (using face detection)
    detect_user()

    # Ask the user for a monument name
    monument_name = input("Enter the name of the monument: ")

    if monument_name:
        # Fetch information about the monument from Wikipedia
        info = get_monument_info(monument_name)
        print(info)
