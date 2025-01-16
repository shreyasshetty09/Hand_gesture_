import cv2
import mediapipe as mp
import numpy as np

class Tracker:
    def __init__(self, static_image_mode=False, max_num_hands=1, 
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.hands = mp.solutions.hands.Hands(static_image_mode=self.static_image_mode,
                                              max_num_hands=self.max_num_hands,
                                              min_detection_confidence=self.min_detection_confidence,
                                              min_tracking_confidence=self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils

    def hand_landmark(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
        return img

    def detect_gestures(self, img):
        h, w, c = img.shape
        led_bulbs = np.zeros((100, 400, 3), dtype=np.uint8)  # LED bulbs area
        led_bulbs[:, :] = (50, 50, 50)  # Dim state for LEDs

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]
                middle_tip = hand_landmarks.landmark[12]
                ring_tip = hand_landmarks.landmark[16]
                pinky_tip = hand_landmarks.landmark[20]

                thumb_y = int(thumb_tip.y * h)
                index_y = int(index_tip.y * h)
                middle_y = int(middle_tip.y * h)
                ring_y = int(ring_tip.y * h)
                pinky_y = int(pinky_tip.y * h)

                # Gesture logic
                text = ""
                led_color = (50, 50, 50)  # Default LED color

                if thumb_y < index_y and thumb_y < middle_y and thumb_y < ring_y and thumb_y < pinky_y:
                    text = "Thumbs Up!"
                    led_color = (0, 255, 0)  # Green LEDs
                elif thumb_y > index_y and thumb_y > middle_y and thumb_y > ring_y and thumb_y > pinky_y:
                    text = "Thumbs Down!"
                    led_color = (0, 0, 255)  # Red LEDs
                elif index_y < thumb_y and middle_y < thumb_y and ring_y > thumb_y and pinky_y > thumb_y:
                    text = "Scissors!"
                    led_color = (255, 255, 0)  # Yellow LEDs

                if text:
                    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 2, 3)[0]
                    text_x = (w - text_size[0]) // 2
                    text_y = (h + text_size[1]) // 2
                    cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
                    cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

                    led_bulbs[:, :] = led_color

        return img, led_bulbs

    def enhance_image(self, img):
        # Convert to YUV and equalize histogram for better light distribution
        yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
        img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

        # Apply GaussianBlur for noise reduction
        img = cv2.GaussianBlur(img, (5, 5), 0)
        return img

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    
    # Set resolution to 4K
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    
    tracker = Tracker()

    while True:
        success, img = cap.read()
        if not success:
            break

        # Enhance the captured image
        img = tracker.enhance_image(img)
        img = tracker.hand_landmark(img)
        img, led_bulbs = tracker.detect_gestures(img)

        # Combine LED display and video feed
        combined_img = np.hstack((img, cv2.resize(led_bulbs, (640, img.shape[0]))))

        # Add overlay for context
        cv2.putText(combined_img, "Gesture Tracker - 4K Ultra HD", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Display in full screen
        cv2.namedWindow("Gesture Tracker", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Gesture Tracker", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Gesture Tracker", combined_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
