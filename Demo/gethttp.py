# coding=UTF-8
import os  # 导入os库
import urllib.request  # 导入urllib库
import shutil
import zipfile
import sys  # 获取输入参数import os #使用命令行port=sys.argv[1]



def file_downloand():
    # 文件url

    if not os.path.exists('D:/0下载测试'):
        os.makedirs('D:/0下载测试')
    # 文件基准路径
    basedir = os.path.abspath('D:/0下载测试')
    # 下载到服务器的地址
    file_path = os.path.join(basedir, 'war')

    try:
        file_suffix = os.path.splitext(image_url)[1]
        filename = '{}{}'.format(file_path, file_suffix)  # 拼接文件名。
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Apipost client Runtime/+https://www.apipost.cn/'),
                             ('Authorization', 'Basic bGl4aW46bGl4aW4yMzI0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(image_url, filename=filename)
        print("成功下载文件")

        zips = zipfile.ZipFile('D:/0下载测试/archive.zip', 'r')
        zips.extractall("D:/0下载测试")
        zips.close()

        file_copy()

        copy()

    except IOError as exception_first:  # 设置抛出异常
        print(1, exception_first)

    except Exception as exception_second:  # 设置抛出异常
        print(2, exception_second)


# def file_copy():
#     new_path = 'D:/afServer/nginx-8400/html/备份'
#     if not os.path.exists(new_path):
#         os.makedirs(new_path)
#     # shutil.copytree("D:/afServer/nginx-8400/html/static", "D:/afServer/nginx-8400/html/备份/static")
#     shutil.copyfile("D:/afServer/nginx-8400/html/index.html", "D:/afServer/nginx-8400/html/备份/index.html")
#     print('文件已备份')

def start():
  cmd="I:\桌面\Print.bat"
  win32api.ShellExecute(0, 'open', cmd, '', '', 1)  # 前台打开

start()
print(1)


# def copy():
#     shutil.rmtree("D:/afServer/nginx-8400/html/static")
#     os.remove("D:/afServer/nginx-8400/html/index.html")
#     shutil.copytree("D:/0下载测试/archive/dist/static", "D:/afServer/nginx-8400/html/static")
#     shutil.copyfile("D:/0下载测试/archive/dist/index.html", "D:/afServer/nginx-8400/html/index.html")
#     print('更新完成')


if __name__ == '__main__':
    file_downloand()
