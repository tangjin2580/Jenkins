# !/usr/bin/python
# coding:utf-8
from bs4 import BeautifulSoup
# from git_data_get import GitDate
import requests
import jenkins
import xlwt
import xlrd
import re


class JenkinsDate(object):
    def __init__(self):
        pass

    def login(self, target):
        '''
        判断url抓取数据
        :param target: URL
        :return:返回抓取到底 HTML 数据
        '''
        server = jenkins.Jenkins("http://192.168.50.41:8088/", username='lixin', password='lixin2324')
        req = requests.get(url=target)
        soup = BeautifulSoup(req.content, 'html.parser', from_encoding='utf-8')
        return soup

    def extraction(self, soup):
        '''
        获取下层链接的 module 列表，并储存
        :param soup: login 函数抓取的数据集
        :return:返回构建 url
        '''
        module = []
        for link in soup.find_all('a', {'class': 'display-name'}):
            mod = link.get('href')
            module.append(mod)
        return module

    def retrieval(self, module, url, tail, u):
        '''
        检索符合要求的构建job,返回要检查的job
        :param module: module 列表
        :param url: 基础 url
        :param tail: 拼接 url 字段
        :param u: 限制抓取列表长度
        :return: 返回要抓取数据 job 的 url
        '''
        job = []
        for i in module:
            target = url + i + tail
            soup = JenkinsDate.login(self, target)
            try:
                contrast_value = soup.find(name='a', text='Coverage Report').text
                if contrast_value == 'Coverage Report':
                    job.append(target)
                else:
                    x = 1
            except AttributeError:
                pass
            if len(job) == u:
                break
        return job

    def initialization_data(self, job):
        '''
        数据抓取
        :param job: 传入的 job 界面链接
        :return: 返回抓取到的数据-需要的基础数据
        '''
        coverages = []
        excessive = []
        target = job[0]
        soup = JenkinsDate().login(target)
        coverage = soup.find_all("td", {"class": "data"})
        coverage_one = coverage[1].text
        coverage_three = coverage[3].text
        if len(coverages) >= 2:
            pass
        else:
            coverages.append(coverage_one)
            coverages.append(coverage_three)
        # 获取所有a 标签链接,储存下层链接的 module 列表
        i = 0
        for link in soup.find_all('a'):
            mod = link.get('href')
            # 判断获取的mod是否包含com，包含则加入列表
            if str(mod).startswith('com.'):
                excessive.append(mod)
            i += 1
        result = []
        for mod in excessive:
            target1 = job[0] + mod
            req1 = requests.get(url=target1)
            soup1 = BeautifulSoup(req1.content, 'html.parser', from_encoding='utf-8')
            for tag in soup1.find_all(re.compile("td")):
                dabe = tag.text
                result.append(dabe)
            for a in range(1):
                if 'com.' in result[0]:
                    break
                else:
                    del result[0]
            while '' in result:
                result.remove('')
        return result, coverages

    def analysis(self, list):
        '''
        数据分析
        :param list: 抓取数据 list 表
        :return: 把数据分析整理为我们想要的样子
        '''
        for i in list:
            if 'JenkinsPOS_PROJECTS' in i:
                c = list.index(i)
                del list[c]
        num = len(list) - 1
        for i in range(num):
            py = re.search('.:', list[num])
            if py is None:
                x = 1
            else:
                del list[num]
            num = num - 1
        name = ['name', 'instruction%', 'branch%', 'complexity%', 'line%', 'method%', 'class%']
        uu = name + list
        segmentation = [uu[i:i + 7] for i in range(0, len(uu), 7)]
        n = len(segmentation)
        for i in range(len(segmentation)):
            n = n - 1
            if 'com.' in segmentation[n][0]:
                del segmentation[n]
            else:
                continue
        u = [6, 5, 3, 1]
        wc = 1
        ww = len(segmentation)
        for v in range(len(segmentation)):
            for i in u:
                if v >= 0:
                    del segmentation[v][i]
                    wc = wc + 1
                elif wc == ww:
                    break
        n = len(segmentation)
        for i in range(len(segmentation)):
            n = n - 1
            if ('com.' in segmentation[n][0]):
                del segmentation[n]
            else:
                continue
        segmentation[0].append('ascription')
        return segmentation


