# coding:utf-8
'''
获取系统total memory
'''
import os, csv
import time
import csv
import numpy as np
from matplotlib import pyplot as plt

mem_dict = {}
time_list = []
app_list = []
package_name = []
t = 0


def get_applist():
    global package_name
    with open('config/director.txt', encoding='utf-8', mode='r') as f:
        lines = f.readlines()
        for line in lines:
            package_name1 = line
            package_name.append(package_name1)
            app_list.append(line.strip())


def get_mem():
    global filename
    with open(filename, encoding="utf-8", mode="r") as f:
        lines = f.readlines()
        start_flag = False
        for appname in app_list:
            for line in lines:
                if "Total PSS by OOM adjustment" in line:
                    break
                if appname in line and 'pid' in line and 'kB' in line:
                    mem_v = line.strip().split(':')[0].replace('kB', '').replace(',', '')
                    line_name = line.split(':')[1].split('(')[0].strip()
                    if line_name in appname:
                        mem_v = round(float(mem_v) / 1024, 2)
                        mem_dict[appname] = mem_v
                        now_v = time.strftime("%H:%M:%S", time.localtime())
                        # now_int = int(now_v)
                        time_list.append(now_v)
                        print(mem_v, now_v)
                        break
                elif appname in line and 'pid' in line and 'K' in line:
                    mem_v = line.strip().split(':')[0].replace('K', '').replace(',', '')
                    line_name = line.split(':')[1].split('(')[0].strip()
                    if line_name in appname:
                        mem_v = round(float(mem_v) / 1024, 2)
                        mem_dict[appname] = mem_v
                        now_v = time.strftime("%H:%M:%S", time.localtime())
                        # now_int = int(now_v)
                        time_list.append(now_v)
                        print(mem_v, now_v)
                        break


def write_head():
    headers = ['name:']
    headers.append(app_list[0])
    headers.append('init_mem')
    with open('log_su/meminfo.csv', 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()


def write_report():
    headers = ['name', 'aaa', 'init_mem']
    with open('log_su/meminfo.csv', 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        for key in mem_dict:
            writer.writerow({'init_mem': mem_dict[key]})


def mapping():
    filename = 'log_su/meminfo.csv'
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

    print(f"内存值：{highs_float}")

    # 输出平均值
    total = 0
    for value in highs_float:
        total += value
    average = round(total / len(highs_float), 2)
    print(f"内存平均值：{average}")

    # 输出最低值和最高值
    highs_hl = sorted(highs_float)
    print(f"内存最低值：{highs_hl[0]}")
    print(f"内存最高值：{highs_hl[len(highs_hl) - 1]}")

    # 根据数据绘制图形

    plt.figure(figsize=(11, 4), dpi=600)

    # 生成网格
    # plt.grid()
    plt.grid(axis="y")

    if package_name[0] == 'com.function3d.smfunctiondemo':
        plt.plot(wights, highs_float, "c-", linewidth=1, label="PPP")
    elif package_name[0] == 'com.oneapp.max.cn':
        plt.plot(wights, highs_float, "c-", linewidth=1, label="Opt")
    elif package_name[0] == 'com.boost.clean.coin.cn':
        plt.plot(wights, highs_float, "c-", linewidth=1, label="fastclear")
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
    plt.ylabel("Number (Mb)", fontsize=16)
    plt.title("meminfo", fontsize=24)
    plt.legend()

    # 横坐标显示间隔
    if len(wights) <= 15:
        pass
    else:
        t = int(len(wights) / 15)
        plt.xticks(range(0, len(wights), t))

    # 坐标刻度
    # my_y_ticks = np.arange(300, 400, 10)
    # my_x_ticks = np.arange(1, 10, 1)
    # plt.xticks(my_x_ticks)
    # plt.yticks(my_y_ticks)
    # plt.yticks(range(100, 300, 10))

    # 旋转日期
    plt.gcf().autofmt_xdate()

    # 展示每个坐标
    # for a, b in zip(wights, highs_float):
    #     plt.text(a, b, (a, b), ha='center', va='bottom', fontsize=8)

    # plt.show()

    time_now = time.strftime("%m%d-%H-%M-%S", time.localtime())
    path = "report/" + time_now
    # path = "D:/" + time_now
    plt.savefig(path)


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
        f_name.write(text)
    print(f"将要监测的包名为：{text}")


def time_control():
    global filename
    while True:
        end_time = time.time()
        if (end_time - start_time) / 60 >= tol_time:  # 分钟
            # if end_time - start_time >= tol_time:    #秒
            break
        # time.sleep(2)
        # filename = str(input("请输入文件名："))
        adb = "adb shell dumpsys meminfo > log_su/adb_info1.csv"
        d = os.system(adb)
        filename = "log_su/adb_info1.csv"
        get_mem()
        write_report()


if __name__ == "__main__":
    name_app()
    tol_time = int(input("请输入脚本执行时间(分钟)："))
    start_time = time.time()
    get_applist()
    write_head()
    time_control()
    mapping()