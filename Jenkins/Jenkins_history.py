import os.path

import jenkinsapi
import openpyxl
import datetime

now_time = datetime.datetime.now().strftime("%Y/%m/%d")
print(now_time)


def get_build_history(jk) -> list:
    for job_name in jk.keys():
        job = jk.get_job(job_name)
        # number1 = job.get_last_completed_buildnumber()
        number = job.get_next_build_number()
        if number == 1:
            continue
        for n in range(1, 1):
        # for n in range(number - 2, number):
            try:
                b = job.get_build(n)
                # branch1 = b._get_vcs()
                # branch = branch1[]
                # if b.get_timestamp().strftime("%Y/%m/%d") != now_time:
                #     print(b)
                #     continue
            except jenkinsapi.custom_exceptions.NotFound:
                continue
            info = {
                'job_name': job_name,
                # 'job_url': job.url,
                'number': n,
                'node': b.get_slave() or 'master',
                'branch': str(b._get_vcs),
                'Datestamp': b.get_timestamp().strftime("%Y/%m/%d"),
                'timestamp': b.get_timestamp().strftime("%Y/%m/%d-%H:%M:%S"),
                'duration': round(b.get_duration().total_seconds()),
                'status': b.get_status(),
                'cause': b.get_causes()[0].get('shortDescription').replace('Started by ', '')
            }
            print(info)
            yield info


jk = jenkinsapi.jenkins.Jenkins("http://192.168.50.41:8088", username='lixin', password='lixin2324')
build_history = get_build_history(jk)

wb = openpyxl.Workbook(write_only=True)
ws = wb.create_sheet('构建历史')
ws.append(['任务名', '构建编号', '所在节点', '打包分支', '开始日期', '开始时间', '耗时', '状态', '启动者'])
for i in build_history:
    ws.append([i['job_name'], i['number'], i['node'], i['branch'], i['Datestamp'],
               i['timestamp'], i['duration'], i['status'], i['cause']])
    print('fetched ', i['job_name'], '\t#', i['number'])

# 创建文件夹
add_file_path: str = 'jenkins\history'
if not os.path.exists(add_file_path):
    print('文件夹', add_file_path, '不存在,已创建')
    os.makedirs(add_file_path)
    file_path = os.getcwd()+os.sep+add_file_path

 file_name= now_time+'Jenkins构建历史.xlsx'

wb.save("./jenkins/history/Jenkins构建历史.xlsx")

wb.close()
