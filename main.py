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


silent = True
positions_analyzed = range(len(files_sorted) // 4)
# positions_analyzed = [0]
for i in positions_analyzed:
    print(f"Обработка позиции {i}")
    pngs = get_blob_by_blob_index(files_sorted, i)
    print(pngs)

    results = depth_and_metrics.do_your_stuff(*[f"{raw_data_folder}{png}" for png in pngs],
                                              silent=silent, name=f"Позиция {i}")
