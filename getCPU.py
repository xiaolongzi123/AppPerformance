# coding:utf-8
'''
获取系统total cpu
'''
import os, csv
import time
import csv
import numpy as np
from matplotlib import pyplot as plt

cpu_list = []
time_list = []
app_list = []
lines = []
package_name = []


# 读取进程名称（包名）
def get_applist():
    global package_name
    with open('config/director.txt', encoding='utf-8', mode='r') as f:
        lines_all = f.readlines()
        for appname in lines_all:
            package_name1 = appname
            appname_new = appname[0:15]
            package_name.append(package_name1)
            lines.append(appname_new)
        for line in lines:
            app_list.append(line.strip())


# 获取cpu数值
def get_cpu():
    global filename
    with open(filename, encoding="utf-8", mode="r") as f:
        lines = f.readlines()
        for appname in app_list:
            for lis in lines:
                # 适配低版本手机
                if appname in lis and '%' in lis:
                    now = time.strftime("%H:%M:%S", time.localtime())
                    time_list.append(now)
                    cpu_1 = lis.split('%')[0]
                    cpu_2 = cpu_1.split(' ')
                    # print(cpu_2)
                    cpu = cpu_2[len(cpu_2) - 1]
                    print(cpu, now)
                    cpu_list.append(cpu)
                    break
                # 适配高版本手机
                elif appname in lis:
                    now = time.strftime("%H:%M:%S", time.localtime())
                    time_list.append(now)
                    cpu1 = lis.split(' ')
                    # print(cpu1)
                    cpu2 = list(set(cpu1))
                    cpu2.sort(key=cpu1.index)
                    cpu_h = cpu2[len(cpu2) - 4]
                    print(cpu_h, now)
                    cpu_list.append(cpu_h)
                    break
                else:
                    pass


# csv头部
def write_head():
    headers = ['name:']
    headers.append(app_list[0])
    headers.append('init_cpu')
    with open('log_su/cpuinfo.csv', 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()


# 将数值写入csv，用于绘图时读取
def write_report():
    # headers = ['name', 'aaa', 'init_cpu']
    with open('log_su/cpuinfo.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key in cpu_list:
            writer.writerow([' ', ' ', key])


# 绘制折线图，生成测试报告
def mapping():
    filename = 'log_su/cpuinfo.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        highs = []
        for row in reader:
            high = row[2]
            highs.append(high)
        # print(highs)

    wights = time_list
    highs_float = list(map(float, highs))
    # print(f"****{highs}")
    print(f"CPU值：{highs_float}")
    # 输出平均值
    total = 0
    for value in highs_float:
        total += value
    average = round(total / len(highs_float), 2)
    print(f"CPU平均值：{average}")

    # 输出最低值和最高值
    highs_hl = sorted(highs_float)
    print(f"CPU最低值：{highs_hl[0]}")
    print(f"CPU最高值：{highs_hl[len(highs_hl) - 1]}")

    # 根据数据绘制图形
    plt.figure(figsize=(11, 4), dpi=600)
    # 生成网格
    # plt.grid()
    plt.grid(axis="y")
    # 折线图
    if package_name[0] == 'com.function3d.smfunctiondemo':
        plt.plot(wights, highs_float, "c-", linewidth=1, label="PPP")
    elif package_name[0] == 'com.oneapp.max.cn':
        plt.plot(wights, highs_float, "c-", linewidth=1, label="Opt1.6.1")
    elif package_name[0] == 'com.boost.clean.coin.cn':
        plt.plot(wights, highs_float, "c-", linewidth=1, label="Fastclear")
    elif package_name[0] == 'com.walk.sports.cn':
        plt.plot(wights, highs_float, "c-", linewidth=1, label="Walk")
    elif package_name[0] == 'com.diamond.coin.cn':
        plt.plot(wights, highs_float, "c-", linewidth=1, label="Amber")
    elif package_name[0] == 'com.oneapp.max.cleaner.booster.cn':
        plt.plot(wights, highs_float, "c-", linewidth=1, label="Space")
    else:
        plt.plot(wights, highs_float, "c-", linewidth=1, label=package_name[0])
    # 坐标轴范围
    # plt.ylim(300, 400)
    # plt.xlim(0, 10)

    plt.xlabel('time(H:Min:S)', fontsize=16)
    plt.ylabel("cpu_realtime(%)", fontsize=16)
    plt.title("cpu real time line chart", fontsize=24)
    plt.legend()

    # 横坐标显示间隔
    if len(wights) <= 15:
        pass
    else:
        t = int(len(wights) / 15)
        plt.xticks(range(0, len(wights), t))

    # 纵坐标显示间隔
    # plt.yticks(range(100, 300, 10))

    # 旋转日期
    plt.gcf().autofmt_xdate()

    # 展示每个坐标
    # for a, b in zip(wights, highs_float):
    #     plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=8)

    # plt.show()

    time_now = time.strftime("%m%d-%H-%M-%S", time.localtime())
    path = "report/" + time_now
    # path="D:/"+ time_now
    plt.savefig(path)


# 自动识别当前需检测的
def name_app():
    cmd = 'adb shell dumpsys window | findstr mCurrentFocus > log_su/name_info.csv'
    os.system(cmd)
    with open('log_su/name_info.csv', encoding='utf-8', mode='r') as f:
        lines = f.readlines()
        for line in lines:
            if 'mCurrentFocus' in line:
                name1 = line.split('/')[0].split(' ')
                name = name1[len(name1) - 1]

    with open('config/director.txt', encoding='utf-8', mode='w') as f_name:
        text = name
        # text="com.function3d.smfunctiondemo"
        f_name.write(text)
    print(f"将要监测的包名为：{text}")


# 控制监测时间
def time_control():
    global filename
    while True:
        end_time = time.time()
        if (end_time - start_time) / 60 >= tol_time:  # 分钟
            # if end_time - start_time >= tol_time:  # 秒
            break

        time.sleep(1)
        adb = "adb shell top -n 1 > log_su/adb_info.csv"
        d = os.system(adb)
        filename = "log_su/adb_info.csv"
        get_cpu()


if __name__ == "__main__":
    name_app()
    tol_time = int(input("请输入脚本执行时间(分钟)："))
    start_time = time.time()
    get_applist()
    write_head()
    time_control()
    write_report()
    mapping()