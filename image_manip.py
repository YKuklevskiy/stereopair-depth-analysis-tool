import cv2
import constants


def read_image(filename):
    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)

    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img


def _increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def _increase_contrast(img, value=2):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE
    clahe = cv2.createCLAHE(clipLimit=value, tileGridSize=(16, 9))
    cl = clahe.apply(l_channel)

    limg = cv2.merge((cl, a, b))
    return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


def prepare_image(img):
    img = _increase_brightness(img, constants.BRIGHTNESS_INCREASE)
    img = _increase_contrast(img, constants.CLAHE_CONTRAST_INCREASE)
    return img
