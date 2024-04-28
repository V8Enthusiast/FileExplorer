import os

# def compare_2_directories(source_path, target_path):
#     data_in_source = os.listdir(source_path)
#     data_in_target = os.listdir(target_path)
#     for item in data_in_source:
#         if os.path.isdir(source_path + item):
#             compare_2_directories(source_path + item + "/", target_path + item + "/")
#         else:
#             if item in data_in_target:
#                 print("Conflict in " + item)

def compare_2_directories(source_path, target_path, conflicts=None):
    if conflicts is None:
        conflicts = []
    data_in_source = os.listdir(source_path)
    if os.path.exists(target_path):
        data_in_target = os.listdir(target_path)
    else:
        data_in_target = []
    for item in data_in_source:
        source_item_path = os.path.join(source_path, item)
        target_item_path = os.path.join(target_path, item)
        if os.path.isdir(source_item_path):
            compare_2_directories(source_item_path + "\\", target_item_path + "\\", conflicts)
        else:
            if item in data_in_target:
                conflicts.append(source_item_path)
    return conflicts