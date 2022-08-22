# -*- coding: utf-8 -*-
import os
import datetime
from easyxlsx import SimpleWriter


def main():
    # 切换git的目录
    os.chdir("E:\\Project\\xxx")
    cur = str(datetime.date.today())
    path = 'C:\\Users\\Administrator\\Desktop\\公司项目\\bugs\\' + cur + '.log'
    if os.path.exists(path):
        os.remove(path)
    os.system(
        'git log --pretty=format:"%s。"  --author tangfan --after=\'2020-11-15\' >> C:\\Users\\Administrator\\Desktop\\公司项目\\bugs\\' + cur + '.log')
    # 读取file文件
    log = open(path, 'r', encoding='utf-8')
    content = log.read()
    li = content.split("。")
    wri = []
    for i in li:
        if len(i) > 0:
            li = []
            li.append('项目名称')
            li.append(i)
            li.append("1")
            li.append("唐帆")
            li.append(cur)
            li.append(cur)
            wri.append(li)
    if len(wri) > 0:
        # 导出
        SimpleWriter(wri, headers=('项目名称', '任务名称', '权重', '研发人员', "预计时间", "完成时间"),
                     bookname="C:\\Users\\Administrator\\Desktop\\公司项目\\bugs\\daily.xlsx").export()


if __name__ == '__main__':
    main()
