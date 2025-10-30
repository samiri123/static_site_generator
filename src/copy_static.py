import os
import shutil

def copy_static():
    if os.path.exists('public'):
        try:
            shutil.rmtree('public')
        except Exception as e:
            print(f"Something went wrong during the deletion: {e}")
    if not os.path.exists('public'):
        os.mkdir('public')
    copy_dir('static', 'public')

def copy_dir(src_dir, tar_dir):
    if not os.path.exists(src_dir):
        raise Exception("source directory does not exist")
    try:
        entries = os.listdir(src_dir)
        for path in entries:
            src_path = os.path.join(src_dir, path)
            tar_path = os.path.join(tar_dir, path)
            if os.path.isfile(src_path):
                shutil.copy(src_path, tar_dir)
            else:
                os.mkdir(tar_path)
                copy_dir(src_path, tar_path)
    except Exception as e:
        print(f"Something went wrong during copying files and subdirectories: {e}")        