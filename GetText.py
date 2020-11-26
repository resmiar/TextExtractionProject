import pytesseract
import cv2


def get_text(image_path, coordinates):
    image = cv2.imread(image_path)

    # cropping image img = image[y0:y1, x0:x1]
    #add code to fix error if end_x or end_y greater than start_x or y
    if coordinates[0][1] > coordinates[1][1]:
        y0 = coordinates[1][1]
        y1 = coordinates[0][1]
    else:
        y0 = coordinates[0][1]
        y1 = coordinates[1][1]
    if coordinates[0][0] > coordinates[1][0]:
        x0 = coordinates[1][0]
        x1 = coordinates[0][0]
    else:
        x0 = coordinates[0][0]
        x1 = coordinates[1][0]

    image_ROI = image[y0:y1, x0:x1]
    # image_ROI = image[coordinates[0][1]:coordinates[1][1], coordinates[0][0]:coordinates[1][0]]


    # # pre-processing the image
    # gray = cv2.cvtColor(image_ROI, cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray, (3,3), 0)
    # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # #
    # # # Morph open to remove noise and invert image
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    # invert = 255 - opening
    # cv2.imshow('invert',thresh)
    # cv2.waitKey(0)

    # Perform text extraction
    text = pytesseract.image_to_string(image_ROI, lang='eng', config='--psm 6')
    # print(text)
    return text


def process_image(image_path, selection_set):
    tags_list = dict()

    for selection in selection_set.keys():
        coordinates = selection_set[selection]
        print("coordinates for ", selection, " is ", coordinates)
        text = get_text(image_path, coordinates)
        tags_list[selection] = text

    print("tags list is:", tags_list)
    return tags_list


if __name__=='__main__':
    # process_image('ocr_example_2.jpeg', {'Name': [[662, 381], [538, 410]]})

    process_image('ocr_example_2.jpeg', {'Name': [[538, 381], [662, 410]]})