class AllDate(object):
    def __init__(self):
        pass

    def data_result(self, u_data, ust_date):
        '''
        合并抓取的 ut list 和 ust list
        :param u_data: ut list
        :param ust_date: ust list
        :return: 返回列表整合了我们想要的行和列覆盖率信息数据
        '''
        for i in range(len(u_data)):
            for x in range(len(ust_date)):
                if not u_data[i][0] in ust_date[x]:
                    pass
                else:
                    u_data[i][1] = ust_date[x][1]
        return u_data

    def data_screen(self, ut_data):
        '''
        判断数据是否符合要求，数据过滤
        :param ut_data: 数据分析后的列表
        :return: 返回筛选数据
        '''
        screen = []
        screen_new = []
        for i in range(len(ut_data)):
            if i in (0, 1, 2, 3, 4):
                screen.append(ut_data[i])
            elif int(ut_data[i][1].replace('%', '')) < 70 or int(ut_data[i][2].replace('%', '')) < 80:
                screen.append(ut_data[i])
        for i in range(len(screen)):
            if screen[i] in screen_new:
                continue
            else:
                screen_new.append(screen[i])
        return screen_new

    def data_merge(self, file, data_list):
        '''
     对比新数据与增量数据
     :param file:  excel 文件路径
     :param data_list: 筛选好的数据列表
     :return: 返回现有结果与历史结果的对比结果
     '''
        excel_path = file
        excel = xlrd.open_workbook(excel_path, encoding_override='utf-8')
        sheet = excel.sheet_by_name('Sheet 1')
        sheet_name = sheet.name
        sheet_row = sheet.nrows
        # 将数据还原为列表
        sheet_data = []
        class_list = []
        ok = 0
        for i in range(sheet_row):
            sheet_data.append(sheet.row_values(i))
        print('sheet_data', len(sheet_data), sheet_data)
        # 分裂过渡表
        for w in range(5, len(sheet_data)):
            class_list.append(sheet_data[w][0])
        print('class_list', len(class_list), class_list)
        # 替换行/分支覆盖率数据
        for y in (1, 2):
            sheet_data[y][2] = data_list[y][2][0]
            sheet_data[y][3] = data_list[y][3][0]
        # 替换最新行/分支覆盖率
        print(range(5, len(data_list)))
        print(range(5, len(sheet_data)))
        for x in range(5, len(data_list)):
            for z in range(5, len(sheet_data)):
                if data_list[x][0] == sheet_data[z][0]:
                    if len(data_list[x]) == 3 and len(sheet_data[z]) == 3:
                        sheet_data[z][1] = data_list[x][1]
                        sheet_data[z][2] = data_list[x][2]
                    elif len(data_list[x]) == 5 and len(sheet_data[z]) == 3:
                        sheet_data[z][1] = data_list[x][1]
                        sheet_data[z][2] = data_list[x][2]
                        sheet_data[z].append(data_list[x][3])
                        sheet_data[z].append(data_list[x][4])
                    elif len(data_list[x]) == 5 and len(sheet_data[z]) == 5:
                        sheet_data[z][1] = data_list[x][1]
                        sheet_data[z][2] = data_list[x][2]
                        sheet_data[z][3] = data_list[x][3]
                        sheet_data[z][4] = data_list[x][4]
                    elif len(data_list[x]) == 3 and len(sheet_data[z]) == 5:
                        sheet_data[z][1] = data_list[x][1]
                        sheet_data[z][2] = data_list[x][2]
                    else:
                        pass
                elif data_list[x][0] != sheet_data[z][0]:
                    if data_list[x] in sheet_data:
                        pass
                    elif data_list[x] not in sheet_data:
                        if data_list[x][0] in class_list:
                            pass
                        else:
                            sheet_data.append(data_list[x])
                    else:
                        pass
                else:
                    pass
        for i in range(5):
            if i == 4:
                sheet_data[i][4] = 'Date of submission'
            else:
                del sheet_data[i][4]
        return sheet_data

    def data_merge_cup(self,file):
        '''
        将数据还原为列表
        :param file: 文件路径
        :return: 将数据还原为列表
        '''
        excel_path = file
        excel = xlrd.open_workbook(excel_path, encoding_override='utf-8')
        sheet = excel.sheet_by_name('Sheet 1')
        sheet_name = sheet.name
        sheet_row = sheet.nrows
        # 将数据还原为列表
        sheet_data = []
        class_list = []
        for i in range(sheet_row):
            sheet_data.append(sheet.row_values(i))
        return sheet_data

    def date_duplicate_removal(self, sheet_data):
        '''
        去重
        :param sheet_data:
        :return: 去重后的列表
        '''
        sheet_data_new = []
        for i in range(len(sheet_data)):
            sheet_data_new.append([z for z in sheet_data[i] if z != ''])
        new_sheet_data = []
        for x in sheet_data_new:
            if x not in new_sheet_data:
                new_sheet_data.append(x)
        sheet_new = []
        for z in range(len(new_sheet_data)):
            for y in range(len(new_sheet_data)):
                if new_sheet_data[z][0] == new_sheet_data[y][0]:
                    if len(new_sheet_data[z]) == 4:
                        sheet_new.append(new_sheet_data[z])
                    else:
                        sheet_new.append(new_sheet_data[y])
                else:
                    pass
        return sheet_new

    def date_duplicate(self, data_list):
        '''
        去重方式之-重定义列表去重
        :param data_list:
        :return:
        '''
        new_data_list = []
        for i in data_list:
            if i in new_data_list:
                pass
            else:
                new_data_list.append(i)
        return new_data_list


