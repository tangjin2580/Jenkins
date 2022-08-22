import os
import time
import datetime
import threading


def run():
    del_file()
    del_file1()
    del_file2()
    print(datetime.datetime.now())
    r_t01 = threading.Timer(8600, run)
    r_t01.start()


def del_file():
    print("d盘清理")
    filepath = 'D:\\'
    del_list = os.walk(filepath)
    for dirpath, dirnames, filenames in del_list:
        lists = os.listdir(dirpath)
        for lis in lists:
            try:
                file_path = os.path.join(dirpath, lis)
                if os.path.isfile(file_path):
                    if file_path.endswith(".log"):
                        if time.time() - os.path.getmtime(file_path) > 86400 * 61:
                            print(file_path)
                            os.remove(file_path)
            except Exception:
                continue


def del_file1():
    print("e盘清理")
    filepath = 'E:\\'
    del_list = os.walk(filepath)
    for dirpath, dirnames, filenames in del_list:
        lists = os.listdir(dirpath)
        for lis in lists:
            try:
                file_path = os.path.join(dirpath, lis)
                if os.path.isfile(file_path):
                    if file_path.endswith(".log"):
                        if time.time() - os.path.getmtime(file_path) > 86400 * 61:
                            print(file_path)
                            os.remove(file_path)
            except Exception:
                continue


def del_file2():
    print("f盘清理")
    filepath = 'F:\\'
    del_list = os.walk(filepath)
    for dirpath, dirnames, filenames in del_list:
        lists = os.listdir(dirpath)
        for lis in lists:
            try:
                file_path = os.path.join(dirpath, lis)
                if os.path.isfile(file_path):
                    if file_path.endswith(".log"):
                        if time.time() - os.path.getmtime(file_path) > 86400 * 61:
                            print(file_path)
                            os.remove(file_path)
            except Exception:
                continue


if __name__ == '__main__':
    t01 = threading.Thread(target=run)

run()
