import numpy as np
import math

# legacy for 1 byte depth planes
NEAR_PLANE = 10.0
FAR_PLANE = 1000.0 + NEAR_PLANE


def fov(deg):
    return np.deg2rad(deg)


def focal_length(photo_width, fov_in_deg):
    return 0.5 * photo_width / math.tan(fov(fov_in_deg) / 2)


# stereopair calibration constants
_chosen_detection_dist_meters = 10
STEREOPAIR_CHOSEN_DETECTION_DISTANCE = 100 * _chosen_detection_dist_meters
STEREOPAIR_BASELINE = 13.5 * 2
STEREOPAIR_FOV_DEG = 90 # градусов
SCREEN_WIDTH = 1920  # we will calculate everything in pixels so need to use converted depth
STEREOPAIR_FOCAL_LENGTH = focal_length(SCREEN_WIDTH, STEREOPAIR_FOV_DEG)

# algorithm
DISCRETE_DISPARITIES_COUNT = 128
ALGORITHM_BLOCK_SIZE = 15
WLS_LAMBDA = 8000 # typical val is 8000
WLS_SIGMA_COLOR = 2 # typical val range is [0.8; 2]

# analysis
DEPTH_ERROR_THRESHOLD = 43.2 #cm

# misc
BRIGHTNESS_INCREASE = 25
CLAHE_CONTRAST_INCREASE = 1
