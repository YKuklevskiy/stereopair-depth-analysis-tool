import os


def list_files_in_directory(directory_path):
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]


def get_time_index_from_name(name):
    return name.split('_')[-1][:-4]


def create_tuple_pairs(values):
    result = []
    for i in range(0, len(values) - 1, 2):
        pair = (values[i], values[i + 1])
        result.append(pair)
    return result
