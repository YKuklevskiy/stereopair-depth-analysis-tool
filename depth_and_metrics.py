import cv2
import cv2.ximgproc
import itertools
from matplotlib import pyplot as plt
import numpy as np

import constants
from utilities import *
from image_manip import *
from depth_maths import *
from analysis_results import AnalysisResults

import os

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"


def do_your_stuff(rd_file_name, rr_file_name, ld_file_name, lr_file_name, silent=False, name="42"):
    ldepth = read_image(ld_file_name)
    # rdepth = read_image(rd_file_name)
    lraw = read_image(lr_file_name)
    rraw = read_image(rr_file_name)

    # increase brightness
    lraw = prepare_image(lraw)
    rraw = prepare_image(rraw)

    lraw_8UC1 = cv2.cvtColor(lraw, cv2.COLOR_BGR2GRAY)
    rraw_8UC1 = cv2.cvtColor(rraw, cv2.COLOR_BGR2GRAY)

    stereo_block_matching_params = {
        'blockSize': constants.ALGORITHM_BLOCK_SIZE,
        'numDisparities': constants.DISCRETE_DISPARITIES_COUNT
    }

    print("LOG: начало обработки")
    left_matcher = cv2.StereoSGBM_create(**stereo_block_matching_params)
    wls_filter = cv2.ximgproc.createDisparityWLSFilter(left_matcher)
    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)
    ldisp = left_matcher.compute(lraw_8UC1, rraw_8UC1)
    rdisp = right_matcher.compute(rraw_8UC1, lraw_8UC1)

    wls_filter.setLambda(constants.WLS_LAMBDA)
    wls_filter.setSigmaColor(constants.WLS_SIGMA_COLOR)
    filtered_disparity = wls_filter.filter(ldisp, lraw, None, rdisp)
    visualized = cv2.ximgproc.getDisparityVis(filtered_disparity)
    print("LOG: обработка окончена")

    # Now as we have both the raw and calculated visualized depth map, we analyze it.
    inv_filt_disp_vis = (filtered_disparity).astype(np.float64)

    left_border = -1
    # find left border of calculable disp:
    for i in range(inv_filt_disp_vis.shape[1]):
        if inv_filt_disp_vis[0][i] >= 0:
            left_border = i
            break

    inv_filt_disp_vis = inv_filt_disp_vis[:, left_border:]
    # real_disp = (ldepth[:, :, 0]).astype(np.float64) # это старый метод
    real_disp = precise_depth_remap_to_dm((ldepth[:, left_border:]).astype(np.float64))
    # real_disp *= 16

    # now we get to remap all these to depth great!!!
    calc_depth = inv_filt_disp_vis.copy()
    real_depth = real_disp.copy()

    for x, y in itertools.product(range(calc_depth.shape[0]), range(calc_depth.shape[1])):
        calc_depth[x][y] = depth(calc_depth[x][y])
        # real_depth[x][y] = remap_dm_to_depth(real_depth[x][y])

    pixel_count = inv_filt_disp_vis.shape[0] * inv_filt_disp_vis.shape[1]
    diff = calc_depth - real_depth
    distance_mask = np.logical_and(real_depth >= 500, real_depth <= 1000)
    diff_mask = np.logical_and(calc_depth < 256*256-256, distance_mask)
    # diff_mask = calc_depth < 256 * 256
    flat_masked_diff = diff[diff_mask].flatten()

    min_diff = np.absolute(flat_masked_diff).min()
    max_diff = flat_masked_diff.max()
    mean_diff = np.absolute(flat_masked_diff.mean())
    median_diff = np.quantile(flat_masked_diff, 0.5)
    mean_abs_diff = np.absolute(flat_masked_diff).mean()
    median_abs_diff = np.quantile(np.absolute(flat_masked_diff), 0.5)
    std_diff = flat_masked_diff.std()
    std_abs_diff = np.absolute(flat_masked_diff - flat_masked_diff.mean()).mean()

    calc_far_mask = inv_filt_disp_vis <= 16
    real_far_mask = real_disp >= 256*256-256

    calc_0_perc = inv_filt_disp_vis[calc_far_mask].shape[0] / pixel_count
    real_0_perc = real_disp[real_far_mask].shape[0] / pixel_count

    # plots
    def get_figure():
        figure = plt.figure(name, figsize=(18, 9))
        plt.subplots_adjust(left=0.03, right=0.97, bottom=0.06, top=0.94, wspace=0.04, hspace=0.4)
        return figure

    rows = 2
    columns = 2
    fig = get_figure()

    def imshow_macro(*args):
        if silent:
            return

        plt.imshow(*args)

    fig.add_subplot(rows, columns, 1)
    plt.gca().set_title('RealImage')
    imshow_macro(cv2.cvtColor(lraw, cv2.COLOR_BGR2RGB))

    fig.add_subplot(rows, columns, 2)
    plt.gca().set_title('RealDepth')
    imshow_macro(visualize_3byte_depth(ldepth), 'gray')

    fig.add_subplot(rows, columns, 3)
    plt.gca().set_title('CalcDepth')
    imshow_macro(visualized, 'gray')

    # Разница карт глубины
    visual_depth_diff = visualize_3byte_depth(ldepth)[:, left_border:] - visualized[:, left_border:]
    fig.add_subplot(rows, columns, 4)
    plt.gca().set_title('DepthDiff')
    imshow_macro(np.absolute(visual_depth_diff), 'gray')

    if not silent:
        plt.show()

    fig = get_figure()

    # Дальние точки на реальной карте
    real_depth_far_thresh = (real_disp >= 256*256-256)*255
    fig.add_subplot(rows, columns, 2)
    plt.gca().set_title('RawFarPoints')
    imshow_macro(real_depth_far_thresh, 'gray')

    # Дальние точки на рассчитанной карте
    calc_depth_far_thresh = (inv_filt_disp_vis <= 20)*255
    fig.add_subplot(rows, columns, 3)
    plt.gca().set_title('CalculatedFarPoints')
    imshow_macro(calc_depth_far_thresh, 'gray')

    # Разница зон дальних точек
    far_thresh_diff = np.logical_xor(real_depth_far_thresh == 255, calc_depth_far_thresh == 255)
    fig.add_subplot(rows, columns, 4)
    plt.gca().set_title('FarPointsDiff')
    imshow_macro(far_thresh_diff, 'gray')


    # E-ошибка
    depth_diff_threshold = constants.DEPTH_ERROR_THRESHOLD
    abs_diff = np.absolute(diff)
    errors = np.logical_and(abs_diff > depth_diff_threshold, calc_depth_far_thresh != 255) * 255

    fig.add_subplot(rows, columns, 1)
    plt.gca().set_title('Errors')
    imshow_macro(errors, 'gray')


    # False Negative pixel count
    fnpc = np.logical_and(calc_depth_far_thresh == 0, real_depth_far_thresh == 255).sum()
    fnpr = fnpc / pixel_count
    # print("Ложно-отрицательные дальние пиксели:", fnpc)

    # False Positive pixel count
    fppc = np.logical_and(calc_depth_far_thresh == 255, real_depth_far_thresh == 0).sum()
    fppr = fppc / pixel_count
    # print("Ложно-положительные дальние пиксели:", fppc)

    results = AnalysisResults()
    results.setup(
        min_diff,
        max_diff,
        mean_diff,
        mean_abs_diff,
        median_diff,
        median_abs_diff,
        std_diff,
        std_abs_diff,
        calc_0_perc,
        real_0_perc,
        fnpr,
        fppr
    )

    analysis_filename_index = get_time_index_from_name(ld_file_name)
    analysis_filename = f"{analysis_filename_index}.txt"
    results.save_analysis_results(analysis_filename)

    if not silent:
        results.print_metrics()
        analysis_table_filename = f"{analysis_filename_index}.csv"
        results.save_analysis_results_as_table(analysis_table_filename)

    if not silent:
        plt.show()

    plt.close()
