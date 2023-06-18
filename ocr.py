import cv2
import pytesseract
import numpy as np
# Set the Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


min_area_threshold = 100  # Adjust this value based on your specific requirements

# Apply preprocessing techniques to the ROI
def preprocess_roi(roi):
    # Convert ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply background subtraction to separate foreground (text) from background
    fgbg = cv2.createBackgroundSubtractorMOG2()
    mask = fgbg.apply(gray_roi)
    
    # Apply contour analysis to detect and filter out unwanted objects
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_mask = np.zeros_like(mask)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area_threshold:  # Set a suitable minimum area threshold
            cv2.drawContours(filtered_mask, [contour], -1, 255, thickness=cv2.FILLED)
    
    # Apply the filtered mask to the original ROI
    masked_roi = cv2.bitwise_and(gray_roi, filtered_mask)
    
    # Apply adaptive thresholding to enhance contrast
    _, thresholded_roi = cv2.threshold(masked_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Apply morphological operations (e.g., erosion and dilation) to improve text extraction
    kernel = np.ones((3, 3), np.uint8)
    processed_roi = cv2.erode(thresholded_roi, kernel, iterations=1)
    processed_roi = cv2.dilate(processed_roi, kernel, iterations=1)
    
    return processed_roi

def extract(frame):

        # Determine the region of interest (bottom right corner)
        height, width = frame.shape[:2]
        print(height, width)
        bottom_right_x = width
        bottom_right_y = height
        roi = frame[bottom_right_y-70:bottom_right_y, bottom_right_x-250:bottom_right_x]

        # Example usage
        # Assuming 'roi' contains the selected region of interest as a numpy array (BGR image)
        processed_roi = preprocess_roi(roi)
        #cv2.imshow("Processed ROI", processed_roi)

        extracted_text = ""
        # Perform OCR on the extracted region
        extracted_text = pytesseract.image_to_string(processed_roi)

        extracted_text = extracted_text.replace('\n', ' ')
        extracted_text = extracted_text.replace('"', '').replace("'", "")


        print("Extracted date:", extracted_text)
        return extracted_text



# video_path = r"C:\Users\DELL\Desktop\Videos\test3.MP4"
# cap = cv2.VideoCapture(video_path)
# while True:
#         # Read a frame from the video
#         ret, frame = cap.read()

#         # Break the loop if the video has ended
#         if not ret:
#             break
#         extract(frame)