import pytesseract
import cv2


def get_text(image_path, coordinates):
    image = cv2.imread(image_path)

    # cropping image img = image[y0:y1, x0:x1]
    image_ROI = image[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]

    # pytesseract image to string to get results
    text = str(pytesseract.image_to_string(image_ROI, config='--psm 6'))

    return text


def process_image(image_path, selection_set):

    im = cv2.imread(image_path)
    ret,im = cv2.threshold(im,120,255,cv2.THRESH_BINARY)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)

    # Dilate to combine adjacent text contours
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    tags_list = dict()

    for selection in selection_set.keys():
        coordinates = selection_set[selection]
        print("coordinates for ", selection, " is ", coordinates)
        text = get_text(image_path, coordinates)
        tags_list[selection] = text

    print("tags list is:", tags_list)
