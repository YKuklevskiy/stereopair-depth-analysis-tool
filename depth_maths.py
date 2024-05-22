import numpy as np

import constants
from math_utils import *

near_plane = constants.NEAR_PLANE
far_plane = constants.FAR_PLANE
baseline = constants.STEREOPAIR_BASELINE
focal_length = constants.STEREOPAIR_FOCAL_LENGTH


# legacy
def remap_dm_to_depth(value):
    #     return clamp01(value / 255) * far_plane
    return map_n_clamp_val_to_int(value, (0, 255), (near_plane, far_plane))


# legacy
def remap_depth_to_dm(value):
    return value * 255 / far_plane


# take a depth rgb data (which is a Vector3), and calculate actual depth value
def precise_depth_remap_to_dm(data):
    # b1 = data[2]
    # b2 = data[1]
    # b3 = data[0]  # BGR, not RGB

    #nparray
    b1 = data[:, :, 2]
    b2 = data[:, :, 1]  # BGR, not RGB
    b3 = data[:, :, 0]  # BGR, not RGB

    return b1 * 256 + b2 + b3 / 256.0


# d = f * B / z => z = f * B / d
def mega_cool_disp_depth_function(d_val):
    return focal_length * baseline / d_val


# isPreScaled - if False, disparity will be divided by 16 as it is the
# factor which opencv uses to store CV16S disparity values.
# See ximgproc::getDisparityVis implementation for details.
#
# takes a disparity value, which was output by the algorithm, and calculates predicted depth value
def depth(disparity_value, is_pre_scaled=False):
    if disparity_value <= 0: return 256*256

    if not is_pre_scaled:
        disparity_value /= 16.0

    return focal_length * baseline / disparity_value
    # return min(focal_length * baseline / disparity_value,
    #            far_plane) 


# calculates the disparity value for a depth value with set camera settings
def disparity(depth_value):
    depth_value = remap_dm_to_depth(depth_value)

    # if depth <= 0:
    #     return 100000000
    return focal_length * baseline / depth_value


def visualize_3byte_depth(depth):
    calculated = mega_cool_disp_depth_function(precise_depth_remap_to_dm(depth.astype(np.float64)))
    return calculated