# 对比dev数据上升下降
class Summary(object):
    def __init__(self):
        pass

    # 判断函数，传参：新列表，旧列表
    def summary(self, one, two):
        '''
        对比列表数据上升下降结果
        :param one: 新数据列表
        :param two: 旧数据列表
        :return: 返回新列表，标明上升下降结果
        '''
        for i in range(1, len(one)):
            for x in range(1, len(two)):
                if one[i][0] == two[x][0]:
                    if int(one[i][2].replace('%', '')) == int(two[x][2].replace('%', '')):
                        one[i].append('No change')
                        break
                    elif int(one[i][2].replace('%', '')) < int(two[x][2].replace('%', '')):
                        one[i].append('line coverage desc')
                        break
                    elif int(one[i][2].replace('%', '')) > int(two[x][2].replace('%', '')):
                        one[i].append('line coverage asc')
                        break
        one[0].append('state')
        return one

    # 合并git与jenkins数据
    def compare_list(self, git_list, jenkins_list, table_d, table_c, table_b, table_a):
        '''
        合并 Git 和 Jenkins数据
        :param git_list: Git 列表
        :param jenkins_list: Jenkins 列表
        :param table_d: 覆盖率数据
        :param table_c: 覆盖率数据
        :param table_b: 覆盖率数据
        :param table_a: 覆盖率数据
        :return: 返回整合后的列表
        '''
        for i in range(len(jenkins_list)):
            for x in range(len(git_list)):
                if not jenkins_list[i][0] in git_list[x]:
                    continue
                elif jenkins_list[i][0] in git_list[x] and len(jenkins_list[i]) == 3:
                    indexd = git_list[x].index(jenkins_list[i][0])
                    jenkins_list[i].append(git_list[x][0])
                    jenkins_list[i].append(git_list[x][indexd+1])
                else:
                    pass
        jenkins_list.insert(0, table_d)
        jenkins_list.insert(0, table_c)
        jenkins_list.insert(0, table_b)
        jenkins_list.insert(0, table_a)
        return jenkins_list

    def data_new_sc(self, ut_data):
        screen = []
        screen_new = []
        print('ut_data', ut_data)
        for i in range(len(ut_data)):
            if ut_data[i] not in screen_new:
                print(ut_data[i])
                screen_new.append(ut_data[i])
            else:
                pass
        return screen_new

    def insert_data(self, ut_coverage_branch, ut_coverage_line, ust_coverage_branch, ust_coverage_line):
        '''
        插入表格汇总数据
        :param ut_coverage_branch: UT 分支覆盖率
        :param ut_coverage_line:  UT 行覆盖率
        :param ust_coverage_branch:  UST 分支覆盖率
        :param ust_coverage_line:  UST 行覆盖率
        :return: 返回插入数据：列表
        '''
        table_a = [['job_name'], ['job类型'], ['分支覆盖率'], ['行覆盖率']]
        table_b = [['OpsTech_Cstdn_Pos_Ms_Server_UST_Jacoco'], ['UST'], [], []]
        table_c = [['OpsTech_Cstdn_Pos_Ms_Server_UT_Jacoco'], ['UT'], [], []]
        table_d = [['注：分支覆盖率数据关注UST，行覆盖率数据关注UT。'], [], []]
        table_c[2].append(ut_coverage_branch)
        table_c[3].append(ut_coverage_line)
        table_b[2].append(ust_coverage_branch)
        table_b[3].append(ust_coverage_line)
        return table_a, table_b, table_c, table_d

    def dev_file(self, date):
        '''
        根据传入列表，生成 Excel 文件
        :param date:
        :return:
        '''
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        for i, row in enumerate(date):
            for j, col in enumerate(row):
                sheet1.write(i, j, col)
        workbook.save(r'.\File\dev_jenkins_coverage.xls')

    def coverage_file(self, date):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        for i, row in enumerate(date):
            for j, col in enumerate(row):
                sheet1.write(i, j, col)
        workbook.save(r'.\File\INCOS_coverage.xls')

    def ust_file(self, date):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        for i, row in enumerate(date):
            for j, col in enumerate(row):
                sheet1.write(i, j, col)
        workbook.save(r'.\File\ust_jenkins.xls')

    def git_jenkins(self, date):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        for i, row in enumerate(date):
            for j, col in enumerate(row):
                sheet1.write(i, j, col)
        workbook.save(r'.\File\git_jenkins.xls')

    def new_old_data(self, date):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        for i, row in enumerate(date):
            for j, col in enumerate(row):
                sheet1.write(i, j, col)
        workbook.save(r'.\File\new_old_data.xls')


class Implement(object):

    def __init__(self):
        pass

    def jenkins_date(self, targe, url, tail):
        html = JenkinsDate().login(targe)
        module = JenkinsDate().extraction(html)
        print('00', module)
        job = JenkinsDate().retrieval(module, url, tail, 1)
        result = JenkinsDate().initialization_data(job)
        list_one = result[0]
        coverage = result[1]
        coverage_new = JenkinsDate().analysis(list_one)
        return coverage_new, coverage

    def git_date(self):
        git = GitDate().verb()
        two = GitDate().obtain(git)
        three = GitDate().git_analysis(two)
        four = GitDate().date_end(three)
        return four

    # def coverage(self, ):


if __name__ == "__main__":
    ut_targe = 'http://jenkinsXXXXXXX'
    ust_targe = 'http://jenkinsXXXXXX'
    url = 'http://jenkinsXXXX'
    tail = 'jacoco/'

    x = Implement().jenkins_date(ut_targe, url, tail)

