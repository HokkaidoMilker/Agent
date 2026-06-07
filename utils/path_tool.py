import os
#获取工程所在根目录
def get_path()->str:
    current_path = os.path.abspath(__file__)
    cureent_dir = os.path.dirname(current_path)
    project_root = os.path.dirname(cureent_dir)
    return project_root

#传入相对路径获取绝对路径
def get_abs_path(relative_path=None)->str:
    project_root = get_path()
    relative_path = os.path.join(project_root,relative_path)
    return relative_path

if __name__ == '__main__':
    path = get_abs_path("/utils/path_tool.py")
    print(path)
