# '''
# Нужно оценить возможную ошибку на исследуемых расстояниях. Для этого нужно построить график
# отображения диспаратности в глубину, и отметить на нем дискретные точки диспаратности
# которые получились после расчета. Затем оценить разницу между двумя значениями глубины в двух смежных
# точках, и это скажет о том какая может быть ошибка.
# '''

import numpy as np
import constants
from matplotlib import pyplot as plt
import itertools


def disparity_depth_conversion_function(value, focal_len, baseline):
    return focal_len * baseline / value


def calculate_current_delta_on_chosen_distance(focal_len, baseline):
    print('-' * 50)

    print(f'focal length: {focal_len}, baseline: {baseline}')
    alias_ddcf = lambda d: disparity_depth_conversion_function(d, focal_len, baseline)

    disparity_for_chosen_max_detection_range = int(alias_ddcf(constants.STEREOPAIR_CHOSEN_DETECTION_DISTANCE))
    errored_disparity = disparity_for_chosen_max_detection_range - 1  # Нужно рассчитать максимальную идеальную ошибку при ошибке в 1 пиксель
    print(disparity_for_chosen_max_detection_range)  # диспаратность на выбранном расстоянии

    error = alias_ddcf(errored_disparity) - alias_ddcf(disparity_for_chosen_max_detection_range)
    print(f"величина ошибки: {error}")

    print('-' * 50)
    return error


def optimize_params(baseline_range, fov_range, baseline_step=1, fov_step=1):
    permutations = list(itertools.product(range(baseline_range[0], baseline_range[1] + 1, baseline_step),
                                          range(fov_range[0], fov_range[1] + 1, fov_step)))

    results = []
    for pair in permutations:
        focal_len = constants.focal_length(constants.SCREEN_WIDTH, pair[1])
        error = calculate_current_delta_on_chosen_distance(focal_len, pair[0])
        results.append((error, pair[0] / 2, pair[1]))

    results_sorted = sorted(results, key=lambda values: values[0])

    for res in results_sorted:
        print(f"Baseline/2: {res[1]}, \tFOV: {res[2]}. \tError: {res[0]}")

    return results_sorted[0]


def plot_disparities_depth_graph(disparities_range, fov, baseline):
    disp_range_min = disparities_range[0]
    disp_range_max = disparities_range[1]

    disparities = np.linspace(disp_range_min, disp_range_max, disp_range_max - disp_range_min)
    focal = constants.focal_length(constants.SCREEN_WIDTH, fov)
    depths = disparity_depth_conversion_function(disparities, focal, baseline)
    plt.plot(disparities, depths)
    plt.show()


if __name__ == '__main__':
    optimize_params([27, 30], [90, 90], baseline_step=1, fov_step=5)
    plot_disparities_depth_graph([5, 200], constants.STEREOPAIR_FOV_DEG, constants.STEREOPAIR_BASELINE)


# baseline 27, fov 75 - optimal (~32 error)
# baseline 30, fov 90 - if fov doesnt work out (~38 error)
# baseline 27, fov 90 - current (~43.2 error)
