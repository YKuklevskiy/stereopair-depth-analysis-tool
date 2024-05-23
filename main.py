from utilities import *
import depth_and_metrics


raw_data_folder = "Data/Raw/"

# get all files to analyze
files = list_files_in_directory(raw_data_folder)
files_sorted = sorted(files, key=lambda file: int(get_time_index_from_name(file)))


def get_blob_by_blob_index(blobs: list, index):
    ind = index * 4

    def get_prefix(name):
        return '_'.join(name.split('_')[:3])

    d = {get_prefix(f): f for f in blobs[ind:ind+4]}
    return d['right_cam_d'], d['right_cam_r'], d['left_cam_d'], d['left_cam_r']


silent = False
positions_analyzed = range(len(files_sorted) // 4)
# positions_analyzed = [0]
id_filter = ['1715901218315', '1715901487391']
# additional_condition_for_position = None
additional_condition_for_position = lambda l_pngs: len(set(id_filter).intersection(set(map(get_time_index_from_name, l_pngs)))) > 0
for i in positions_analyzed:
    pngs = get_blob_by_blob_index(files_sorted, i)
    if additional_condition_for_position is not None and not additional_condition_for_position(pngs):
        continue
    print(f"Обработка позиции {i}")
    print(pngs)

    results = depth_and_metrics.do_your_stuff(*[f"{raw_data_folder}{png}" for png in pngs],
                                              silent=silent, name=f"Позиция {i}")
