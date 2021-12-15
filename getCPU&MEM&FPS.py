# coding:utf-8
'''
获取系统total memory
'''
import re
import threading
import datetime
import os, csv
import time
import csv

import numpy as np
from matplotlib import pyplot as plt
from pyecharts import Line,Page,Overlap

import pandas as pd

mem_dict = {}
cpu_list = []
mem_list = []
time_list = []
time_list_cpu = []
time_list_mem = []
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
                    cpu_1 = lis.split('%')[0]
                    cpu_2 = cpu_1.split(' ')
                    cpu = cpu_2[len(cpu_2) - 1]
                    print(cpu, now)
                    with open('log_su/cpuinfo.csv', 'a+', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([' ', now, cpu])
                    break
                #针对红米手机
                elif "com.function3d+" in lis:
                    now = time.strftime("%H:%M:%S", time.localtime())
                    cpu1 = lis.split(' ')
                    cpu2 = list(set(cpu1))
                    # print(cpu1)
                    cpu2.sort(key=cpu1.index)
                    # print(cpu2)
                    cpu_h = cpu2[len(cpu2) - 3]
                    # cpu_h = cpu1[10]
                    print(cpu_h, now)
                    # 写入cpu
                    with open('log_su/cpuinfo.csv', 'a+', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([' ', now, cpu_h])
                    break
                # 适配高版本手机
                elif appname in lis:
                    now = time.strftime("%H:%M:%S", time.localtime())
                    cpu1 = lis.split(' ')
                    cpu2 = list(set(cpu1))
                    cpu2.sort(key=cpu1.index)
                    cpu_h = cpu2[len(cpu2) - 4]
                    print(cpu_h, now)
                    # 写入cpu
                    with open('log_su/cpuinfo.csv', 'a+', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow([' ', now, cpu_h])
                    break
                else:
                    pass


def get_mem():
    global filename1
    with open(filename1, encoding="utf-8", mode="r") as f:
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
                        now_v = time.strftime("%H:%M:%S", time.localtime())
                        print(mem_v, now_v)
                        # 写入mem
                        with open('log_su/meminfo.csv', 'a+', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([' ', now_v, mem_v])
                        break
                elif appname in line and 'pid' in line and 'K' in line:
                    mem_v = line.strip().split(':')[0].replace('K', '').replace(',', '')
                    line_name = line.split(':')[1].split('(')[0].strip()
                    if line_name in appname:
                        mem_v = round(float(mem_v) / 1024, 2)
                        now_v = time.strftime("%H:%M:%S", time.localtime())
                        print(mem_v, now_v)
                        # 写入mem
                        with open('log_su/meminfo.csv', 'a+', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([' ', now_v, mem_v])
                        break


def write_head_mem():
    headers = ['name:']
    headers.append(app_list[0])
    headers.append('init_mem')
    with open('log_su/meminfo.csv', 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
# csv头部
def write_head_cpu():
    headers = ['name:']
    headers.append(app_list[0])
    headers.append('init_cpu')
    with open('log_su/cpuinfo.csv', 'w+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()


def mapping_mem():
    filename1 = 'log_su/meminfo.csv'
    with open(filename1) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        highs = []
        wights= []
        for row in reader:
            high = row[2]
            wight=row[1]
            highs.append(high)
            wights.append(wight)
        # print(highs)

    # wights = time_list_mem
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
    plt.plot(wights, highs_float, "c-", linewidth=1, label="memory")
    # if package_name[0] == 'com.function3d.smfunctiondemo':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="PPP")
    # elif package_name[0] == 'com.oneapp.max.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Opt")
    # elif package_name[0] == 'com.boost.clean.coin.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="fastclear")
    # elif package_name[0] == 'com.walk.sports.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Walk")
    # elif package_name[0] == 'com.diamond.coin.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Amber")
    # elif package_name[0] == 'com.oneapp.max.cleaner.booster.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Space")
    # else:
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label=package_name[0])
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
    path = "report/mem" + time_now
    # path = "D:/" + time_now
    # plt.show()
    plt.savefig(path)

# 绘制折线图，生成测试报告
def mapping_cpu():
    filename = 'log_su/cpuinfo.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        highs = []
        wights=[]
        for row in reader:
            high = row[2]
            wight=row[1]
            highs.append(high)
            wights.append(wight)
        # print(highs)

    # wights = time_list_cpu
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
    plt.plot(wights, highs_float, "c-", linewidth=1, label="cpu")
    # if package_name[0] == 'com.function3d.smfunctiondemo':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="PPP")
    # elif package_name[0] == 'com.oneapp.max.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Opt1.6.1")
    # elif package_name[0] == 'com.boost.clean.coin.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Fastclear")
    # elif package_name[0] == 'com.walk.sports.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Walk")
    # elif package_name[0] == 'com.diamond.coin.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Amber")
    # elif package_name[0] == 'com.oneapp.max.cleaner.booster.cn':
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label="Space")
    # else:
    #     plt.plot(wights, highs_float, "c-", linewidth=1, label=package_name[0])

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
    path = "report/cpu" + time_now
    # path="D:/"+ time_now
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


def time_control_mem():
    global filename1
    write_head_mem()
    while True:
        end_time = time.time()
        if (end_time - start_time) / 60 >= tol_time:  # 分钟
            # if end_time - start_time >= tol_time:    #秒
            break
        time.sleep(1)
        adb = "adb shell dumpsys meminfo > log_su/adb_info1.csv"
        d = os.system(adb)
        filename1 = "log_su/adb_info1.csv"
        get_mem()
    # write_report_mem()
# 控制监测时间
def time_control_cpu():
    global filename
    write_head_cpu()
    while True:
        end_time = time.time()
        if (end_time - start_time) / 60 >= tol_time:  # 分钟
            # if end_time - start_time >= tol_time:  # 秒
            break
        time.sleep(2)
        adb = "adb shell top -n 1 > log_su/adb_info.csv"
        d = os.system(adb)
        filename = "log_su/adb_info.csv"
        get_cpu()

def draw_line_cpu():
    filename = 'log_su/cpuinfo.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        highs = []
        wights = []
        for row in reader:
            high = row[2]
            wight = row[1]
            highs.append(high)
            wights.append(wight)
        # print(highs)

    # wights = time_list_cpu
    highs_float = list(map(float, highs))
    # 普通折线图
    line = Line('CPU')
    line.add('cpu', wights, highs_float,  is_stack=True, is_label_show=True,
                 is_smooth=False ,is_more_utils =True,is_datazoom_show=False, yaxis_formatter="%",
                 mark_point=["max", "min"], mark_line=["average"])
    line.show_config()
    line.render(path='report/cpu折线图.html')
def draw_line_mem():
    filename = 'log_su/meminfo.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        highs = []
        wights = []
        for row in reader:
            high = row[2]
            wight = row[1]
            highs.append(high)
            wights.append(wight)
        # print(highs)

    # wights = time_list_cpu
    highs_float = list(map(float, highs))
    # 普通折线图
    line = Line('MEM')
    line.add('mem', wights, highs_float, is_stack=True, is_label_show=True, is_smooth=False,is_more_utils =True, is_datazoom_show=False,
                 yaxis_formatter="MB",  mark_point=["max", "min"], mark_line=["average"])
    line.show_config()
    line.render(path='report/mem折线图.html')

def draw_line_fps():
    filename = 'log_su/fpsinfo.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)
        highs = []
        wights = []
        for row in reader:
            high = row[2]
            wight = row[1]
            highs.append(high)
            wights.append(wight)
        # print(highs)

    # wights = time_list_cpu
    highs_float = list(map(float, highs))
    # 普通折线图
    line= Line('FPS')
    line.add('fps', wights, highs_float, is_stack=True, is_label_show=True, is_smooth=False,is_more_utils =True, is_datazoom_show=False,
                 yaxis_formatter="FPS",  mark_point=["max", "min"], mark_line=["average"])
    line.show_config()
    line.render(path='report/fps折线图.html')

def copy_fps():
    adb = "adb pull /sdcard/SuperMap/TestLog/fpsinfo.csv ./log_su/"
    d = os.system(adb)


def draw_report():
    filename_fps = 'log_su/fpsinfo.csv'
    filename_cpu = 'log_su/cpuinfo.csv'
    filename_mem = 'log_su/meminfo.csv'
    page = Page()
    # fps------------------------------------------------------------------------------------
    with open(filename_fps) as f_fps:
        reader = csv.reader(f_fps)
        header_row = next(reader)
        highs_fps = []
        wights_fps = []
        for row in reader:
            high = row[2]
            wight = row[1]
            highs_fps.append(high)
            wights_fps.append(wight)
    highs_float_fps = list(map(float, highs_fps))
    # 折线图
    line_fps = Line('FPS')
    # 设置属性label_color=['#218868']颜色
    line_fps.add('fps', wights_fps, highs_float_fps, is_stack=True, is_label_show=False, is_smooth=False, is_more_utils=True,
             is_datazoom_show=True,
             yaxis_formatter="FPS", mark_point=["max", "min"],mark_point_symbolsize=[70,70],mark_line=["average"])
    # mem-------------------------------------------------------------------------------
    with open(filename_mem) as f_mem:
        reader = csv.reader(f_mem)
        header_row = next(reader)
        highs_mem = []
        wights_mem = []
        for row in reader:
            high = row[2]
            wight = row[1]
            highs_mem.append(high)
            wights_mem.append(wight)
    highs_float = list(map(float, highs_mem))
    # 普通折线图
    line_mem = Line('MEM')
    line_mem.add('mem', wights_mem, highs_float, is_stack=True, is_label_show=False, is_smooth=False, is_more_utils=True,
             is_datazoom_show=True,
             yaxis_formatter="MB", mark_point=["max", "min"],mark_point_symbolsize=[70,70],mark_line=["average"])
    # cpu-------------------------------------------------------------------------------
    with open(filename_cpu) as f_cpu:
        reader = csv.reader(f_cpu)
        header_row = next(reader)
        highs_cpu = []
        wights_cpu = []
        for row in reader:
            high = row[2]
            wight = row[1]
            highs_cpu.append(high)
            wights_cpu.append(wight)
    highs_float = list(map(float, highs_cpu))
    # 普通折线图
    line_cpu = Line('CPU')



    # 属性xaxis_rotate=90 x轴旋转
    line_cpu.add('cpu', wights_cpu, highs_float, is_stack=True, is_label_show=False, is_smooth=False, is_more_utils=True,
                 is_datazoom_show=True,
                 yaxis_formatter="%", mark_point=["max", "min"],mark_point_symbolsize=[70,70], mark_line=["average"])

    page.add(line_cpu)
    page.add(line_mem)
    page.add(line_fps)
    now_v = time.strftime("%H:%M:%S", time.localtime())
    page.render(path='report/'+time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) +'.html')



threads = []
t1 = threading.Thread(target=time_control_cpu,name='time_control_cpu')
threads.append(t1)
t2 = threading.Thread(target=time_control_mem,name='time_control_mem')
threads.append(t2)
print(threads)

if __name__ == "__main__":
    name_app()
    # # tol_time = int(input("请输入脚本执行时间(分钟)："))
    ###########开始执行获取cpu、mem信息—————先修改时间（分钟）———————————————————————————————————
    tol_time = 390
    start_time = time.time()
    get_applist()
    # write_head()
    for t in threads:
        print(t)
        t.start()
    for t in threads:
        t.join()
    print(threading.active_count())
    ###############执行结束------------------------------------------------------------
    # mapping_mem()
    # mapping_cpu()
    ########### 输出优化后的图表----------------------------------------------------------------------
    # draw_line_cpu()
    # draw_line_mem()
    # draw_line_fps()
    ###########输出结束--------------------------------------------------------------
    ##############将帧率csv拷贝出来---------------------------------
    copy_fps()
    # 输出图表到一个html----------------------------------------------------------------
    draw_report()
    # 输出结束---------------------------------------------------------------


