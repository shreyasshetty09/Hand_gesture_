import cv2
import numpy as np

class Button:
    def __init__(self, x, y, w, h, value, 
                 font=cv2.FONT_HERSHEY_COMPLEX, 
                 operator_color=(0,0,0),  # Default operator color
                 operand_color=(102, 102, 0),
                 font_color=(0, 0, 0), 
                 thick=2, font_size=1.5, circular=True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.value = value
        self.circular = circular
        
        self.font = font
        self.font_color = font_color
        self.thick = thick
        self.font_size = font_size
        self.operator_color = operator_color  # Assigning operator color here
        self.operand_color = operand_color
        
        self.text_width, self.text_height = cv2.getTextSize(self.value, self.font, self.font_size, self.thick)[0]
    
    def draw(self, img):
        if self.value == 'CLEAR':
            # Draw rounded rectangular button for CLEAR
            radius = 20
            cv2.rectangle(img, (self.x + radius, self.y), (self.x + self.w - radius, self.y + self.h), self.operand_color, cv2.FILLED)
            cv2.rectangle(img, (self.x, self.y + radius), (self.x + self.w, self.y + self.h - radius), self.operand_color, cv2.FILLED)
            cv2.rectangle(img, (self.x + radius, self.y), (self.x + self.w - radius, self.y + self.h), (255, 255, 255), 3)
            cv2.rectangle(img, (self.x, self.y + radius), (self.x + self.w, self.y + self.h - radius), (255, 255, 255), 3)
        else:
            # Draw regular button
            if self.circular:
                # Draw circular button
                radius = min(self.w, self.h) // 2
                center = (self.x + self.w // 2, self.y + self.h // 2)
                cv2.circle(img, center, radius, self.operand_color, cv2.FILLED)
                cv2.circle(img, center, radius, (255, 255, 255), 3)
            else:
                # Draw rectangular button
                cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), self.operand_color, cv2.FILLED)
                cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 255, 255), 3)
                cv2.rectangle(img, (self.x + 5, self.y + 5), (self.x + self.w - 5, self.y + self.h - 5), (255, 255, 255), cv2.FILLED)
        
        # Put text on button
        if self.value in ['+', '-', '*', '/', '^', '=']:
            text_color = self.operator_color  # Use operator color for operators
        else:
            text_color = self.font_color
        text_x = self.x + 10    
        cv2.putText(img, self.value, 
                    (self.x + (self.w - self.text_width) // 2, 
                     self.y + (self.h + self.text_height) // 2),
                    self.font, self.font_size, text_color, self.thick)
        
        return img
    
    def check_click(self, img, dist, x1, y1):
        if (self.x <= x1 <= self.x + self.w) and (self.y <= y1 <= self.y + self.h) and dist <= 50:
            if self.value == 'CLEAR':
                # Highlight rounded rectangular button when clicked
                radius = 20
                cv2.rectangle(img, (self.x + radius, self.y), (self.x + self.w - radius, self.y + self.h), (0, 255, 0), cv2.FILLED)
                cv2.rectangle(img, (self.x, self.y + radius), (self.x + self.w, self.y + self.h - radius), (0, 255, 0), cv2.FILLED)
                cv2.rectangle(img, (self.x + radius, self.y), (self.x + self.w - radius, self.y + self.h), (255, 255, 255), 3)
                cv2.rectangle(img, (self.x, self.y + radius), (self.x + self.w, self.y + self.h - radius), (255, 255, 255), 3)
            else:
                if self.circular:
                    # Highlight circular button when clicked
                    radius = min(self.w, self.h) // 2
                    center = (self.x + self.w // 2, self.y + self.h // 2)
                    cv2.circle(img, center, radius, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, center, radius, (255, 255, 255), 3)
                else:
                    # Highlight rectangular button when clicked
                    cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), cv2.FILLED)
                    cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 255, 255), 3)
                    cv2.rectangle(img, (self.x + 5, self.y + 5), (self.x + self.w - 5, self.y + self.h - 5), (255, 255, 255), cv2.FILLED)
            
            if self.value in ['+', '-', '*', '/', '^', '=', '(', ')']:
                text_color = self.operator_color
            else:
                text_color = self.font_color
            
            cv2.putText(img, self.value, 
                        (self.x + (self.w - self.text_width) // 2, 
                         self.y + (self.h + self.text_height) // 2),
                        self.font, self.font_size, text_color, self.thick)
            return True
        return False

def draw_rounded_rectangle(img, pt1, pt2, color, thickness, radius):
    x1, y1 = pt1
    x2, y2 = pt2
    cv2.rectangle(img, (x1 + radius, y1), (x2 - radius, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + radius), (x2, y2 - radius), color, thickness)

def draw_calculator(img):
    button_list_values = [['7', '8', '9', '^', '('],
                          ['4', '5', '6', '*', ')'],
                          ['1', '2', '3', '-', 'DEL'],
                          ['0', '.', '/', '+', '=']]
    button_list = []
    start_x, start_y = 600, 130
    button_size = 110
    
    for i in range(4):
        for j in range(5):
            if button_list_values[i][j] in ['+', '-', '*', '/', '^', '(', ')', '=']:
                button_list.append(Button(start_x + button_size * j, start_y + button_size * i, button_size, button_size, button_list_values[i][j], operator_color=(100, 0, 0)))  # Blood red color (BGR)
            else:
                button_list.append(Button(start_x + button_size * j, start_y + button_size * i, button_size, button_size, button_list_values[i][j], operand_color=(150, 150, 150)))  # Grey color
    
    # Clear button as rounded rectangular shape
    clear_button_width = button_size * 2
    clear_button_height = button_size
    clear_button_x = start_x + 3 * button_size
    clear_button_y = start_y + 4 * button_size
    button_list.append(Button(clear_button_x, clear_button_y, clear_button_width, clear_button_height, 'CLEAR', circular=False, operand_color=(150, 150, 150)))  # Grey color
    
    for button in button_list:
        img = button.draw(img)
    
    # Draw background rectangle for buttons
    background_color = (50, 50, 50)
    border_color = (255, 255, 255)
    border_thickness = 3
    border_radius = 20
    
    background_pt1 = (start_x, start_y - 100)
    background_pt2 = (start_x + 5 * button_size, start_y)
    draw_rounded_rectangle(img, background_pt1, background_pt2, background_color, cv2.FILLED, border_radius)
    draw_rounded_rectangle(img, background_pt1, background_pt2, border_color, border_thickness, border_radius)
    
    return img, button_list

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    # Assuming Tracker class is defined elsewhere
    tracker = Tracker()
    
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = tracker.hand_landmark(img)
        img, button_list = draw_calculator(img)
        img, dist, x1, y1 = tracker.tracking(img)
        
        for button in button_list:
            if button.check_click(img, dist, x1, y1):
                print(f'Clicked: {button.value}')
                # Add logic for button functionality here
        
        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()