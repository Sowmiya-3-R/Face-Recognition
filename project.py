import cv2
from fer import FER
import time

# Initialize detector
detector = FER(mtcnn=True)

# Desired emotion to unlock
AUTHORIZED_EMOTION = "happy"

# Start webcam
cap = cv2.VideoCapture(0)

is_unlocked = False

print("Smart Lock is active. Show emotion to unlock...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = detector.detect_emotions(frame)

    for result in results:
        (x, y, w, h) = result["box"]
        emotions = result["emotions"]
        dominant_emotion = max(emotions, key=emotions.get)

        # Draw face and emotion
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"{dominant_emotion}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        # Unlock logic
        if dominant_emotion == AUTHORIZED_EMOTION and emotions[dominant_emotion] > 0.9:
            if not is_unlocked:
                print("🔓 Lock opened! Welcome.")
                is_unlocked = True
                cv2.putText(frame, "LOCK OPENED", (x, y + h + 30),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
                # Simulate lock open time
                time.sleep(3)
        else:
            is_unlocked = False

    # Display frame
    cv2.imshow("Emotion Smart Lock", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
