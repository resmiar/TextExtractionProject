import os
import pytesseract
import cv2
from pytesseract import TesseractNotFoundError


def get_text(image_path, coordinates, resize=None):
    image = cv2.imread(image_path)
    print('resize is {}'.format(resize))
    if resize is not None:
        image = cv2.resize(image,resize)

    # cropping image img = image[y0:y1, x0:x1]
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

    # # pre-processing the image
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
    text = ''
    try:
        text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
    except TesseractNotFoundError:
        print("Tesseract is not installed or not set in environment path variable")
    return text.strip()


def process_image(image_path, selection_set, resize=None):
    tags_list = dict()

    for selection in selection_set.keys():
        coordinates = selection_set[selection]
        print("coordinates for ", selection, " is ", coordinates)
        text = get_text(image_path, coordinates, resize=resize)
        tags_list[selection] = text

    print("tags list is:", tags_list)
    return tags_list


def process_bulk(template, directory_name):
    # Getting list of images in the given path
    images = load_images_from_folder(directory_name)

    # Get template details
    print("Inside process bulk. Template is: ", template)
    image_size = tuple(template[0])
    attributes = list(template[1].keys())
    attribute_values = dict()

    # For each file in list, call process image with image resizing
    for image in images:
        image_path = directory_name + '//'+image
        tags_list = process_image(image_path, template[1], resize=image_size)
        print('image size is {}'.format(image_size))
        print(tags_list)
        attribute_values[image] = list(tags_list.values())
        print(attribute_values)

    return attributes, attribute_values


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(filename)
    return images


# if __name__ == '__main__':
#     process_image('ocr_example_2.jpeg', {'Name': [[495, 235], [314, 200]]})


