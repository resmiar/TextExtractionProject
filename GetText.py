import pytesseract
import cv2


def get_text(image_path, coordinates):
    image = cv2.imread(image_path)

    # cropping image img = image[y0:y1, x0:x1]
    image_ROI = image[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]

    # pre-processing the image
    gray = cv2.cvtColor(image_ROI, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #
    # # Morph open to remove noise and invert image
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # invert = 255 - opening
    # cv2.imshow('invert',thresh)
    # cv2.waitKey(0)

    # Perform text extraction
    text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
    return text


def process_image(image_path, selection_set):
    tags_list = dict()

    for selection in selection_set.keys():
        coordinates = selection_set[selection]
        print("coordinates for ", selection, " is ", coordinates)
        text = get_text(image_path, coordinates)
        tags_list[selection] = text

    print("tags list is:", tags_list)


if __name__=='__main__':
    process_image('ocr_example_3.jpeg', {'Name': [[117, 83], [321, 124]]})