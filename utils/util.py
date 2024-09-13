import os
import json

def get_directory_structure(rootdir):
    """
    生成只包含文件夹的层次结构，并以字典形式返回
    """
    def build_tree(dirpath):
        tree = {}
        # 列出当前文件夹中的所有条目（文件夹和文件）
        for entry in os.listdir(dirpath):
            full_path = os.path.join(dirpath, entry)
            if os.path.isdir(full_path):
                # 如果是文件夹，递归调用build_tree并构建树
                sub_tree = build_tree(full_path)
                # 如果子文件夹为空，设置为[]
                tree[entry] = sub_tree if sub_tree else []
        return tree

    return json.dumps(build_tree(rootdir), ensure_ascii=False, indent=4)


def get_all_files_in_directory(directory: str):
    """
    递归获取某个文件夹及其子文件夹下的所有文件
    """
    all_files = []
    for root, dirs, files in os.walk(directory):
        # 筛选出以.xlsx, .xls, .csv结尾的文件
        for file in files:
            if file.endswith(('.xlsx', '.xls', '.csv')):
                # 组合相对路径
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                all_files.append([file, relative_path])
    return all_files